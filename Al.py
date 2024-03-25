import math
from Banco import Banco
from QuanCo import *
from functools import wraps
from Log import Logger, BancoRepr
import random


log = Logger()


def log_tree(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        Banco: Banco = args[0]
        if Banco.log:
            depth = args[1]
            write_to_file(Banco, depth)
        return func(*args, **kwargs)
    return wrapper


def write_to_file(Banco: Banco, current_depth):
    global log
    if Banco.depth == current_depth:
        log.clear()
    Banco_repr = BancoRepr(Banco.mang_unicode(), current_depth, Banco.danh_gia())
    log.append(Banco_repr)


@log_tree
def minimax(Banco, depth, alpha, beta, max_player, save_move, data):

    if depth == 0 or Banco.cuoi_cung():
        data[1] = Banco.danh_gia()
        return data

    if max_player:
        max_eval = -math.inf
        for i in range(8):
            for j in range(8):
                if isinstance(Banco[i][j], QuanCo) and Banco[i][j].color != Banco.mau_xuat_phat():
                    piece = Banco[i][j]
                    dichuyen = piece.loc_dichuyen(piece.dichuyen(Banco), Banco)
                    for move in dichuyen:
                        Banco.make_move(piece, move[0], move[1], keep_history=True)
                        evaluation = minimax(Banco, depth - 1, alpha, beta, False, False, data)[1]
                        if save_move:
                            if evaluation >= max_eval:
                                if evaluation > data[1]:
                                    data.clear()
                                    data[1] = evaluation
                                    data[0] = [piece, move, evaluation]
                                elif evaluation == data[1]:
                                    data[0].append([piece, move, evaluation])
                        Banco.khong_dichuyen(piece)
                        max_eval = max(max_eval, evaluation)
                        alpha = max(alpha, evaluation)
                        if beta <= alpha:
                            break
        return data
    else:
        min_eval = math.inf
        for i in range(8):
            for j in range(8):
                if isinstance(Banco[i][j], QuanCo) and Banco[i][j].color == Banco.mau_xuat_phat():
                    piece = Banco[i][j]
                    dichuyen = piece.dichuyen(Banco)
                    for move in dichuyen:
                        Banco.make_move(piece, move[0], move[1], keep_history=True)
                        evaluation = minimax(Banco, depth - 1, alpha, beta, True, False, data)[1]
                        Banco.khong_dichuyen(piece)
                        min_eval = min(min_eval, evaluation)
                        beta = min(beta, evaluation)
                        if beta <= alpha:
                            break
        return data


def get_ai_move(Banco):
    dichuyen = minimax(Banco, Banco.depth, -math.inf, math.inf, True, True, [[], 0])
    if Banco.log:
        log.write()
    if len(dichuyen[0]) == 0:
        return False
    best_score = max(dichuyen[0], key=lambda x: x[2])[2]
    piece_and_move = random.choice([move for move in dichuyen[0] if move[2] == best_score])
    piece = piece_and_move[0]
    move = piece_and_move[1]
    if isinstance(piece, QuanCo) and len(move) > 0 and isinstance(move, tuple):
        Banco.make_move(piece, move[0], move[1])
    return True


def get_random_move(Banco):
    pieces = []
    dichuyen = []
    for i in range(8):
        for j in range(8):
            if isinstance(Banco[i][j], QuanCo) and Banco[i][j].color != Banco.mau_xuat_phat():
                pieces.append(Banco[i][j])
    for piece in pieces[:]:
        piece_dichuyen = piece.loc_dichuyen(piece.dichuyen(Banco), Banco)
        if len(piece_dichuyen) == 0:
            pieces.remove(piece)
        else:
            dichuyen.append(piece_dichuyen)
    if len(pieces) == 0:
        return
    piece = random.choice(pieces)
    move = random.choice(dichuyen[pieces.index(piece)])
    if isinstance(piece, QuanCo) and len(move) > 0:
        Banco.make_move(piece, move[0], move[1])
