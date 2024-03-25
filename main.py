import Giaodien
from Banco import *


if __name__ == '__main__':
    keep_playing = True

    Banco = Banco(game_mode=0, ai=True, depth=1, log=True)

    while keep_playing:
        Giaodien.khoitao()
        Banco.place_pieces()
        Giaodien.ve_background(Banco)
        keep_playing = Giaodien.batdau(Banco)