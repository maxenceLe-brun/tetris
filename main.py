import pygame
import random
"""

###############################################################################
#                             Project : Tetris                                #
#                                                                             #
#                                  By :                                       #
#                            Maxence Le Brun                                  #
#                             Clement Papia                                   #
###############################################################################


"""


MAP = [[-1 for a in range(10)] for b in range(25)]
MVD_MAP = MAP[:]
LAST_MOVE = MAP[:]
#MAP est la matrice sans le block actuellement joué
#MVD_MAP est la matrice avec le block joué
#LAST_MOVE sert de repère lors du moindre mouvement



red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 215, 0)
magenta = (255, 0, 255)
orange = (255, 165, 0)
cyan = (0, 255, 255)
colors = [red, green, blue, yellow, magenta, orange, cyan, (60,)*3]
#La numérotation de la matrice a été faite pour suivre cette liste : -1 étant le vide.


BLOCKS_UP = [[[0, 0, -1], [-1, 0, 0]], [[-1, 1, 1], [1, 1, -1]], [[2, -1, -1], [2, 2, 2]],
             [[3, 3], [3, 3]], [[-1, 4, -1], [4, 4, 4]], [[-1, -1, 5], [5, 5, 5]],
             [[6, 6, 6, 6]]]
#BLOCKS_UP est la version initiale d'un block

BLOCKS_RG = [[[-1, 0], [0, 0], [0, -1]], [[1, -1], [1, 1], [-1, 1]],
             [[2, 2], [2, -1],[2, -1]], BLOCKS_UP[3], [[4, -1], [4, 4], [4, -1]],
             [[5, -1], [5, -1], [5, 5]], [[6], [6], [6], [6]]]
#BLOCKS_RG est la version a rotation unique du block

BLOCKS_DW = [BLOCKS_UP[0], BLOCKS_UP[1],[[2, 2, 2], [-1, -1, 2]], BLOCKS_UP[3],
             [[4, 4, 4], [-1, 4, -1]], [[5, 5, 5], [5, -1, -1]], BLOCKS_UP[6]]
#BLOCKS_DW est la version du block avec deux rotations (soit : retourné)

BLOCKS_LF = [BLOCKS_RG[0], BLOCKS_RG[1], [[-1, 2], [-1, 2], [2, 2]], BLOCKS_UP[3],
             [[-1, 4], [4, 4], [-1, 4]], [[5, 5], [-1, 5], [-1, 5]], BLOCKS_RG[6]]
#BLOCKS_LF est la dernière rotation avant la récursivitée.

ANGLE = [BLOCKS_UP, BLOCKS_RG, BLOCKS_DW, BLOCKS_LF]


pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 16)
screen = pygame.display.set_mode([500, 700])
running = True
screen.fill((200,)*3) #un fond assez clair et appréciable a voir
pygame.display.flip()

N = -1
Next = random.randrange(0,7)
angle = 0
time = 0
turn = 1
level = 1
down = False
score = 0
SCORE = 0
pygame.draw.rect(screen, (200,)*3, (330, 300,len(str(SCORE))*16, 16))
scored = my_font.render("Score : ", False, (0,)*3)
text_surface = my_font.render(str(SCORE), False, (0,)*3)
screen.blit(scored, (280,300))
screen.blit(text_surface, (330 + 8*len(str(SCORE)), 300))
def cube(x:int, y:int, rgb:tuple): 
    """
    

    Parameters
    ----------
    x : type = int
        the X coordinate
    y : type = int
        the Y coordinate
    rgb : type = tuple
        the color of the block

    Returns
    -------
    Draw something ?

    """
    if rgb != (60,)*3:
        pygame.draw.rect(screen, (0,)*3, (x, y, 20, 20))
        pygame.draw.rect(screen, rgb, (x+1, y+1, 18, 18))
        
    else:
        pygame.draw.rect(screen, rgb, (x, y, 20, 20))

def erase():
    for a in range(len(MAP)):
        for b in range(len(MAP[a])):
            cube(50 + 20 * b, 50 + 20 * a, colors[MAP[a][b]])

def re_place():
    for a in range(len(MAP)):
        for b in range(len(MAP[a])):
            cube(50 + 20 * b, 50 + 20 * a, colors[MVD_MAP[a][b]])

erase()
while running:
    """
    légende : 
        x & y sont les coordonées
        X & Y sont respectivement la longueur et la hauteur d'un block
        N est le block joué actuellement
        Next est le block suivant, qui s'applique une fois le block actuel placé
        time est un compteur de tick
        turn est un compteur de rapidité pour chaque ligne gagnés
    """
    if N == -1:
        MAP = MVD_MAP[:]
        if MAP[0][5] != -1:
            break
        for a in range(len(MAP)):
            if -1 not in MAP[a] and a != 24:
                MAP = [[-1 for a in range(10)]] + MAP[:a] + MAP[a+1:]
                turn += 1
                score += 25 * level
            if -1 not in MAP[a] and a == 24:
                MAP = [[-1 for a in range(10)]] + MAP[:a]
                turn += 1
                score += 25 * level
        MVD_MAP = MAP[:]
        angle = 0
        N = Next
        Next = random.randrange(0,7)
        pygame.draw.rect(screen, (120,)*3, (280, 80, 120, 120))
        for a in range(len(ANGLE[0][Next])):
            for b in range(len(ANGLE[0][Next][a])):
                if ANGLE[0][Next][a][b] != -1:
                    cube(300 + 20 * b, 100 + 20 * a, colors[ANGLE[0][Next][a][b]])
        pygame.display.flip()
        Y = len(BLOCKS_UP[N])
        y = 0
        X = len(BLOCKS_UP[N][0])
        x = 0
        for a in range(Y):
            MVD_MAP[a] = MVD_MAP[a][:((10-X)//2)] + ANGLE[angle][N][a] + MVD_MAP[a][((10-X)//2)+X:]
    time += 1
    
    if down:
        time += 5
    if score != 0:
        SCORE += score + (score*(score // 25 - 1))
        pygame.draw.rect(screen, (200,)*3, (330, 300,len(str(SCORE))*20, 20))
        text_surface = my_font.render(str(SCORE), False, (0,)*3)
        screen.blit(text_surface,(330 + 2*len(str(SCORE)), 300))
        
        score = 0
    if time >= 2000 - 20 * turn and y < 24 - (Y-1):
        """
        Go expliquer le if juste en dessous : 
        
        "False not in" pour verifier que rien n'est "False" dans les essais suivants;
        [
            [MAP[y+Y][((10 - X) // 2) + x + a] for a in range(X)] == [-1 for b in range(X)]
            Essaye si la ligne juste dessous le block est vide.
            Calcul : 
                y+Y pour être juste en dessous
                ((10 - X) // 2 + x + a) pour parcourir de gauche a droite la longueur du block sans déborder
            
            
            
         ANGLE[angle % 4][N][-1][a] == -1 and (
             [MAP[y + Y][((10 - X) // 2) + x + a] for a in range(X)][a] != -1 or [
                 MAP[y + Y][((10 - X) // 2) + x + a] for a in range(X)][a] == -1))
         
         Essaye si dans la dernière ligne du block, il y a des espaces vide et si juste en dessous
         il y a un block (ou non) capable de rentrer dans cet espace vide.
                
        
        
        (ANGLE[angle % 4][N][-1][a] != -1 or ANGLE[angle % 4][N][-1][a] == -1
         ) and [MAP[y + Y][((10 - X) // 2) + x + a] for a in range(X)][a] == -1) for a in range(X)]
        Essaye si pour la dernière ligne du block il y a un block (ou non) et si en dessous du block
        il y a un espace vide pour le completer.
        """
        if False not in [[MAP[y+Y][((10-X)//2)+x + a] for a in range(X)] == [-1 for b in range(X)] or (ANGLE[angle % 4][N][-1][a] == -1 and ([MAP[y + Y][((10 - X) // 2) + x + a] for a in range(X)][a] != -1 or [MAP[y + Y][((10 - X) // 2) + x + a] for a in range(X)][a] == -1)) or ((ANGLE[angle % 4][N][-1][a] != -1 or ANGLE[angle % 4][N][-1][a] == -1) and [MAP[y + Y][((10 - X) // 2) + x + a] for a in range(X)][a] == -1) for a in range(X)]:
            time = 0
            MVD_MAP = MAP[:]
            y += 1
            for a in range(Y):
                MVD_MAP[a+y] = MVD_MAP[a+y][:((10-X)//2)+x] + ANGLE[angle%4][N][a] + MVD_MAP[a+y][((10-X)//2) + X + x:]
            for a in range(len(MAP)):
                for b in range(len(MAP[a])):
                    if MVD_MAP[a][b] != MAP[a][b] and MAP[a][b] != -1 and MVD_MAP[a][b] != -1:
                        y -= 1
                        MVD_MAP = MAP[:]
                        for c in range(Y):
                            MVD_MAP[c+y] = MVD_MAP[c+y][:((10-X)//2)+x] + ANGLE[angle%4][N][c] + MVD_MAP[c+y][((10-X)//2) + X + x:]
                        N =- 1
            for a in range(Y):
                for b in range(X):
                    if MVD_MAP[y+a][((10-X)//2)+x+b] != -1 and MAP[y+a][((10-X)//2)+x+b] != -1:
                        y -= 1
                        MVD_MAP = MAP[:]
                        for c in range(Y):
                            MVD_MAP[c+y] = MVD_MAP[c+y][:((10-X)//2)+x] + ANGLE[angle%4][N][c] + MVD_MAP[c+y][((10-X)//2) + X + x:]
                        N =- 1
        else:
            N =- 1
    if time >= 2000 - 20 * turn and y == 24 - (Y-1):
        N = -1
    
    if N == -1:
        for a in range(len(MAP)):
            for b in range(len(MAP[a])):
                if MAP[a][b] != -1 and MVD_MAP[a][b] == -1:
                    MVD_MAP[a][b] = MAP[a][b]
        time = 0
        MAP = MVD_MAP[:]
    
    if LAST_MOVE != MVD_MAP:
        for a in range(len(MAP)):
            for b in range(len(MAP[a])):
                if MAP[a][b] != -1 and MVD_MAP[a][b] == -1:
                    MVD_MAP[a][b] = MAP[a][b]
        re_place()
        pygame.display.flip()
        LAST_MOVE = MVD_MAP[:]
        
    if down:
        time += 15
        
    for event in pygame.event.get():
        if len(str(event)) > 60:
            
            if str(event)[40:50] == '1073741906' and ((N != 6 and y < 24 - (Y-1)) or (N == 6 and y < 25 - 4)):
                angle += 1
                MVD_MAP = MAP[:]
                Y = len(ANGLE[angle % 4][N])
                X = len(ANGLE[angle % 4][N][0])
                if X//2 + x > 5:
                    x -= (X//2+x)-5
                if X//2 + X%2 + x < X-5 + X%2:
                    x -= X-5 +X%2
                for a in range(Y):
                    MVD_MAP[a+y] = MVD_MAP[a+y][:((10-X)//2)+x] + ANGLE[angle%4][N][a] + MVD_MAP[a+y][((10-X)//2) + X + x:]
                for a in range(len(MAP)):
                    for b in range(len(MAP[a])):
                        if MVD_MAP[a][b] != MAP[a][b] and MAP[a][b] != -1 and MVD_MAP[a][b] != -1:
                            angle -= 1
                            MVD_MAP = MAP[:]
                            Y = len(ANGLE[angle % 4][N])
                            X = len(ANGLE[angle % 4][N][0])
                            for c in range(Y):
                                MVD_MAP[c+y] = MVD_MAP[c+y][:((10-X)//2)+x] + ANGLE[angle%4][N][c] + MVD_MAP[c+y][((10-X)//2) + X + x:]
            if str(event)[40:50] == '1073741903' and X//2 + x < 5:
                if False not in [[[MAP[y + a][((10 - X) // 2) + X + x]] for a in range(Y)] == [[-1] for a in range(Y)] or ([[MAP[y + a][((10 - X) // 2) + X + x]] for a in range(Y)][a][0] == -1 and (ANGLE[angle % 4][N][a][-1] != -1 or ANGLE[angle % 4][N][a][-1] == -1)) or (([[MAP[y + a][((10 - X) // 2) + X + x]] for a in range(Y)][a][0] != -1 or [[MAP[y + a][((10 - X) // 2) + X + x]] for a in range(Y)][a][0] == -1) and ANGLE[angle % 4][N][a][-1] == -1) for a in range(Y)]:
                    MVD_MAP = MAP[:]
                    x+=1
                    for a in range(Y):
                        MVD_MAP[a+y] = MVD_MAP[a+y][:((10-X)//2)+x] + ANGLE[angle%4][N][a] + MVD_MAP[a+y][((10-X)//2) + X + x:]
                    for a in range(len(MAP)):
                        for b in range(len(MAP[a])):
                            if MVD_MAP[a][b] != MAP[a][b] and MAP[a][b] != -1 and MVD_MAP[a][b] != -1:
                                x -= 1
                                MVD_MAP = MAP[:]
                                Y = len(ANGLE[angle % 4][N])
                                X = len(ANGLE[angle % 4][N][0])
                                for c in range(Y):
                                    MVD_MAP[c+y] = MVD_MAP[c+y][:((10-X)//2)+x] + ANGLE[angle%4][N][c] + MVD_MAP[c+y][((10-X)//2) + X + x:]
                        
            
            if str(event)[40:50] == '1073741904' and X//2 + X%2 + x > X-5 + X%2:
                if False not in [[[MAP[y + a][((10 - X) // 2) + x - 1]] for a in range(Y)] == [[-1] for a in range(Y)] or ([[MAP[y + a][((10 - X) // 2) + x - 1]] for a in range(Y)][a][0] == -1 and (ANGLE[angle % 4][N][a][0] != -1 or ANGLE[angle % 4][N][a][0] == -1)) or (([[MAP[y + a][((10 - X) // 2) + x -1]] for a in range(Y)][a][0] != -1 or [[MAP[y + a][((10 - X) // 2) + x -1]] for a in range(Y)][a][0] == -1) and ANGLE[angle % 4][N][a][0] == -1) for a in range(Y)]:
                    MVD_MAP = MAP[:]
                    x -= 1
                    for a in range(Y):
                        MVD_MAP[a+y] = MVD_MAP[a+y][:((10-X)//2)+x] + ANGLE[angle%4][N][a] + MVD_MAP[a+y][((10-X)//2) + X + x:]
                    for a in range(len(MAP)):
                        for b in range(len(MAP[a])):
                            if MVD_MAP[a][b] != MAP[a][b] and MAP[a][b] != -1 and MVD_MAP[a][b] != -1:
                                x += 1
                                MVD_MAP = MAP[:]
                                Y = len(ANGLE[angle % 4][N])
                                X = len(ANGLE[angle % 4][N][0])
                                for c in range(Y):
                                    MVD_MAP[c+y] = MVD_MAP[c+y][:((10-X)//2)+x] + ANGLE[angle%4][N][c] + MVD_MAP[c+y][((10-X)//2) + X + x:]
            
            if str(event)[42:52] == '1073741905':
                down = True
            if str(event)[40:50] == '1073741905':
                down = False
                
           
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
pygame.quit()
