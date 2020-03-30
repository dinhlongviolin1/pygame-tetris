import random, time, pygame, sys
from pygame.locals import *
from pynput import keyboard 

FPS = 500 
WINDOWWIDTH = 1240
WINDOWHEIGHT = 600
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 40
PLAYBOARD = 20
BLANK = '.'

AUTOREPEATRATE = 0
DELAYAUTOSHIFT = 0.12
MOVEDOWNFREQ = 0
DELAYLOCKIN = 0.5

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2) 
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 80

ATTACKTABLE = (0,0,1,2,4,4,6,2,0,10,1) # (0lines,1lines,2lines,3lines,4lines,T Spin Double,T Spin Triple,T Spin Single,T Spin Mini, Perfect Clear, Back 2 Back)
COMBOTABLE = (0,0,1,1,1,2,2,3,3,4,4,4,5) # (0,1,2,3,4,5,6,7,8,9,10,11,12+)

#               R    G    B 
WHITE       = (255, 255, 255) 
GRAY1       = ( 12,  12,  12)
GRAY2       = ( 50,  50,  50)
GRAY3       = (106, 106, 106)
GRAY4       = (150, 150, 150)
BLACK       = (  0,   0,   0) 
RED         = (215,  15,  54) # S-piece
GREEN       = ( 89, 177,   1) # Z-piece
BLUE        = ( 33,  65, 198) # J-piece
ORANGE      = (227,  91,   3) # L-piece
LIGHTBLUE   = ( 15, 155, 215) # I-piece
YELLOW      = (227, 159,   1) # O-piece
PINK        = (175,  40, 138) # T-piece

S_RED         = (107,   9,  27) # S-piece
S_GREEN       = ( 45,  88,   6) # Z-piece
S_BLUE        = ( 17,  33,  99) # J-piece
S_ORANGE      = (113,  45,   6) # L-piece
S_LIGHTBLUE   = ( 10,  78, 107) # I-piece
S_YELLOW      = (113,  79,   8) # O-piece
S_PINK        = ( 87,  21,  69) # T-piece

BORDERCOLOR     = GRAY2
BGCOLOR         = BLACK
TEXTCOLOR       = WHITE
COLORS          = (GREEN, RED, BLUE, ORANGE, LIGHTBLUE, YELLOW, PINK, S_GREEN, S_RED, S_BLUE, S_ORANGE, S_LIGHTBLUE, S_YELLOW, S_PINK, GRAY3, GRAY4)
GAMEOVERCOLOR   = GRAY3

TEMPLATEWIDTH   = 4
TEMPLATEHEIGHT  = 4

S_SHAPE_TEMPLATE = [['.OO.',
                     'OO..',
                     '....',
                     '....'],
                    ['.O..',
                     '.OO.',
                     '..O.',
                     '....'],
                    ['....',
                     '.OO.',
                     'OO..',
                     '....'],
                    ['O...',
                     'OO..',
                     '.O..',
                     '....']]

Z_SHAPE_TEMPLATE = [['OO..',
                     '.OO.',
                     '....',
                     '....'],
                    ['..O.',
                     '.OO.',
                     '.O..',
                     '....'],
                    ['....',
                     'OO..',
                     '.OO.',
                     '....'],
                    ['.O..',
                     'OO..',
                     'O...',
                     '....']]

I_SHAPE_TEMPLATE = [['....',
                     'OOOO',
                     '....',
                     '....'],
                    ['..O.',
                     '..O.',
                     '..O.',
                     '..O.'],
                    ['....',
                     '....',
                     'OOOO',
                     '....'],
                    ['.O..',
                     '.O..',
                     '.O..',
                     '.O..']]


O_SHAPE_TEMPLATE = [['.OO.',
                     '.OO.',
                     '....',
                     '....'],
                    ['.OO.',
                     '.OO.',
                     '....',
                     '....'],
                    ['.OO.',
                     '.OO.',
                     '....',
                     '....'],
                    ['.OO.',
                     '.OO.',
                     '....',
                     '....']]

J_SHAPE_TEMPLATE = [['O...',
                     'OOO.',
                     '....',
                     '....'],
                    ['.OO.',
                     '.O..',
                     '.O..',
                     '....'],
                    ['....',
                     'OOO.',
                     '..O.',
                     '....'],
                    ['.O..',
                     '.O..',
                     'OO..',
                     '....']]

L_SHAPE_TEMPLATE = [['..O.',
                     'OOO.',
                     '....',
                     '....'],
                    ['.O..',
                     '.O..',
                     '.OO.',
                     '....'],
                    ['....',
                     'OOO.',
                     'O...',
                     '....'],
                    ['OO..',
                     '.O..',
                     '.O..',
                     '....']]

T_SHAPE_TEMPLATE = [['.O..',
                     'OOO.',
                     '....',
                     '....'],
                    ['.O..',
                     '.OO.',
                     '.O..',
                     '....'],
                    ['....',
                     'OOO.',
                     '.O..',
                     '....'],
                    ['.O..',
                     'OO..',
                     '.O..',
                     '....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}

PIECES_COLOR = {'S': 0,
                'Z': 1,
                'J': 2,
                'L': 3,
                'I': 4,
                'O': 5,
                'T': 6,
                'S_S': 7,
                'S_Z': 8,
                'S_J': 9,
                'S_L': 10,
                'S_I': 11,
                'S_O': 12,
                'S_T': 13,
                }

set1WallkickData = [((-1, 0), (-1, 1), ( 0,-2), (-1,-2)),
                    (( 1, 0), ( 1,-1), ( 0, 2), ( 1, 2)),
                    (( 1, 0), ( 1,-1), ( 0, 2), ( 1, 2)),
                    ((-1, 0), (-1, 1), ( 0,-2), (-1,-2)),
                    (( 1, 0), ( 1, 1), ( 0,-2), ( 1,-2)),
                    ((-1, 0), (-1,-1), ( 0, 2), (-1, 2)),
                    ((-1, 0), (-1,-1), ( 0, 2), (-1, 2)),
                    (( 1, 0), ( 1, 1), ( 0,-2), ( 1,-2))]

set2WallkickData = [((-2, 0), ( 1, 0), (-2,-1), ( 1, 2)),
                    (( 2, 0), (-1, 0), ( 2, 1), (-1,-2)),
                    ((-1, 0), ( 2, 0), (-1, 2), ( 2,-1)),
                    (( 1, 0), (-2, 0), ( 1,-2), (-2, 1)),
                    (( 2, 0), (-1, 0), ( 2, 1), (-1,-2)),
                    ((-2, 0), ( 1, 0), (-2,-1), ( 1, 2)),
                    (( 1, 0), (-2, 0), ( 1,-2), (-2, 1)),
                    ((-1, 0), ( 2, 0), (-1, 2), ( 2,-1))]

def main():
    global FPSCLOCK, DISPLAYSURF, SMALLFONT, BASICFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    SMALLFONT = pygame.font.Font('freesansbold.ttf', 14)
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption('Tetris')

    showTextScreen('Tetris')
    while True: # game loop
        runGame()
        showTextScreen('Game Over')


def runGame():
    # setup variables for the start of the game
    global loseP1, loseP2, DISPLAYSURF
    boardP1 = getBlankBoard()
    boardP2 = getBlankBoard()
    lastMoveDownTimeP1 = time.time()
    lastMoveSidewaysTimeP1 = time.time()
    lastFallTimeP1 = time.time()
    loseP1 = False
    movingDownP1 = False # note: there is no movingUp variable
    movingLeftP1 = False
    movingRightP1 = False
    canHoldedP1 = True
    P1Tspin = False
    P2Tspin = False
    P1backToBack = False
    P2backToBack = False
    P1ComboCounter = 0
    P2ComboCounter = 0
    spinDirectionP1 = ''
    spinDirectionP2 = ''
    lastMoveDownTimeP2 = time.time()
    lastMoveSidewaysTimeP2 = time.time()
    lastFallTimeP2 = time.time()
    loseP2 = False
    movingDownP2 = False # note: there is no movingUp variable
    movingLeftP2 = False
    movingRightP2 = False
    canHoldedP2 = True
    P1LineRemoved = 0
    P2LineRemoved = 0
    P1PerfectClear = False
    P2PerfectClear = False
    P1backToBackPrint = False
    P2backToBackPrint = False
    P1Tetris = False
    P2Tetris = False
    P1Combo = False
    P2Combo = False
    P1TMini = False
    P2TMini = False
    P1TSingle = False
    P2TSingle = False
    P1TDouble = False
    P2TDouble = False
    P1TTriple = False
    P2TTriple = False

    garbageQueueForP1 = []
    garbageQueueForP2 = []

    lineSentToP1 = 0
    lineSentToP2 = 0

    fallFreq = 1
    bagP1 = list(PIECES.keys())
    bagP2 = list(PIECES.keys())

    fallingPieceP1 = getNewPieceP1(bagP1)
    bagP1.remove(fallingPieceP1['shape'])

    fallingPieceP2 = getNewPieceP2(bagP2)
    bagP2.remove(fallingPieceP2['shape'])

    nextPiece1P1 = getNewPieceP1(bagP1)
    bagP1.remove(nextPiece1P1['shape'])
    nextPiece2P1 = getNewPieceP1(bagP1)
    bagP1.remove(nextPiece2P1['shape'])
    nextPiece3P1 = getNewPieceP1(bagP1)
    bagP1.remove(nextPiece3P1['shape'])
    nextPiece4P1 = getNewPieceP1(bagP1)
    bagP1.remove(nextPiece4P1['shape'])
    nextPiece5P1 = getNewPieceP1(bagP1)
    bagP1.remove(nextPiece5P1['shape'])

    NEXT_PIECESP1 = [nextPiece1P1,nextPiece2P1,nextPiece3P1,nextPiece4P1,nextPiece5P1]
    holdPieceP1 = None

    nextPiece1P2 = getNewPieceP2(bagP2)
    bagP2.remove(nextPiece1P2['shape'])
    nextPiece2P2 = getNewPieceP2(bagP2)
    bagP2.remove(nextPiece2P2['shape'])
    nextPiece3P2 = getNewPieceP2(bagP2)
    bagP2.remove(nextPiece3P2['shape'])
    nextPiece4P2 = getNewPieceP2(bagP2)
    bagP2.remove(nextPiece4P2['shape'])
    nextPiece5P2 = getNewPieceP2(bagP2)
    bagP2.remove(nextPiece5P2['shape'])

    NEXT_PIECESP2 = [nextPiece1P2,nextPiece2P2,nextPiece3P2,nextPiece4P2,nextPiece5P2]
    holdPieceP2 = None

    while True: # game loop
        if fallingPieceP1 == None:
            # No falling piece in play, so start a new piece at the top
            fallingPieceP1 = nextPiece1P1
            if len(bagP1) == 0:
                bagP1 = list(PIECES.keys())
            
            nextPiece1P1 = nextPiece2P1
            nextPiece2P1 = nextPiece3P1
            nextPiece3P1 = nextPiece4P1
            nextPiece4P1 = nextPiece5P1

            nextPiece5P1 = getNewPieceP1(bagP1)
            bagP1.remove(nextPiece5P1['shape'])
            NEXT_PIECESP1 = [nextPiece1P1,nextPiece2P1,nextPiece3P1,nextPiece4P1,nextPiece5P1]
            lastFallTime = time.time() # reset lastFallTime

            if not isValidPosition(boardP1, fallingPieceP1):
                fallingPieceP1['y'] = 18
                if not isValidPosition(boardP1, fallingPieceP1):
                    loseP1 = True
                    for x in range(BOARDWIDTH):
                        for y in range(BOARDHEIGHT):
                            drawBoxP1(x, y, boardP1[x][y])
                    drawHiddenBoardP1()
                    return # can't fit a new piece on the board, so game over

        if fallingPieceP2 == None:
            # No falling piece in play, so start a new piece at the top
            fallingPieceP2 = nextPiece1P2
            if len(bagP2) == 0:
                bagP2 = list(PIECES.keys())
            
            nextPiece1P2 = nextPiece2P2
            nextPiece2P2 = nextPiece3P2
            nextPiece3P2 = nextPiece4P2
            nextPiece4P2 = nextPiece5P2

            nextPiece5P2 = getNewPieceP2(bagP2)
            bagP2.remove(nextPiece5P2['shape'])
            NEXT_PIECESP2 = [nextPiece1P2,nextPiece2P2,nextPiece3P2,nextPiece4P2,nextPiece5P2]
            lastFallTime = time.time() # reset lastFallTime

            if not isValidPosition(boardP2, fallingPieceP2):
                fallingPieceP2['y'] = 18
                if not isValidPosition(boardP2, fallingPieceP2):
                    loseP2 = True
                    for x in range(BOARDWIDTH):
                        for y in range(BOARDHEIGHT):
                            drawBoxP2(x, y, boardP2[x][y])
                    drawHiddenBoardP2()
                    return # can't fit a new piece on the board, so game over


        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == KEYUP:
                if (event.key == K_TAB):
                    #quit the game
                    terminate()
                elif (event.key == K_f):
                    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.FULLSCREEN)
                    DISPLAYSURF.fill(BGCOLOR)
                    showTextScreen('Paused') # pause until a key press
                    lastFallTimeP1 = time.time() + DELAYLOCKIN - fallFreq
                    lastMoveDownTimeP1 = time.time()
                    lastMoveSidewaysTimeP1 = time.time()
                    lastFallTimeP2 = time.time() + DELAYLOCKIN - fallFreq
                    lastMoveDownTimeP2 = time.time()
                    lastMoveSidewaysTimeP2 = time.time()
                elif (event.key == K_g):
                    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
                    DISPLAYSURF.fill(BGCOLOR)
                    showTextScreen('Paused') # pause until a key press
                    lastFallTimeP1 = time.time() + DELAYLOCKIN - fallFreq
                    lastMoveDownTimeP1 = time.time()
                    lastMoveSidewaysTimeP1 = time.time()
                    lastFallTimeP2 = time.time() + DELAYLOCKIN - fallFreq
                    lastMoveDownTimeP2 = time.time()
                    lastMoveSidewaysTimeP2 = time.time()
                elif (event.key == K_r):
                    #reset the game
                    return
                elif (event.key == K_h):
                    DISPLAYSURF.fill(BGCOLOR)
                    drawInstructions(WINDOWWIDTH/2 - 100, 200, WHITE)
                    titleSurf, titleRect = makeTextObjs('Instructions', BIGFONT, TEXTCOLOR)
                    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) - 200)
                    DISPLAYSURF.blit(titleSurf, titleRect)

                    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
                    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 200)
                    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

                    while checkForKeyPress() == None:
                        pygame.display.update()
                        FPSCLOCK.tick()
                elif (event.key == K_p):
                    # Pausing the game
                    DISPLAYSURF.fill(BGCOLOR)
                    showTextScreen('Paused') # pause until a key press
                    lastFallTimeP1 = time.time() + DELAYLOCKIN - fallFreq
                    lastMoveDownTimeP1 = time.time()
                    lastMoveSidewaysTimeP1 = time.time()

                    lastFallTimeP2 = time.time() + DELAYLOCKIN - fallFreq
                    lastMoveDownTimeP2 = time.time()
                    lastMoveSidewaysTimeP2 = time.time()

                elif (event.key == K_LEFT):
                    movingLeftP1 = False
                elif (event.key == K_RIGHT):
                    movingRightP1 = False
                elif (event.key == K_DOWN):
                    movingDownP1 = False
                elif (event.key == K_j):
                    movingLeftP2 = False
                elif (event.key == K_l):
                    movingRightP2 = False
                elif (event.key == K_k):
                    movingDownP2 = False

            if event.type == KEYDOWN:
                # moving the piece sideways
                if (event.key == K_LEFT) and fallingPieceP1 != None:
                    movingRightP1 = False
                    movingLeftP1 = True
                    if isValidPosition(boardP1, fallingPieceP1, adjX=-1):
                        fallingPieceP1['x'] -= 1
                        lastMoveSidewaysTimeP1 = time.time() + DELAYAUTOSHIFT
                        if not isValidPosition(boardP1, fallingPieceP1, adjY=1):
                            lastFallTimeP1 = time.time() + DELAYLOCKIN - fallFreq

                elif (event.key == K_RIGHT) and fallingPieceP1 != None:
                    movingLeftP1 = False
                    movingRightP1 = True
                    if isValidPosition(boardP1, fallingPieceP1, adjX=1):
                        fallingPieceP1['x'] += 1
                        lastMoveSidewaysTimeP1 = time.time() + DELAYAUTOSHIFT
                        if not isValidPosition(boardP1, fallingPieceP1, adjY=1):
                            lastFallTimeP1 = time.time() + DELAYLOCKIN - fallFreq
                    
                elif (event.key == K_j) and fallingPieceP2 != None:
                    movingRightP2 = False
                    movingLeftP2 = True
                    if isValidPosition(boardP2, fallingPieceP2, adjX=-1):
                        fallingPieceP2['x'] -= 1
                        lastMoveSidewaysTimeP2 = time.time() + DELAYAUTOSHIFT
                        if not isValidPosition(boardP2, fallingPieceP2, adjY=1):
                            lastFallTimeP2 = time.time() + DELAYLOCKIN - fallFreq


                elif (event.key == K_l) and fallingPieceP2 != None:
                    movingLeftP2 = False
                    movingRightP2 = True
                    if isValidPosition(boardP2, fallingPieceP2, adjX=1):
                        fallingPieceP2['x'] += 1
                        lastMoveSidewaysTimeP2 = time.time() + DELAYAUTOSHIFT
                        if not isValidPosition(boardP2, fallingPieceP2, adjY=1):
                            lastFallTimeP2 = time.time() + DELAYLOCKIN - fallFreq

                # hold a peice
                elif (event.key == K_e) and canHoldedP1 and fallingPieceP1 != None:
                    lastMoveSidewaysTimeP1 = time.time() + DELAYAUTOSHIFT
                    copyPieceP1 = holdPieceP1
                    holdPieceP1 = fallingPieceP1
                    fallingPieceP1 = copyPieceP1
                    holdPieceP1['x'] = int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2) 
                    holdPieceP1['rotation'] = 0
                    canHoldedP1 = False
                    if fallingPieceP1 != None:
                        fallingPieceP1['y'] = 19
                        if not isValidPosition(boardP1, fallingPieceP1):
                            fallingPieceP1['y'] = 18
                    
                elif (event.key == K_3) and canHoldedP2 and fallingPieceP2 != None:
                    lastMoveSidewaysTimeP2 = time.time() + DELAYAUTOSHIFT
                    copyPieceP2 = holdPieceP2
                    holdPieceP2 = fallingPieceP2
                    fallingPieceP2 = copyPieceP2
                    holdPieceP2['x'] = int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2) 
                    holdPieceP2['rotation'] = 0
                    canHoldedP2 = False
                    if fallingPieceP2 != None:
                        fallingPieceP2['y'] = 19
                        if not isValidPosition(boardP2, fallingPieceP2):
                            fallingPieceP2['y'] = 18

                # rotating the piece (if there is room to rotate)
                elif (event.key == K_UP) and fallingPieceP1 != None:
                    P1Tspin = False
                    if not isValidPosition(boardP1, fallingPieceP1, adjY=1):
                        lastFallTimeP1 = time.time() + DELAYLOCKIN - fallFreq
                    spinDirectionP1 = 'CW'
                    fallingPieceP1['rotation'] = (fallingPieceP1['rotation'] + 1) % len(PIECES[fallingPieceP1['shape']])
                    if fallingPieceP1['shape'] == 'T':
                        if isValidPosition(boardP1, fallingPieceP1) and not isValidPosition(boardP1, fallingPieceP1, adjY=-1) and is3ConnerRule(boardP1, fallingPieceP1):
                            P1Tspin = True
                        elif not isValidPosition(boardP1, fallingPieceP1):
                            superRotationSystem(boardP1, fallingPieceP1, spinDirectionP1)
                            if is3ConnerRule(boardP1, fallingPieceP1):
                                P1Tspin = True
                    else:
                        superRotationSystem(boardP1, fallingPieceP1, spinDirectionP1)
                elif (event.key == K_w) and fallingPieceP1 != None: # rotate the other direction
                    P1Tspin = False
                    if not isValidPosition(boardP1, fallingPieceP1, adjY=1):
                        lastFallTimeP1 = time.time() + DELAYLOCKIN - fallFreq
                    spinDirectionP1 = 'CCW'
                    fallingPieceP1['rotation'] = (fallingPieceP1['rotation'] - 1) % len(PIECES[fallingPieceP1['shape']])
                    if fallingPieceP1['shape'] == 'T':
                        if isValidPosition(boardP1, fallingPieceP1) and not isValidPosition(boardP1, fallingPieceP1, adjY=-1) and is3ConnerRule(boardP1, fallingPieceP1):
                            P1Tspin = True
                        elif not isValidPosition(boardP1, fallingPieceP1):
                            superRotationSystem(boardP1, fallingPieceP1, spinDirectionP1)
                            if is3ConnerRule(boardP1, fallingPieceP1):
                                P1Tspin = True
                    else:
                        superRotationSystem(boardP1, fallingPieceP1, spinDirectionP1)
                elif (event.key == K_q) and fallingPieceP1 != None: # rotate the other direction
                    if not isValidPosition(boardP1, fallingPieceP1, adjY=1):
                        lastFallTimeP1 = time.time() + DELAYLOCKIN - fallFreq
                    fallingPieceP1['rotation'] = (fallingPieceP1['rotation'] + 2) % len(PIECES[fallingPieceP1['shape']])
                    if not isValidPosition(boardP1, fallingPieceP1):
                        fallingPieceP1['rotation'] = (fallingPieceP1['rotation'] - 2) % len(PIECES[fallingPieceP1['shape']])

                elif (event.key == K_i) and fallingPieceP2 != None:
                    P2Tspin = False
                    if not isValidPosition(boardP2, fallingPieceP2, adjY=1):
                        lastFallTimeP2 = time.time() + DELAYLOCKIN - fallFreq
                    spinDirectionP2 = 'CW'
                    fallingPieceP2['rotation'] = (fallingPieceP2['rotation'] + 1) % len(PIECES[fallingPieceP2['shape']])
                    if fallingPieceP2['shape'] == 'T':
                        if isValidPosition(boardP2, fallingPieceP2) and not isValidPosition(boardP2, fallingPieceP2, adjY=-1) and is3ConnerRule(boardP2, fallingPieceP2):
                            P2Tspin = True
                        elif not isValidPosition(boardP2, fallingPieceP2):
                            superRotationSystem(boardP2, fallingPieceP2, spinDirectionP2)
                            if is3ConnerRule(boardP2, fallingPieceP2):
                                P2Tspin = True
                    else:
                        superRotationSystem(boardP2, fallingPieceP2, spinDirectionP2)
                elif (event.key == K_2) and fallingPieceP2 != None: # rotate the other direction
                    P2Tspin = False
                    if not isValidPosition(boardP2, fallingPieceP2, adjY=1):
                        lastFallTimeP2 = time.time() + DELAYLOCKIN - fallFreq
                    spinDirectionP2 = 'CCW'
                    fallingPieceP2['rotation'] = (fallingPieceP2['rotation'] - 1) % len(PIECES[fallingPieceP2['shape']])
                    if fallingPieceP2['shape'] == 'T':
                        if isValidPosition(boardP2, fallingPieceP2) and not isValidPosition(boardP2, fallingPieceP2, adjY=-1) and is3ConnerRule(boardP2, fallingPieceP2):
                            P2Tspin = True
                        elif not isValidPosition(boardP2, fallingPieceP2):
                            superRotationSystem(boardP2, fallingPieceP2, spinDirectionP2)
                            if is3ConnerRule(boardP2, fallingPieceP2):
                                P2Tspin = True
                    else:
                        superRotationSystem(boardP2, fallingPieceP2, spinDirectionP2)
                elif (event.key == K_1) and fallingPieceP2 != None: # rotate the other direction
                    if not isValidPosition(boardP2, fallingPieceP2, adjY=1):
                        lastFallTimeP2 = time.time() + DELAYLOCKIN - fallFreq
                    fallingPieceP2['rotation'] = (fallingPieceP2['rotation'] + 2) % len(PIECES[fallingPieceP2['shape']])
                    if not isValidPosition(boardP2, fallingPieceP2):
                        fallingPieceP2['rotation'] = (fallingPieceP2['rotation'] - 2) % len(PIECES[fallingPieceP2['shape']])


                # making the piece fall faster with the down key
                elif (event.key == K_DOWN) and fallingPieceP1 != None:
                    movingDownP1 = True
                    if isValidPosition(boardP1, fallingPieceP1, adjY=2):
                        fallingPieceP1['y'] += 2
                    elif isValidPosition(boardP1, fallingPieceP1, adjY=1):
                        fallingPieceP1['y'] += 1
                    lastMoveDownTimeP1 = time.time()

                elif (event.key == K_k) and fallingPieceP2 != None:
                    movingDownP2 = True
                    if isValidPosition(boardP2, fallingPieceP2, adjY=2):
                        fallingPieceP2['y'] += 2
                    elif isValidPosition(boardP2, fallingPieceP2, adjY=1):
                        fallingPieceP2['y'] += 1
                    lastMoveDownTimeP2 = time.time()

                # move the current piece all the way down
                elif event.key == K_SPACE and fallingPieceP1 != None:
                    while isValidPosition(boardP1, fallingPieceP1, adjY=1):
                        fallingPieceP1['y'] += 1
                    addToBoard(boardP1, fallingPieceP1)
                    lineSentToP2, P1backToBack, P1ComboCounter, P1LineRemoved, P1PerfectClear, P1backToBackPrint, P1Tetris, P1Combo, P1TMini, P1TSingle, P1TDouble, P1TTriple = sendLineFromP1(boardP1, removeCompleteLines(boardP1), P1Tspin, P1backToBack, P1ComboCounter, P1PerfectClear, P1backToBackPrint, P1Tetris, P1Combo, P1TMini, P1TSingle, P1TDouble, P1TTriple)
                    if P1LineRemoved == 0:
                        for line in garbageQueueForP1:
                            reciveGarbage(boardP1, line)
                        garbageQueueForP1 = []
                    else:
                        while lineSentToP2 > 0 and garbageQueueForP1 != []:
                            for line in garbageQueueForP1:
                                if lineSentToP2 >= line:
                                    lineSentToP2 -= line
                                    garbageQueueForP1.pop(0)
                                elif lineSentToP2 < line:
                                    garbageQueueForP1[0] -= lineSentToP2
                                    lineSentToP2 = 0
                        if lineSentToP2 > 0:
                            garbageQueueForP2.append(lineSentToP2)
                    P1Tspin = False
                    canHoldedP1 = True
                    if P1PerfectClear:
                        P1PCTimer = time.time()
                    if P1backToBackPrint:
                        P1B2BTimer = time.time()
                    if P1Tetris:
                        P1TetrisTimer = time.time()
                    if P1Combo:
                        P1ComboTimer = time.time()
                    if P1TMini:
                        P1TMiniTimer = time.time()
                    if P1TSingle:
                        P1TSingleTimer = time.time()
                    if P1TDouble:
                        P1TDoubleTimer = time.time()
                    if P1TTriple:
                        P1TTripleTimer = time.time()

                    fallingPieceP1 = nextPiece1P1
                    if len(bagP1) == 0:
                        bagP1 = list(PIECES.keys())
                    
                    nextPiece1P1 = nextPiece2P1
                    nextPiece2P1 = nextPiece3P1
                    nextPiece3P1 = nextPiece4P1
                    nextPiece4P1 = nextPiece5P1
                    nextPiece5P1 = getNewPieceP1(bagP1)
                    bagP1.remove(nextPiece5P1['shape'])

                    NEXT_PIECESP1 = [nextPiece1P1,nextPiece2P1,nextPiece3P1,nextPiece4P1,nextPiece5P1]
                    lastFallTimeP1 = time.time() # reset lastFallTime

                    if not isValidPosition(boardP1, fallingPieceP1):
                        fallingPieceP1['y'] = 18
                        if not isValidPosition(boardP1, fallingPieceP1):
                            loseP1 = True
                            for x in range(BOARDWIDTH):
                                for y in range(BOARDHEIGHT):
                                    drawBoxP1(x, y, boardP1[x][y])
                            drawHiddenBoardP1()
                            return # can't fit a new piece on the board, so game over

                elif event.key == K_v and fallingPieceP2 != None:
                    while isValidPosition(boardP2, fallingPieceP2, adjY=1):
                        fallingPieceP2['y'] += 1
                    addToBoard(boardP2, fallingPieceP2)
                    lineSentToP1, P2backToBack, P2ComboCounter, P2LineRemoved, P2PerfectClear, P2backToBackPrint, P2Tetris, P2Combo, P2TMini, P2TSingle, P2TDouble, P2TTriple = sendLineFromP2(boardP2, removeCompleteLines(boardP2), P2Tspin, P2backToBack, P2ComboCounter, P2PerfectClear, P2backToBackPrint, P2Tetris, P2Combo, P2TMini, P2TSingle, P2TDouble, P2TTriple)
                    if P2LineRemoved == 0:
                        for line in garbageQueueForP2:
                            reciveGarbage(boardP2, line)
                        garbageQueueForP2 = []
                    else:
                        while lineSentToP1 > 0 and garbageQueueForP2 != []:
                            for line in garbageQueueForP2:
                                if lineSentToP1 >= line:
                                    lineSentToP1 -= line
                                    garbageQueueForP2.pop(0)
                                elif lineSentToP1 < line:
                                    garbageQueueForP2[0] -= lineSentToP1
                                    lineSentToP1 = 0
                        if lineSentToP1 > 0:
                            garbageQueueForP1.append(lineSentToP1)
                    P2Tspin = False
                    canHoldedP2 = True
                    if P2PerfectClear:
                        P2PCTimer = time.time()
                    if P2backToBackPrint:
                        P2B2BTimer = time.time()
                    if P2Tetris:
                        P2TetrisTimer = time.time()
                    if P2Combo:
                        P2ComboTimer = time.time()
                    if P2TMini:
                        P2TMiniTimer = time.time()
                    if P2TSingle:
                        P2TSingleTimer = time.time()
                    if P2TDouble:
                        P2TDoubleTimer = time.time()
                    if P2TTriple:
                        P2TTripleTimer = time.time()

                    fallingPieceP2 = nextPiece1P2
                    if len(bagP2) == 0:
                        bagP2 = list(PIECES.keys())
                    
                    nextPiece1P2 = nextPiece2P2
                    nextPiece2P2 = nextPiece3P2
                    nextPiece3P2 = nextPiece4P2
                    nextPiece4P2 = nextPiece5P2
                    nextPiece5P2 = getNewPieceP2(bagP2)
                    bagP2.remove(nextPiece5P2['shape'])

                    NEXT_PIECESP2 = [nextPiece1P2,nextPiece2P2,nextPiece3P2,nextPiece4P2,nextPiece5P2]
                    lastFallTimeP2 = time.time() # reset lastFallTime

                    if not isValidPosition(boardP2, fallingPieceP2):
                        fallingPieceP2['y'] = 18
                        if not isValidPosition(boardP2, fallingPieceP2):
                            loseP2 = True
                            for x in range(BOARDWIDTH):
                                for y in range(BOARDHEIGHT):
                                    drawBoxP2(x, y, boardP2[x][y])
                            drawHiddenBoardP2()
                            return # can't fit a new piece on the board, so game over    
                
        # handle moving the piece because of user input
        if (movingLeftP1 or movingRightP1) and time.time() - lastMoveSidewaysTimeP1 > AUTOREPEATRATE and fallingPieceP1 != None:
            if movingLeftP1 and isValidPosition(boardP1, fallingPieceP1, adjX=-1):
                fallingPieceP1['x'] -= 1
            elif movingRightP1 and isValidPosition(boardP1, fallingPieceP1, adjX=1):
                fallingPieceP1['x'] += 1
            lastMoveSidewaysTimeP1 = time.time()
        
        if (movingLeftP2 or movingRightP2) and time.time() - lastMoveSidewaysTimeP2 > AUTOREPEATRATE and fallingPieceP2 != None:
            if movingLeftP2 and isValidPosition(boardP2, fallingPieceP2, adjX=-1):
                fallingPieceP2['x'] -= 1
            elif movingRightP2 and isValidPosition(boardP2, fallingPieceP2, adjX=1):
                fallingPieceP2['x'] += 1
            lastMoveSidewaysTimeP2 = time.time()

        if movingDownP1 and time.time() - lastMoveDownTimeP1 > MOVEDOWNFREQ and isValidPosition(boardP1, fallingPieceP1, adjY=1) and fallingPieceP1 != None:
            fallingPieceP1['y'] += 1
            lastMoveDownTimeP1 = time.time()
            lastFallTimeP1 = time.time() + DELAYLOCKIN - fallFreq

        if movingDownP2 and time.time() - lastMoveDownTimeP2 > MOVEDOWNFREQ and isValidPosition(boardP2, fallingPieceP2, adjY=1) and fallingPieceP2 != None:
            fallingPieceP2['y'] += 1
            lastMoveDownTimeP2 = time.time()
            lastFallTimeP2 = time.time() + DELAYLOCKIN - fallFreq

        # let the piece fall if it is time to fall
        if time.time() - lastFallTimeP1 > fallFreq:
            # see if the piece has landed
            if not isValidPosition(boardP1, fallingPieceP1, adjY=1):
                # falling piece has landed, set it on the board
                addToBoard(boardP1, fallingPieceP1)
                lineSentToP2, P1backToBack, P1ComboCounter, P1LineRemoved, P1PerfectClear, P1backToBackPrint, P1Tetris, P1Combo, P1TMini, P1TSingle, P1TDouble, P1TTriple = sendLineFromP1(boardP1, removeCompleteLines(boardP1), P1Tspin, P1backToBack, P1ComboCounter, P1PerfectClear, P1backToBackPrint, P1Tetris, P1Combo, P1TMini, P1TSingle, P1TDouble, P1TTriple)
                if P1LineRemoved == 0:
                    for line in garbageQueueForP1:
                        reciveGarbage(boardP1, line)
                    garbageQueueForP1 = []
                else:
                    while lineSentToP2 > 0 and garbageQueueForP1 != []:
                        for line in garbageQueueForP1:
                            if lineSentToP2 >= line:
                                lineSentToP2 -= line
                                garbageQueueForP1.pop(0)
                            elif lineSentToP2 < line:
                                garbageQueueForP1[0] -= lineSentToP2
                                lineSentToP2 = 0
                    if lineSentToP2 > 0:
                        garbageQueueForP2.append(lineSentToP2)
                P1Tspin = False
                canHoldedP1 = True
                if P1PerfectClear:
                    P1PCTimer = time.time()
                if P1backToBackPrint:
                    P1B2BTimer = time.time()
                if P1Tetris:
                    P1TetrisTimer = time.time()
                if P1Combo:
                    P1ComboTimer = time.time()
                if P1TMini:
                    P1TMiniTimer = time.time()
                if P1TSingle:
                    P1TSingleTimer = time.time()
                if P1TDouble:
                    P1TDoubleTimer = time.time()
                if P1TTriple:
                    P1TTripleTimer = time.time()
            
                # No falling piece in play, so start a new piece at the top
                fallingPieceP1 = nextPiece1P1
                if len(bagP1) == 0:
                    bagP1 = list(PIECES.keys())
                
                nextPiece1P1 = nextPiece2P1
                nextPiece2P1 = nextPiece3P1
                nextPiece3P1 = nextPiece4P1
                nextPiece4P1 = nextPiece5P1

                nextPiece5P1 = getNewPieceP1(bagP1)
                bagP1.remove(nextPiece5P1['shape'])
                NEXT_PIECESP1 = [nextPiece1P1,nextPiece2P1,nextPiece3P1,nextPiece4P1,nextPiece5P1]
                lastFallTime = time.time() # reset lastFallTime

                if not isValidPosition(boardP1, fallingPieceP1):
                    fallingPieceP1['y'] = 18
                    if not isValidPosition(boardP1, fallingPieceP1):
                        loseP1 = True
                        for x in range(BOARDWIDTH):
                            for y in range(BOARDHEIGHT):
                                drawBoxP1(x, y, boardP1[x][y])
                        drawHiddenBoardP1()
                        return # can't fit a new piece on the board, so game over
            else:
                # piece did not land, just move the piece down
                fallingPieceP1['y'] += 1
                lastFallTimeP1 = time.time()

        if time.time() - lastFallTimeP2 > fallFreq:
            # see if the piece has landed
            if not isValidPosition(boardP2, fallingPieceP2, adjY=1):
                # falling piece has landed, set it on the board
                addToBoard(boardP2, fallingPieceP2)
                lineSentToP1, P2backToBack, P2ComboCounter, P2LineRemoved, P2PerfectClear, P2backToBackPrint, P2Tetris, P2Combo, P2TMini, P2TSingle, P2TDouble, P2TTriple = sendLineFromP2(boardP2, removeCompleteLines(boardP2), P2Tspin, P2backToBack, P2ComboCounter, P2PerfectClear, P2backToBackPrint, P2Tetris, P2Combo, P2TMini, P2TSingle, P2TDouble, P2TTriple)
                if P2LineRemoved == 0:
                    for line in garbageQueueForP2:
                        reciveGarbage(boardP2, line)
                    garbageQueueForP2 = []
                else:
                    while lineSentToP1 > 0 and garbageQueueForP2 != []:
                        for line in garbageQueueForP2:
                            if lineSentToP1 >= line:
                                lineSentToP1 -= line
                                garbageQueueForP2.pop(0)
                            elif lineSentToP1 < line:
                                garbageQueueForP2[0] -= lineSentToP1
                                lineSentToP1 = 0
                    if lineSentToP1 > 0:
                        garbageQueueForP1.append(lineSentToP1)
                P2Tspin = False
                canHoldedP2 = True
                if P2PerfectClear:
                    P2PCTimer = time.time()
                if P2backToBackPrint:
                    P2B2BTimer = time.time()
                if P2Tetris:
                    P2TetrisTimer = time.time()
                if P2Combo:
                    P2ComboTimer = time.time()
                if P2TMini:
                    P2TMiniTimer = time.time()
                if P2TSingle:
                    P2TSingleTimer = time.time()
                if P2TDouble:
                    P2TDoubleTimer = time.time()
                if P2TTriple:
                    P2TTripleTimer = time.time()

                # No falling piece in play, so start a new piece at the top
                fallingPieceP2 = nextPiece1P2
                if len(bagP2) == 0:
                    bagP2 = list(PIECES.keys())
                
                nextPiece1P2 = nextPiece2P2
                nextPiece2P2 = nextPiece3P2
                nextPiece3P2 = nextPiece4P2
                nextPiece4P2 = nextPiece5P2

                nextPiece5P2 = getNewPieceP2(bagP2)
                bagP2.remove(nextPiece5P2['shape'])
                NEXT_PIECESP2 = [nextPiece1P2,nextPiece2P2,nextPiece3P2,nextPiece4P2,nextPiece5P2]
                lastFallTime = time.time() # reset lastFallTime

                if not isValidPosition(boardP2, fallingPieceP2):
                    fallingPieceP2['y'] = 18
                    if not isValidPosition(boardP2, fallingPieceP2):
                        loseP2 = True
                        for x in range(BOARDWIDTH):
                            for y in range(BOARDHEIGHT):
                                drawBoxP2(x, y, boardP2[x][y])
                        drawHiddenBoardP2()
                        return # can't fit a new piece on the board, so game over
            else:
                # piece did not land, just move the piece down
                fallingPieceP2['y'] += 1
                lastFallTimeP2 = time.time()

        # drawing everything on the screen
        DISPLAYSURF.fill(BGCOLOR)
        drawBoardP1(boardP1)
        drawBoardP2(boardP2)
        drawNextPieceP1(NEXT_PIECESP1)
        drawHoldPieceP1(holdPieceP1)
        drawNextPieceP2(NEXT_PIECESP2)
        drawHoldPieceP2(holdPieceP2)
        drawText('Press h for help', 20, 20, WHITE)
        if fallingPieceP1 != None:
            drawPieceP1(GhostPiece(fallingPieceP1, boardP1))
            drawPieceP1(fallingPieceP1)
        if fallingPieceP2 != None:
            drawPieceP2(GhostPiece(fallingPieceP2, boardP2))
            drawPieceP2(fallingPieceP2)
        drawAleartBarP1(sum(garbageQueueForP1))
        drawAleartBarP2(sum(garbageQueueForP2))
        drawHiddenBoardP1()
        drawHiddenBoardP2()

        drawSpecialMove(60, 300, P1ComboCounter, P1Tspin, P1backToBackPrint, boardP1, P1Tetris, P1PerfectClear, P1Combo, P1TMini, P1TSingle, P1TDouble, P1TTriple)
        drawSpecialMove(660, 300, P2ComboCounter, P2Tspin, P2backToBackPrint, boardP2, P2Tetris, P2PerfectClear, P2Combo, P2TMini, P2TSingle, P2TDouble, P2TTriple)

        if P1PerfectClear:
            if time.time() - P1PCTimer > 1:
                P1PerfectClear = False

        if P2PerfectClear:
            if time.time() - P2PCTimer > 1:
                P2PerfectClear = False

        if P1backToBackPrint:
            if time.time() - P1B2BTimer > 1:
                P1backToBackPrint = False

        if P2backToBackPrint:
            if time.time() - P2B2BTimer > 1:
                P2backToBackPrint = False

        if P1Tetris:
            if time.time() - P1TetrisTimer > 1:
                P1Tetris = False

        if P2Tetris:
            if time.time() - P2TetrisTimer > 1:
                P2Tetris = False

        if P1Combo:
            if time.time() - P1ComboTimer > 1:
                P1Combo = False

        if P2Combo:
            if time.time() - P2ComboTimer > 1:
                P2Combo = False

        if P1TMini:
            if time.time() - P1TMiniTimer > 1:
                P1TMini = False

        if P2TMini:
            if time.time() - P2TMiniTimer > 1:
                P2TMini = False

        if P1TSingle:
            if time.time() - P1TSingleTimer > 1:
                P1TSingle = False

        if P2TSingle:
            if time.time() - P2TSingleTimer > 1:
                P2TSingle = False

        if P1TDouble:
            if time.time() - P1TDoubleTimer > 1:
                P1TDouble = False

        if P2TDouble:
            if time.time() - P2TDoubleTimer > 1:
                P2TDouble = False

        if P1TTriple:
            if time.time() - P1TTripleTimer > 1:
                P1TTriple = False

        if P2TTriple:
            if time.time() - P2TTripleTimer > 1:
                P2TTriple = False
                
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def terminate():
    pygame.quit()
    sys.exit()


def checkForKeyPress():
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def showTextScreen(text):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text drop shadow

    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back


def getNewPieceP1(bag):
    # return a random new piece in a random rotation and color
    if len(bag) == 0:
        bag = list(PIECES.keys())
    shape = bag[random.randrange(len(bag))]
    newPiece = {'shape': shape,
                'rotation': 0,
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': 19, # start it above the board (i.e. less than 0)
                'color': PIECES_COLOR[shape]}
    return newPiece


def getNewPieceP2(bag):
    # return a random new piece in a random rotation and color
    if len(bag) == 0:
        bag = list(PIECES.keys())
    shape = bag[random.randrange(len(bag))]
    newPiece = {'shape': shape,
                'rotation': 0,
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': 19, # start it above the board (i.e. less than 0)
                'color': PIECES_COLOR[shape]}
    return newPiece


def addToBoard(board, piece):
    # fill in the board based on piece's location, shape, and rotation
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if piece!=None and PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']


def getBlankBoard():
    # create and return a new blank board data structure
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * (BOARDHEIGHT))
    return board

 
def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT
 

def isValidPosition(board, piece, adjX=0, adjY=0):
    # Return True if the piece is within the board and not colliding
    if piece == None:
        return False
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
    return True


def is3ConnerRule(board, piece, adjX=0, adjY=0):
    count = 0 
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if ((x==0 and y==0) or (x==0 and y==2) or (x==2 and y==0) or (x==2 and y==2)):
                if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                    count += 1
                elif board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                    count += 1
    if count >= 3:
        return True
    else:
        return False
    

def superRotationSystem(board, fallingPiece, spinDirection):
    set1 = ['J', 'L', 'S', 'T', 'Z']
    set2 = ['I']

    rotationAndDirection = [(fallingPiece['rotation'] == 1 and spinDirection == 'CW'),
                            (fallingPiece['rotation'] == 0 and spinDirection == 'CCW'),                
                            (fallingPiece['rotation'] == 2 and spinDirection == 'CW'),
                            (fallingPiece['rotation'] == 1 and spinDirection == 'CCW'),
                            (fallingPiece['rotation'] == 3 and spinDirection == 'CW'),
                            (fallingPiece['rotation'] == 2 and spinDirection == 'CCW'),
                            (fallingPiece['rotation'] == 0 and spinDirection == 'CW'),
                            (fallingPiece['rotation'] == 3 and spinDirection == 'CCW')]

    if fallingPiece['shape'] in set1 and not isValidPosition(board, fallingPiece):
        for comindex, combination in enumerate(rotationAndDirection):
            if combination:
                for testx, testy in set1WallkickData[comindex]:
                    fallingPiece['x'] += testx 
                    fallingPiece['y'] -= testy
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['x'] -= testx 
                        fallingPiece['y'] += testy
                    else:
                        return
    if fallingPiece['shape'] in set2 and not isValidPosition(board, fallingPiece):
        for index, combination in enumerate(rotationAndDirection):
            if combination:
                for testx, testy in set2WallkickData[index]:
                    fallingPiece['x'] += testx 
                    fallingPiece['y'] -= testy
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['x'] -= testx 
                        fallingPiece['y'] += testy
                    else:
                        return
    if not isValidPosition(board, fallingPiece): 
        if spinDirection == 'CW':
            fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
        elif spinDirection == 'CCW':
            fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])


def isCompleteLine(board, y):
    # Return True if the line filled with boxes with no gaps
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    return True


def removeCompleteLines(board):
    # Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
    numLinesRemoved = 0
    y = BOARDHEIGHT - 1 # start y at the bottom of the board
    while y >= 0:
        if isCompleteLine(board, y):
            # Remove the line and pull boxes down by one line.
            for pullDownY in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY-1]
            # Set very top line to blank.
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            numLinesRemoved += 1
            # Note on the next iteration of the loop, y is the same.
            # This is so that if the line that was pulled down is also
            # complete, it will be removed.
        else:
            y -= 1 # move on to check next row up
    return numLinesRemoved


def reciveGarbage(board, line):
    y = 0
    counter = 0
    garbageHole = random.randrange(10)
    while counter < line:
        for pushUpY in range(y, BOARDHEIGHT - 1):
            for x in range(BOARDWIDTH):
                board[x][pushUpY] = board[x][pushUpY + 1]
        for x in range(BOARDWIDTH):
            if x == garbageHole:    
                board[x][BOARDHEIGHT - 1] = BLANK
            else:
                board[x][BOARDHEIGHT - 1] = 15
        counter += 1


def sendLineFromP1(board, numLinesRemoved, P1Tspin, P1backToBack, P1ComboCounter, P1PerfectClear, P1backToBackPrint, P1Tetris, P1Combo, P1TMini, P1TSingle, P1TDouble, P1TTriple):
    blankBoard = getBlankBoard()
    lineSent = 0

    if not P1Tspin:
        if numLinesRemoved == 0:
            lineSent += ATTACKTABLE[0]
        if numLinesRemoved == 1:
            P1backToBack = False
            lineSent += ATTACKTABLE[1]
        elif numLinesRemoved == 2:
            P1backToBack = False
            lineSent += ATTACKTABLE[2]
        elif numLinesRemoved == 3:
            P1backToBack = False
            lineSent += ATTACKTABLE[3]
        elif numLinesRemoved == 4:
            P1Tetris = True
            if P1backToBack:
                P1backToBackPrint = True
                lineSent += ATTACKTABLE[10]
            lineSent += ATTACKTABLE[4]
            P1backToBack = True
    else:
        if P1backToBack:
            P1backToBackPrint = True
            lineSent += ATTACKTABLE[10]
        P1backToBack = True
        if numLinesRemoved == 0:
            P1TMini = True
            lineSent += ATTACKTABLE[8]
        elif numLinesRemoved == 1:
            P1TSingle = True
            lineSent += ATTACKTABLE[7]
        elif numLinesRemoved == 2:
            P1TDouble = True
            lineSent += ATTACKTABLE[5]
        elif numLinesRemoved == 3:
            P1TTriple = True
            lineSent += ATTACKTABLE[6]

    if blankBoard == board:
        P1PerfectClear = True
        lineSent += ATTACKTABLE[9]
        
    if numLinesRemoved > 0:
        P1Combo = True
        P1ComboCounter += 1
        if P1ComboCounter <= 12:
            lineSent += COMBOTABLE[P1ComboCounter - 1]
        else: 
            lineSent += COMBOTABLE[12]
    else:
        P1ComboCounter = 0
    
    return lineSent, P1backToBack, P1ComboCounter, numLinesRemoved, P1PerfectClear, P1backToBackPrint, P1Tetris, P1Combo, P1TMini, P1TSingle, P1TDouble, P1TTriple


def sendLineFromP2(board, numLinesRemoved, P2Tspin, P2backToBack, P2ComboCounter, P2PerfectClear, P2backToBackPrint, P2Tetris, P2Combo, P2TMini, P2TSingle, P2TDouble, P2TTriple):
    blankBoard = getBlankBoard()
    lineSent = 0

    if not P2Tspin:
        if numLinesRemoved == 0:
            lineSent += ATTACKTABLE[0]
        if numLinesRemoved == 1:
            P2backToBack = False
            lineSent += ATTACKTABLE[1]
        elif numLinesRemoved == 2:
            P2backToBack = False
            lineSent += ATTACKTABLE[2]
        elif numLinesRemoved == 3:
            P2backToBack = False
            lineSent += ATTACKTABLE[3]
        elif numLinesRemoved == 4:
            P2Tetris = True
            if P2backToBack:
                P2backToBackPrint = True
                lineSent += ATTACKTABLE[10]
            lineSent += ATTACKTABLE[4]
            P2backToBack = True
    else:
        if P2backToBack:
            P2backToBackPrint = True
            lineSent += ATTACKTABLE[10]
        P2backToBack = True
        if numLinesRemoved == 0:
            P2TMini = True
            lineSent += ATTACKTABLE[8]
        elif numLinesRemoved == 1:
            P2TSingle = True
            lineSent += ATTACKTABLE[7]
        elif numLinesRemoved == 2:
            P2TDouble = True
            lineSent += ATTACKTABLE[5]
        elif numLinesRemoved == 3:
            P2TTriple = True
            lineSent += ATTACKTABLE[6]

    if blankBoard == board:
        P2PerfectClear = True
        lineSent += ATTACKTABLE[9]

    if numLinesRemoved > 0:
        P2Combo = True
        P2ComboCounter += 1
        if P2ComboCounter <= 12:
            lineSent += COMBOTABLE[P2ComboCounter - 1]
        else: 
            lineSent += COMBOTABLE[12]
    else:
        P2ComboCounter = 0

    return lineSent, P2backToBack, P2ComboCounter, numLinesRemoved, P2PerfectClear, P2backToBackPrint, P2Tetris, P2Combo, P2TMini, P2TSingle, P2TDouble, P2TTriple


def convertToPixelCoordsP1(boxx, boxy):
    # Convert the given xy coordinates of the board to xy
    # coordinates of the location on the screen.
    return (XMARGIN -300 + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))


def drawBoxP1(boxx, boxy, color, pixelx=None, pixely=None):
    # draw a single box (each tetromino piece has four boxes)
    # at xy coordinates on the board. Or, if pixelx & pixely
    # are specified, draw to the pixel coordinates stored in
    # pixelx & pixely (this is used for the "Next" piece).
    if color == BLANK:
        return
    if loseP1:
        color = 14
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoordsP1(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx, pixely, BOXSIZE, BOXSIZE))


def convertToPixelCoordsP2(boxx, boxy):
    # Convert the given xy coordinates of the board to xy
    # coordinates of the location on the screen.
    return (XMARGIN +300 + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))


def drawBoxP2(boxx, boxy, color, pixelx=None, pixely=None):
    # draw a single box (each tetromino piece has four boxes)
    # at xy coordinates on the board. Or, if pixelx & pixely
    # are specified, draw to the pixel coordinates stored in
    # pixelx & pixely (this is used for the "Next" piece).
    if color == BLANK:
        return
    if loseP2:
        color = 14
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoordsP2(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx, pixely, BOXSIZE, BOXSIZE))    


def drawBoardP1(board):
    # fill the background of the board
    for y in range(BOARDHEIGHT - 20):
        for x in range(BOARDWIDTH):
            pygame.draw.rect(DISPLAYSURF, GRAY1, (x*BOXSIZE + XMARGIN -300 , y*BOXSIZE + TOPMARGIN + PLAYBOARD * BOXSIZE + 2, BOXSIZE, BOXSIZE), 1)
    # draw the border around the board
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN-302 , TOPMARGIN + PLAYBOARD * BOXSIZE + 2, (BOARDWIDTH * BOXSIZE) + 4, (PLAYBOARD * BOXSIZE)), 3)
    # draw the individual boxes on the board 
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBoxP1(x, y, board[x][y])


def drawBoardP2(board):
    # fill the background of the board
    for y in range(BOARDHEIGHT - 20):
        for x in range(BOARDWIDTH):
            pygame.draw.rect(DISPLAYSURF, GRAY1, (x*BOXSIZE + XMARGIN +300 , y*BOXSIZE + TOPMARGIN + PLAYBOARD * BOXSIZE + 2, BOXSIZE, BOXSIZE), 1)
    # draw the border around the board
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN+298 , TOPMARGIN + PLAYBOARD * BOXSIZE + 2, (BOARDWIDTH * BOXSIZE) + 4, (PLAYBOARD * BOXSIZE)), 3)
    # draw the individual boxes on the board 
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBoxP2(x, y, board[x][y])


def drawHiddenBoardP1():
    pygame.draw.rect(DISPLAYSURF, BLACK, (XMARGIN-302 , TOPMARGIN +2, (BOARDWIDTH * BOXSIZE) + 10, (PLAYBOARD * BOXSIZE)))


def drawHiddenBoardP2():
    pygame.draw.rect(DISPLAYSURF, BLACK, (XMARGIN+298 , TOPMARGIN +2, (BOARDWIDTH * BOXSIZE) + 10, (PLAYBOARD * BOXSIZE)))


def drawAleartBarP1(receivedLine):

    color = (255,0,0)

    if receivedLine == 0:
        color = BLACK

    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN-99 , TOPMARGIN + PLAYBOARD * BOXSIZE + 3, 8, (PLAYBOARD * BOXSIZE) - 1),3)

    pygame.draw.rect(DISPLAYSURF, color, (XMARGIN-97 , TOPMARGIN + PLAYBOARD * BOXSIZE + 3 + (BOXSIZE* (20 - receivedLine)), 4, BOXSIZE * receivedLine))


def drawAleartBarP2(receivedLine):

    color = (255,0,0)

    if receivedLine == 0:
        color = BLACK

    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN+501 , TOPMARGIN + PLAYBOARD * BOXSIZE + 3, 8, (PLAYBOARD * BOXSIZE) - 1),3)

    pygame.draw.rect(DISPLAYSURF, color, (XMARGIN+503 , TOPMARGIN + PLAYBOARD * BOXSIZE + 3 + (BOXSIZE* (20 - receivedLine)), 4, BOXSIZE * receivedLine))


def drawPieceP1(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
        pixelx, pixely = convertToPixelCoordsP1(piece['x'], piece['y'])

    # draw each of the boxes that make up the piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBoxP1(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))


def drawPieceP2(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
        pixelx, pixely = convertToPixelCoordsP2(piece['x'], piece['y'])

    # draw each of the boxes that make up the piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBoxP2(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))


def GhostPiece(fallingPiece, board):
    ghostPiece = {'shape': fallingPiece['shape'],
                  'rotation': fallingPiece['rotation'],
                  'x': fallingPiece['x'],
                  'y': fallingPiece['y'],
                  'color': PIECES_COLOR[fallingPiece['shape']] + 7}

    for i in range(-1, BOARDHEIGHT):
        if not isValidPosition(board, fallingPiece, adjY=i+2):
            break
    ghostPiece['y'] += i + 1

    return ghostPiece


def drawNextPieceP1(NEXT_PIECES):
    # draw the "next" text
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 720, 80)
    DISPLAYSURF.blit(nextSurf, nextRect)
    # draw the "next" piece
    for order, piece in enumerate(NEXT_PIECES):
        drawPieceP1(piece, pixelx=WINDOWWIDTH-740, pixely=120 + (order * 80))


def drawHoldPieceP1(piece):
    holdSurf = BASICFONT.render('Hold', True, TEXTCOLOR)
    holdRect = holdSurf.get_rect()
    holdRect.topleft = (WINDOWWIDTH - 1140, 80)
    DISPLAYSURF.blit(holdSurf, holdRect)

    if piece != None:
        drawPieceP1(piece, pixelx=WINDOWWIDTH-1140, pixely=120)


def drawNextPieceP2(NEXT_PIECES):
    # draw the "next" text
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 80)
    DISPLAYSURF.blit(nextSurf, nextRect)
    # draw the "next" piece
    for order, piece in enumerate(NEXT_PIECES):
        drawPieceP2(piece, pixelx=WINDOWWIDTH-140, pixely=120 + (order * 80))


def drawHoldPieceP2(piece):
    holdSurf = BASICFONT.render('Hold', True, TEXTCOLOR)
    holdRect = holdSurf.get_rect()
    holdRect.topleft = (WINDOWWIDTH - 540, 80)
    DISPLAYSURF.blit(holdSurf, holdRect)

    if piece != None:
        drawPieceP2(piece, pixelx=WINDOWWIDTH-540, pixely=120)


def drawText(text, x, y, color):
    infoSurf = BASICFONT.render(text, True, color)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (x, y)
    DISPLAYSURF.blit(infoSurf, infoRect)


def drawInstructions(x, y, color):
    drawText('tab: Quit', x, y, color)
    drawText('r: Reset', x, y + 20, color)
    drawText('p: Pause', x, y + 40, color)
    drawText('f: Fullscreen', x, y + 60, color)
    drawText('g: Small screen', x, y + 80, color)
    drawText('P1-e | P2-3: Hold', x, y + 100, color)
    drawText('P1-space | P2-v: Hard drop', x, y + 120, color)
    drawText('P1-left | P2-j: Move left', x, y + 140, color)
    drawText('P1-right | P2-l: Move right', x, y + 160, color)
    drawText('P1-down | P2-k: Soft drop', x, y + 180, color)
    drawText('P1-up | P2-i: Clockwise', x, y + 200, color)
    drawText('P1-w | P2-2: Counter clockwise', x, y + 220, color)
    drawText('P1-q | P2-1: Rotate 180', x, y + 240, color)


def drawSpecialMove(x, y, ComboCounter, Tspin, backToBack, board, tetris, PC, combo, mini, single, double, triple):
    if ComboCounter != 0:
        ComboCounter -= 1
     
    if PC:
        drawText('Perfect Clear', x, y, WHITE)
    if combo:
        drawText(str(ComboCounter) + ' Combo', x, y + 40, WHITE)
    if mini:
        drawText('T-Spin Mini', x, y + 80, WHITE)
    if single:
        drawText('T-Spin Single', x, y + 80, WHITE)
    if double:
        drawText('T-Spin Dounble', x, y + 80, WHITE)
    if triple:
        drawText('T-Spin Triple', x, y + 80, WHITE)
    if backToBack:
        drawText('BackToBack', x, y + 120, WHITE)
    if tetris:
        drawText('Tetris', x, y + 160, WHITE)


def fade(width, height, x, y): 
    fade = pygame.Surface((width, height))
    fade.fill((WHITE))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        DISPLAYSURF.blit(fade, (x,y))
        pygame.display.update()
        pygame.time.delay(5)



if __name__ == '__main__':
    main()