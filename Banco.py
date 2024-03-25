from QuanCo import *
from copy import deepcopy


class Banco:

    trang = []
    den = []

    def __init__(self, game_mode, ai=False, depth=2, log=False): 
        self.Banco = []
        self.game_mode = game_mode
        self.depth = depth
        self.ai = ai
        self.log = log

    def khoitao_Banco(self):
        for i in range(8):
            self.Banco.append(['empty-block' for _ in range(8)])

    def place_pieces(self):
        self.Banco.clear()
        self.trang.clear()
        self.den.clear()
        self.khoitao_Banco()
        self.whitecon_vua = Con_vua('white', 0, 4, '\u265A')
        self.blackcon_vua = Con_vua('black', 7, 4, '\u2654')
        for j in range(8):
            self[1][j] = Con_tot('white', 1, j, '\u265F')
            self[6][j] = Con_tot('black', 6, j, '\u2659')
        self[0][0] = Con_xe('white', 0, 0, '\u265C')
        self[0][7] = Con_xe('white', 0, 7, '\u265C')
        self[0][1] = Con_ma('white', 0, 1, '\u265E')
        self[0][6] = Con_ma('white', 0, 6, '\u265E')
        self[0][2] = Con_tuong('white', 0, 2, '\u265D')
        self[0][5] = Con_tuong('white', 0, 5, '\u265D')
        self[0][3] = Con_hau('white', 0, 3, '\u265B')
        self[0][4] = self.whitecon_vua
        self[7][0] = Con_xe('black', 7, 0, '\u2656')
        self[7][7] = Con_xe('black', 7, 7, '\u2656')
        self[7][1] = Con_ma('black', 7, 1, '\u2658')
        self[7][6] = Con_ma('black', 7, 6, '\u2658')
        self[7][2] = Con_tuong('black', 7, 2, '\u2657')
        self[7][5] = Con_tuong('black', 7, 5, '\u2657')
        self[7][3] = Con_hau('black', 7, 3, '\u2655')
        self[7][4] = self.blackcon_vua

        self.save_pieces()

        if self.game_mode != 0:
            self.reverse()

    def save_pieces(self):
        for i in range(8):
            for j in range(8):
                if isinstance(self[i][j], QuanCo):
                    if self[i][j].color == 'white':
                        self.trang.append(self[i][j])
                    else:
                        self.den.append(self[i][j])

    def make_move(self, piece, x, y, keep_history=False):
        old_x = piece.x
        old_y = piece.y
        if keep_history:
            self.Banco[old_x][old_y].dat_lanan_cuoicung(self.Banco[x][y])
        else:
            if isinstance(self.Banco[x][y], QuanCo):
                if self.Banco[x][y].color == 'white':
                    self.trang.remove(self.Banco[x][y])
                else:
                    self.den.remove(self.Banco[x][y])
        self.Banco[x][y] = self.Banco[old_x][old_y]
        self.Banco[old_x][old_y] = 'empty-block'
        self.Banco[x][y].dat_vi_tri(x, y, keep_history)

    def khong_dichuyen(self, piece):
        x = piece.x
        y = piece.y
        self.Banco[x][y].dat_vi_tri_cu()
        old_x = piece.x
        old_y = piece.y
        self.Banco[old_x][old_y] = self.Banco[x][y]
        self.Banco[x][y] = piece.an_cuoicung()

    def reverse(self):
        self.Banco = self.Banco[::-1]
        for i in range(8):
            for j in range(8):
                if isinstance(self.Banco[i][j], QuanCo):
                    piece = self.Banco[i][j]
                    piece.x = i
                    piece.y = j

    def __getitem__(self, item):
        return self.Banco[item]

    def doi_thu(self, piece, x, y):
        if not self.is_valid_move(x, y):
            return False
        if isinstance(self.Banco[x][y], QuanCo):
            return piece.color != self[x][y].color
        return False

    def ban_be(self, piece, x, y):
        if not self.is_valid_move(x, y):
            return False
        if isinstance(self[x][y], QuanCo):
            return piece.color == self[x][y].color
        return False

    @staticmethod
    def is_valid_move(x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def tro_trong(self, x, y):
        if not self.is_valid_move(x, y):
            return False
        return not isinstance(self[x][y], QuanCo)

    def mau_xuat_phat(self):
        if self.game_mode == 0:
            return 'white'
        return 'black'

    def chieu_tuong(self, color, move=None):
        if color == 'white':
            enemies = self.den
            con_vua = self.whitecon_vua
        else:
            enemies = self.trang
            con_vua = self.blackcon_vua
        threats = []
        for enemy in enemies:
            dichuyen = enemy.dichuyen(self)
            if (con_vua.x, con_vua.y) in dichuyen:
                threats.append(enemy)
        if move and len(threats) == 1 and threats[0].x == move[0] and threats[0].y == move[1]:
            return False
        return True if len(threats) > 0 else False

    def cuoi_cung(self):
        terminal1 = self.doitrang_win()
        terminal2 = self.doiden_win()
        terminal3 = self.ve()
        return terminal1 or terminal2 or terminal3

    def ve(self):
        if not self.chieu_tuong('white') and not self.trangthai_moi('white'):
            return True
        if not self.chieu_tuong('black') and not self.trangthai_moi('black'):
            return True
        if self.thieu_quan():
            return True
        return False

    def doitrang_win(self):
        if self.chieu_tuong('black') and not self.trangthai_moi('black'):
            return True
        return False

    def doiden_win(self):
        if self.chieu_tuong('white') and not self.trangthai_moi('white'):
            return True
        return False

    def trangthai_moi(self, color):
        total_dichuyen = 0
        for i in range(8):
            for j in range(8):
                if isinstance(self[i][j], QuanCo) and self[i][j].color == color:
                    piece = self[i][j]
                    total_dichuyen += len(piece.loc_dichuyen(piece.dichuyen(self), self))
                    if total_dichuyen > 0:
                        return True
        return False

    def thieu_quan(self):
        total_white_con_mas = 0
        total_black_con_mas = 0
        total_white_con_tuongs = 0
        total_black_con_tuongs = 0
        total_other_white_pieces = 0
        total_other_black_pieces = 0

        for piece in self.trang:
            if piece.type == 'con_ma':
                total_white_con_mas += 1
            elif piece.type == 'con_tuong':
                total_white_con_tuongs += 1
            elif piece.type != 'con_vua':
                total_other_white_pieces += 1

        for piece in self.den:
            if piece.type == 'con_ma':
                total_black_con_mas += 1
            elif piece.type == 'con_tuong':
                total_black_con_tuongs += 1
            elif piece.type != 'con_vua':
                total_other_black_pieces += 1

        weak_white_pieces = total_white_con_tuongs + total_white_con_mas
        weak_black_pieces = total_black_con_tuongs + total_black_con_mas

        if self.whitecon_vua and self.blackcon_vua:
            if weak_white_pieces + total_other_white_pieces + weak_black_pieces + total_other_black_pieces == 0:
                return True
            if weak_white_pieces + total_other_white_pieces == 0:
                if weak_black_pieces == 1:
                    return True
            if weak_black_pieces + total_other_black_pieces == 0:
                if weak_white_pieces == 1:
                    return True
            if len(self.trang) == 1 and len(self.den) == 16 or len(self.den) == 1 and len(self.trang) == 16:
                return True
            if total_white_con_mas == weak_white_pieces + total_other_white_pieces and len(self.den) == 1:
                return True
            if total_black_con_mas == weak_black_pieces + total_other_black_pieces and len(self.trang) == 1:
                return True
            if weak_white_pieces == weak_black_pieces == 1 and total_other_white_pieces == total_other_black_pieces == 0:
                return True

    def danh_gia(self):
        white_points = 0
        black_points = 0
        for i in range(8):
            for j in range(8):
                if isinstance(self[i][j], QuanCo):
                    piece = self[i][j]
                    if piece.color == 'white':
                        white_points += piece.dat_diem()
                    else:
                        black_points += piece.dat_diem()
        if self.game_mode == 0:
            return black_points - white_points
        return white_points - black_points

    def __str__(self):
        return str(self[::-1]).replace('], ', ']\n')

    def __repr__(self):
        return 'Banco'

    def mang_unicode(self):
        data = deepcopy(self.Banco)
        for idx, row in enumerate(self.Banco):
            for i, p in enumerate(row):
                if isinstance(p, QuanCo):
                    un = p.unicode
                else:
                    un = '\u25AF'
                data[idx][i] = un
        return data[::-1]

    def timthay_vua(self, piece):
        if piece.color == 'white':
            return self.whitecon_vua
        return self.blackcon_vua


