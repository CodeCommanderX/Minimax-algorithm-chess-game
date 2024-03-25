import operator
from itertools import product


class QuanCo:

    eaten_pieces_history = []
    has_moved_history = []
    position_history = []

    def __init__(self, color, x, y, unicode):
        self.moved = False
        self.color = color
        self.x = x
        self.y = y
        self.type = self.__class__.__name__
        self.unicode = unicode

    def loc_dichuyen(self, dichuyen, Banco):
        final_dichuyen = dichuyen[:]
        for move in dichuyen:
            Banco.make_move(self, move[0], move[1], keep_history=True)
            if Banco.chieu_tuong(self.color, move):
                final_dichuyen.remove(move)
            Banco.khong_dichuyen(self)
        return final_dichuyen

    def dichuyen(self, Banco):
        pass

    def an_cuoicung(self):
        return self.eaten_pieces_history.pop()

    def dat_lanan_cuoicung(self, piece):
        self.eaten_pieces_history.append(piece)

    def dat_vi_tri(self, x, y, keep_history):
        if keep_history:
            self.position_history.append(self.x)
            self.position_history.append(self.y)
            self.has_moved_history.append(self.moved)
        self.x = x
        self.y = y
        self.moved = True

    def dat_vi_tri_cu(self):
        position_y = self.position_history.pop()
        position_x = self.position_history.pop()
        self.y = position_y
        self.x = position_x
        self.moved = self.has_moved_history.pop()

    def dat_diem(self):
        return 0

    def __repr__(self):
        return '{}: {}|{},{}'.format(self.type, self.color, self.x, self.y)


class Con_tot(QuanCo):

    def dichuyen(self, Banco):
        dichuyen = []
        if Banco.game_mode == 0 and self.color == 'white' or Banco.game_mode == 1 and self.color == 'black':
            direction = 1
        else:
            direction = -1
        x = self.x + direction
        if Banco.tro_trong(x, self.y):
            dichuyen.append((x, self.y))
            if self.moved is False and Banco.tro_trong(x + direction, self.y):
                dichuyen.append((x + direction, self.y))
        if Banco.is_valid_move(x, self.y - 1):
            if Banco.doi_thu(self, x, self.y - 1):
                dichuyen.append((x, self.y - 1))
        if Banco.is_valid_move(self.x + direction, self.y + 1):
            if Banco.doi_thu(self, x, self.y + 1):
                dichuyen.append((x, self.y + 1))
        return dichuyen

    def dat_diem(self):
        return 10


class Con_ma(QuanCo):

    def dichuyen(self, Banco):
        dichuyen = []
        add = operator.add
        sub = operator.sub
        op_list = [(add, sub), (sub, add), (add, add), (sub, sub)]
        nums = [(1, 2), (2, 1)]
        combinations = list(product(op_list, nums))
        for comb in combinations:
            x = comb[0][0](self.x, comb[1][0])
            y = comb[0][1](self.y, comb[1][1])
            if Banco.tro_trong(x, y) or Banco.doi_thu(self, x, y):
                dichuyen.append((x, y))
        return dichuyen

    def dat_diem(self):
        return 20


class Con_tuong(QuanCo):

    def dichuyen(self, Banco):
        dichuyen = []
        add = operator.add
        sub = operator.sub
        operators = [(add, add), (add, sub), (sub, add), (sub, sub)]
        for ops in operators:
            for i in range(1, 9):
                x = ops[0](self.x, i)
                y = ops[1](self.y, i)
                if not Banco.is_valid_move(x, y) or Banco.ban_be(self, x, y):
                    break
                if Banco.tro_trong(x, y):
                    dichuyen.append((x, y))
                if Banco.doi_thu(self, x, y):
                    dichuyen.append((x, y))
                    break
        return dichuyen

    def dat_diem(self):
        return 30


class Con_xe(QuanCo):

    def dichuyen(self, Banco):
        dichuyen = []
        dichuyen += self.di_chuyen_doc(Banco)
        dichuyen += self.di_chuyen_ngang(Banco)
        return dichuyen

    def di_chuyen_doc(self, Banco):
        dichuyen = []
        for op in [operator.add, operator.sub]:
            for i in range(1, 9):
                x = op(self.x, i)
                if not Banco.is_valid_move(x, self.y) or Banco.ban_be(self, x, self.y):
                    break
                if Banco.tro_trong(x, self.y):
                    dichuyen.append((x, self.y))
                if Banco.doi_thu(self, x, self.y):
                    dichuyen.append((x, self.y))
                    break
        return dichuyen

    def di_chuyen_ngang(self, Banco):
        dichuyen = []
        for op in [operator.add, operator.sub]:
            for i in range(1, 9):
                y = op(self.y, i)
                if not Banco.is_valid_move(self.x, y) or Banco.ban_be(self, self.x, y):
                    break
                if Banco.tro_trong(self.x, y):
                    dichuyen.append((self.x, y))
                if Banco.doi_thu(self, self.x, y):
                    dichuyen.append((self.x, y))
                    break
        return dichuyen

    def dat_diem(self):
        return 30


class Con_hau(QuanCo):

    def dichuyen(self, Banco):
        dichuyen = []
        con_xe = Con_xe(self.color, self.x, self.y, self.unicode)
        con_tuong = Con_tuong(self.color, self.x, self.y, self.unicode)
        di_chuyen_doc = con_xe.dichuyen(Banco)
        con_tuong_dichuyen = con_tuong.dichuyen(Banco)
        if di_chuyen_doc:
            dichuyen.extend(di_chuyen_doc)
        if con_tuong_dichuyen:
            dichuyen.extend(con_tuong_dichuyen)
        return dichuyen

    def dat_diem(self):
        return 240


class Con_vua(QuanCo):

    def dichuyen(self, Banco):
        dichuyen = []
        dichuyen += self.di_chuyen_ngang(Banco)
        dichuyen += self.di_chuyen_doc(Banco)
        return dichuyen

    def di_chuyen_doc(self, Banco):
        dichuyen = []
        for op in [operator.add, operator.sub]:
            x = op(self.x, 1)
            if Banco.tro_trong(x, self.y) or Banco.doi_thu(self, x, self.y):
                dichuyen.append((x, self.y))
            if Banco.tro_trong(x, self.y + 1) or Banco.doi_thu(self, x, self.y + 1):
                dichuyen.append((x, self.y+1))
            if Banco.tro_trong(x, self.y - 1) or Banco.doi_thu(self, x, self.y - 1):
                dichuyen.append((x, self.y - 1))
        return dichuyen

    def di_chuyen_ngang(self, Banco):
        dichuyen = []
        for op in [operator.add, operator.sub]:
            y = op(self.y, 1)
            if Banco.tro_trong(self.x, y) or Banco.doi_thu(self, self.x, y):
                dichuyen.append((self.x, y))
        return dichuyen

    def dat_diem(self):
        return 1000
