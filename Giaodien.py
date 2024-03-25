import pygame
from QuanCo import *
from Al import get_random_move, get_ai_move

dark_block = pygame.image.load('assets/data/128px/square brown dark_png_shadow_128px.png')
light_block = pygame.image.load('assets/data/128px/square brown light_png_shadow_128px.png')
dark_block = pygame.transform.scale(dark_block, (75, 75))
light_block = pygame.transform.scale(light_block, (75, 75))

whiteCon_tot = pygame.image.load('assets/data/128px/tot_trang.png')
whiteCon_tot = pygame.transform.scale(whiteCon_tot, (75, 75))
whiteCon_xe = pygame.image.load('assets/data/128px/xe_trang.png')
whiteCon_xe = pygame.transform.scale(whiteCon_xe, (75, 75))
whiteCon_tuong = pygame.image.load('assets/data/128px/tuong_trang.png')
whiteCon_tuong = pygame.transform.scale(whiteCon_tuong, (75, 75))
whiteCon_ma = pygame.image.load('assets/data/128px/ma_trang.png')
whiteCon_ma = pygame.transform.scale(whiteCon_ma, (75, 75))
whiteCon_vua = pygame.image.load('assets/data/128px/vua_trang.png')
whiteCon_vua = pygame.transform.scale(whiteCon_vua, (75, 75))
whiteCon_hau = pygame.image.load('assets/data/128px/hau_trang.png')
whiteCon_hau = pygame.transform.scale(whiteCon_hau, (75, 75))

blackCon_tot = pygame.image.load('assets/data/128px/tot_den.png')
blackCon_tot = pygame.transform.scale(blackCon_tot, (75, 75))
blackCon_xe = pygame.image.load('assets/data/128px/xe_den.png')
blackCon_xe = pygame.transform.scale(blackCon_xe, (75, 75))
blackCon_tuong = pygame.image.load('assets/data/128px/tuong_den.png')
blackCon_tuong = pygame.transform.scale(blackCon_tuong, (75, 75))
blackCon_ma = pygame.image.load('assets/data/128px/ma_den.png')
blackCon_ma = pygame.transform.scale(blackCon_ma, (75, 75))
blackCon_vua = pygame.image.load('assets/data/128px/vua_den.png')
blackCon_vua = pygame.transform.scale(blackCon_vua, (75, 75))
blackCon_hau = pygame.image.load('assets/data/128px/hau_den.png')
blackCon_hau = pygame.transform.scale(blackCon_hau, (75, 75))

highlight_block = pygame.image.load('assets/data/128px/highlight_128px.png')
highlight_block = pygame.transform.scale(highlight_block, (75, 75))

screen = None
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)

def khoitao():
    global screen
    pygame.init()
    pygame.display.set_caption('Cờ Vua Minimax')
    icon = pygame.image.load('assets/icon.png')
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((600, 650))
    screen.fill((0, 0, 0))

def ve_background(Banco):
    
    block_x = 0
    for i in range(4):
        block_y = 0
        for j in range(4):
            screen.blit(light_block, (block_x, block_y))
            screen.blit(dark_block, (block_x + 75, block_y))
            screen.blit(light_block, (block_x + 75, block_y + 75))
            screen.blit(dark_block, (block_x, block_y + 75))
            block_y += 150
        block_x += 150
    step_x = 0
    step_y = pygame.display.get_surface().get_size()[0] - 75
    for i in range(8):
        for j in range(8):
            if isinstance(Banco[i][j], QuanCo):
                obj = globals()[f'{Banco[i][j].color}{Banco[i][j].type}']
                screen.blit(obj, (step_x, step_y))
            step_x += 75
        step_x = 0
        step_y -= 75
    pygame.display.update()

def ve_text(text):
    s = pygame.Surface((400, 50))
    s.fill((0, 0, 0))
    screen.blit(s, (100, 600))
    text_surface = font.render(text, False, (240, 240, 240))
    if 've' in text:
        x = 260
    else:
        x = 230
    text_surface_rebatdau = font.render('NHẤN "KHOẢNG CÁCH" ĐỂ CHƠI LẠI', False, (240, 240, 240))
    screen.blit(text_surface, (x, 600))
    screen.blit(text_surface_rebatdau, (150, 620))
    pygame.display.update()


def batdau(Banco):
    global screen
    khathi_piece_dichuyen = []
    running = True
    khanang_dichuyen = False
    kichthuoc = pygame.display.get_surface().get_size()
    game_over = False
    piece = None
    if Banco.game_mode == 1 and Banco.ai:
        get_ai_move(Banco)
        ve_background(Banco)
    while running:
        if game_over:
            ve_text(game_over_txt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x = 7 - pygame.mouse.get_pos()[1] // 75
                y = pygame.mouse.get_pos()[0] // 75
                if isinstance(Banco[x][y], QuanCo) and (Banco.mau_xuat_phat() == Banco[x][y].color or not Banco.ai) and (x, y) not in khathi_piece_dichuyen:
                    piece = Banco[x][y]
                    dichuyen = piece.loc_dichuyen(piece.dichuyen(Banco), Banco)
                    dichuyen_vitri = []
                    khathi_piece_dichuyen = []
                    for move in dichuyen:
                        dichuyen_vitri.append((kichthuoc[0] - (8 - move[1]) * 75, kichthuoc[1] - move[0] * 75 - 125))
                        move_x = 7 - dichuyen_vitri[-1][1] // 75
                        move_y = dichuyen_vitri[-1][0] // 75
                        khathi_piece_dichuyen.append((move_x, move_y))
                    if khanang_dichuyen:
                        ve_background(Banco)
                        khanang_dichuyen = False
                    for move in dichuyen_vitri:
                        khanang_dichuyen = True
                        screen.blit(highlight_block, (move[0], move[1]))
                        pygame.display.update()
                else:
                    clicked_move = (x, y)
                    try:
                        if clicked_move in khathi_piece_dichuyen:
                            Banco.make_move(piece, x, y)
                            khathi_piece_dichuyen.clear()
                            ve_background(Banco)
                            if Banco.ai:
                                get_ai_move(Banco)
                                ve_background(Banco)
                                    
                        if Banco.doitrang_win():
                            game_over = True
                            game_over_txt = 'ĐỘI TRẮNG THẮNG!'
                        elif Banco.doiden_win():
                            game_over = True
                            game_over_txt = 'ĐỘI ĐEN THẮNG!'
                        elif Banco.ve():
                            game_over = True
                            game_over_txt = 'HOÀ!'
                    except UnboundLocalError:
                        pass
