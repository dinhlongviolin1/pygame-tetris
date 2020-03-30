import random, time, pygame, sys
from pygame.locals import *
from pynput import keyboard 

#-------------------------------------------------------
#---------------Variable Declaration--------------------
#-------------------------------------------------------

FPS = 500 
WINDOWWIDTH = 640
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

#----------------------Color Code-----------------------
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

#--------------------Color Mapping----------------------
BORDERCOLOR     = GRAY2
BGCOLOR         = BLACK
TEXTCOLOR       = WHITE
COLORS          = (GREEN, RED, BLUE, ORANGE, LIGHTBLUE, YELLOW, PINK, S_GREEN, S_RED, S_BLUE, S_ORANGE, S_LIGHTBLUE, S_YELLOW, S_PINK, GRAY3)
GAMEOVERCOLOR   = GRAY3

TEMPLATEWIDTH   = 4
TEMPLATEHEIGHT  = 4

#--------------Shape Array Mapping (4*4)----------------
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

#---------------Pieces Object Variable------------------
PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}

#---------------Piece Color Assignment------------------
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

#--------------------Wall Kick Data---------------------
set1WallkickData = [(( 0, 0), (-1, 0), (-1, 1), ( 0,-2), (-1,-2)),
                    (( 0, 0), ( 1, 0), ( 1,-1), ( 0, 2), ( 1, 2)),
                    (( 0, 0), ( 1, 0), ( 1,-1), ( 0, 2), ( 1, 2)),
                    (( 0, 0), (-1, 0), (-1, 1), ( 0,-2), (-1,-2)),
                    (( 0, 0), ( 1, 0), ( 1, 1), ( 0,-2), ( 1,-2)),
                    (( 0, 0), (-1, 0), (-1,-1), ( 0, 2), (-1, 2)),
                    (( 0, 0), (-1, 0), (-1,-1), ( 0, 2), (-1, 2)),
                    (( 0, 0), ( 1, 0), ( 1, 1), ( 0,-2), ( 1,-2))]

set2WallkickData = [(( 0, 0), (-2, 0), ( 1, 0), (-2,-1), ( 1, 2)),
                    (( 0, 0), ( 2, 0), (-1, 0), ( 2, 1), (-1,-2)),
                    (( 0, 0), (-1, 0), ( 2, 0), (-1, 2), ( 2,-1)),
                    (( 0, 0), ( 1, 0), (-2, 0), ( 1,-2), (-2, 1)),
                    (( 0, 0), ( 2, 0), (-1, 0), ( 2, 1), (-1,-2)),
                    (( 0, 0), (-2, 0), ( 1, 0), (-2,-1), ( 1, 2)),
                    (( 0, 0), ( 1, 0), (-2, 0), ( 1,-2), (-2, 1)),
                    (( 0, 0), (-1, 0), ( 2, 0), (-1, 2), ( 2,-1))]

#-------------------------------------------------------
#-----------------Tetris Game Function------------------
#-------------------------------------------------------

def getBlankBoard():
    # Create and return a new blank board data structure
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * (BOARDHEIGHT))
    return board

def getNewPiece(bag):
    # Return a random new piece in a random rotation and color
    if len(bag) == 0:
        bag = list(PIECES.keys())
    shape = bag[random.randrange(len(bag))]
    newPiece = {'shape': shape,
                'rotation': 0,
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': 19, # Start it above the board (i.e. less than 0)
                'color': PIECES_COLOR[shape]}
    return newPiece

def addToBoard(board, piece):
    # Fill in the board based on piece's location, shape, and rotation
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']

#------Check Whether Piece Is In Valid Position---------
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
    y = BOARDHEIGHT - 1 # Start y at the bottom of the board
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
            y -= 1 # Move on to check next row up
    return numLinesRemoved


#-------------------------------------------------------
#-----------------Rendering Functions-------------------
#-------------------------------------------------------

def convertToPixelCoords(boxx, boxy):
    # Convert the given xy coordinates of the board to xy
    # coordinates of the location on the screen.
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))

def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    # draw a single box (each tetromino piece has four boxes)
    # at xy coordinates on the board. Or, if pixelx & pixely
    # are specified, draw to the pixel coordinates stored in
    # pixelx & pixely (this is used for the "Next" piece).
    if color == BLANK:
        return
    if lose:
        color = 14
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx, pixely, BOXSIZE, BOXSIZE))

def drawBoard(board):
    # fill the background of the board
    for y in range(BOARDHEIGHT - 20):
        for x in range(BOARDWIDTH):
            pygame.draw.rect(DISPLAYSURF, GRAY1, (x*BOXSIZE + XMARGIN , y*BOXSIZE + TOPMARGIN + PLAYBOARD * BOXSIZE + 2, BOXSIZE, BOXSIZE), 1)
    # draw the border around the board
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN-2 , TOPMARGIN + PLAYBOARD * BOXSIZE + 2, (BOARDWIDTH * BOXSIZE) + 4, (PLAYBOARD * BOXSIZE)), 3)
    # draw the individual boxes on the board 
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])

def drawHiddenBoard():
    pygame.draw.rect(DISPLAYSURF, BLACK, (XMARGIN-2 , TOPMARGIN +2, (BOARDWIDTH * BOXSIZE) + 4, (PLAYBOARD * BOXSIZE)))

def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

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

def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])
    # draw each of the boxes that make up the piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

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

def drawNextPiece(NEXT_PIECES):
    # draw the "next" text
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 80)
    DISPLAYSURF.blit(nextSurf, nextRect)
    # draw the "next" piece
    for order, piece in enumerate(NEXT_PIECES):
        drawPiece(piece, pixelx=WINDOWWIDTH-140, pixely=120 + (order * 80))

def drawHoldPiece(piece): 
    holdSurf = BASICFONT.render('Hold', True, TEXTCOLOR)
    holdRect = holdSurf.get_rect()
    holdRect.topleft = (WINDOWWIDTH - 540, 80)
    DISPLAYSURF.blit(holdSurf, holdRect)
    if piece != None:
        drawPiece(piece, pixelx=WINDOWWIDTH-540, pixely=120)

def drawText(text, x, y):
    infoSurf = BASICFONT.render(text, True, WHITE)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (x, y)
    DISPLAYSURF.blit(infoSurf, infoRect)

def drawInstructions(x, y):
    drawText('q: Quit', x, y)
    drawText('r: Reset', x, y + 20)
    drawText('p: Pause', x, y + 40)
    drawText('f: Fullscreen', x, y + 60)
    drawText('g: Small screen', x, y + 80)
    drawText('e, c: Hold', x, y + 100)
    drawText('space: Hard drop', x, y + 120)
    drawText('left, a: Move left', x, y + 140)
    drawText('right, d: Move right', x, y + 160)
    drawText('down, s: Soft drop', x, y + 180)
    drawText('up, x: Clockwise', x, y + 200)
    drawText('w, z: Counter clockwise', x, y + 220)

#-------------------------------------------------------
#-----------------Additional Functions------------------
#-------------------------------------------------------

def checkForKeyPress():
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.
    checkForQuit()
    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None

def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

#-------------------------------------------------------
#------------------Run Game Function--------------------
#-------------------------------------------------------

def runGame():

    #-----------------Setup Variable--------------------
    global lose, DISPLAYSURF
    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    lose = False
    movingDown = False # no movingUp variable
    movingLeft = False
    movingRight = False
    alowShift = False
    canHolded = True
    fallFreq = 1

    #----------Create a bag with all 7 pieces-----------
    #----Assign pieces in bag randomly to varialbe------
    #-----------Then remove piece from bag--------------
    bag = list(PIECES.keys())
    spinDirection = ''
    fallingPiece = getNewPiece(bag)
    bag.remove(fallingPiece['shape'])
    nextPiece1 = getNewPiece(bag)
    bag.remove(nextPiece1['shape'])
    nextPiece2 = getNewPiece(bag)
    bag.remove(nextPiece2['shape'])
    nextPiece3 = getNewPiece(bag)
    bag.remove(nextPiece3['shape'])
    nextPiece4 = getNewPiece(bag)
    bag.remove(nextPiece4['shape'])
    nextPiece5 = getNewPiece(bag)
    bag.remove(nextPiece5['shape'])
    NEXT_PIECES = [nextPiece1,nextPiece2,nextPiece3,nextPiece4,nextPiece5]
    holdPiece = None

    #--------------------Game Loop----------------------
    while True:

        #--------------No Falling Piece-----------------
        if fallingPiece == None:
            # Spawn new piece
            fallingPiece = nextPiece1
            # If bag is empty --> reset bag
            if len(bag) == 0:
                bag = list(PIECES.keys())
            # Re-assign value for next pieces
            nextPiece1 = nextPiece2
            nextPiece2 = nextPiece3
            nextPiece3 = nextPiece4
            nextPiece4 = nextPiece5
            # Last piece get a new piece from bag
            nextPiece5 = getNewPiece(bag)
            bag.remove(nextPiece5['shape'])
            # Add all pieces to list
            NEXT_PIECES = [nextPiece1,nextPiece2,nextPiece3,nextPiece4,nextPiece5]
            # Reset lastFallTime
            lastFallTime = time.time() 

            # Check for whether new piece can spawn
            if not isValidPosition(board, fallingPiece):
                # Set above board position and check again
                fallingPiece['y'] = 18
                if not isValidPosition(board, fallingPiece):
                    lose = True
                    for x in range(BOARDWIDTH):
                        for y in range(BOARDHEIGHT):
                            drawBox(x, y, board[x][y])
                    drawHiddenBoard()
                    # can't fit a new piece on the board --> game over
                    return 
        
        checkForQuit()

        #------------Event handling Loop----------------
        for event in pygame.event.get():

            #-----------------KEYUP---------------------
            if event.type == KEYUP:
                if (event.key == K_LSHIFT):
                    # Quit the game
                    terminate()

                elif (event.key == K_f):
                    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.FULLSCREEN)
                    DISPLAYSURF.fill(BGCOLOR)
                    showTextScreen('Paused') # Pause until a key press
                    lastFallTime = time.time() + DELAYLOCKIN - fallFreq
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()

                elif (event.key == K_g):
                    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
                    DISPLAYSURF.fill(BGCOLOR)
                    showTextScreen('Paused') # Pause until a key press
                    lastFallTime = time.time() + DELAYLOCKIN - fallFreq
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()

                elif (event.key == K_r):
                    # Reset the game
                    return

                elif (event.key == K_h):
                    DISPLAYSURF.fill(BGCOLOR)
                    drawInstructions(240, 200)
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
                    lastFallTime = time.time() + DELAYLOCKIN - fallFreq
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()

                elif (event.key == K_LEFT or event.key == K_a):
                    movingLeft = False

                elif (event.key == K_RIGHT or event.key == K_d):
                    movingRight = False

                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = False


            #-----------------KEYDOWN---------------------
            if event.type == KEYDOWN:
                # Hold a peice
                if (event.key == K_e or event.key == K_c) and canHolded:
                    lastMoveSidewaysTime = time.time() + DELAYAUTOSHIFT
                    copyPiece = holdPiece
                    holdPiece = fallingPiece
                    fallingPiece = copyPiece
                    holdPiece['x'] = int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2) 
                    holdPiece['rotation'] = 0
                    canHolded = False
                    if fallingPiece != None:
                        fallingPiece['y'] = 19
                        if not isValidPosition(board, fallingPiece):
                            fallingPiece['y'] = 18

                # Moving the piece sideways
                elif (event.key == K_LEFT or event.key == K_a):
                    movingRight = False
                    movingLeft = True
                    if isValidPosition(board, fallingPiece, adjX=-1):
                        fallingPiece['x'] -= 1
                        lastMoveSidewaysTime = time.time() + DELAYAUTOSHIFT
                        if not isValidPosition(board, fallingPiece, adjY=1):
                            lastFallTime = time.time() + DELAYLOCKIN - fallFreq

                elif (event.key == K_RIGHT or event.key == K_d):
                    movingLeft = False
                    movingRight = True
                    if isValidPosition(board, fallingPiece, adjX=1):
                        fallingPiece['x'] += 1
                        lastMoveSidewaysTime = time.time() + DELAYAUTOSHIFT
                        if not isValidPosition(board, fallingPiece, adjY=1):
                            lastFallTime = time.time() + DELAYLOCKIN - fallFreq
                    
                # Rotating the piece (if there is room to rotate)
                elif (event.key == K_UP or event.key == K_x) and fallingPiece != None:
                    if not isValidPosition(board, fallingPiece, adjY=1):
                        lastFallTime = time.time() + DELAYLOCKIN - fallFreq
                    spinDirection = 'CW'
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                    superRotationSystem(board, fallingPiece, spinDirection)

                # Rotate the other direction
                elif (event.key == K_w or event.key == K_z) and fallingPiece != None: 
                    if not isValidPosition(board, fallingPiece, adjY=1):
                        lastFallTime = time.time() + DELAYLOCKIN - fallFreq
                    spinDirection = 'CCW'
                    fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                    superRotationSystem(board, fallingPiece, spinDirection)

                # Rotate the other direction
                elif (event.key == K_q) and fallingPiece != None: 
                    if not isValidPosition(board, fallingPiece, adjY=1):
                        lastFallTime = time.time() + DELAYLOCKIN - fallFreq
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 2) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 2) % len(PIECES[fallingPiece['shape']])

                # Making the piece fall faster with the down key
                elif (event.key == K_DOWN or event.key == K_s) and fallingPiece != None:
                    movingDown = True
                    if isValidPosition(board, fallingPiece, adjY=2):
                        fallingPiece['y'] += 2
                    elif isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()

                # Move the current piece all the way down
                elif event.key == K_SPACE and fallingPiece != None:
                    while isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    addToBoard(board, fallingPiece)
                    removeCompleteLines(board)
                    canHolded = True
                    # Spawn new piece
                    fallingPiece = nextPiece1
                    # If bag is empty --> reset bag
                    if len(bag) == 0:
                        bag = list(PIECES.keys())
                    # Re-assign value for next pieces
                    nextPiece1 = nextPiece2
                    nextPiece2 = nextPiece3
                    nextPiece3 = nextPiece4
                    nextPiece4 = nextPiece5
                    # Last piece get a new piece from bag
                    nextPiece5 = getNewPiece(bag)
                    bag.remove(nextPiece5['shape'])
                    # Add all pieces to list
                    NEXT_PIECES = [nextPiece1,nextPiece2,nextPiece3,nextPiece4,nextPiece5]
                    # Reset lastFallTime
                    lastFallTime = time.time() 
                    # Check for whether new piece can spawn
                    if not isValidPosition(board, fallingPiece):
                        # Set above board position and check again
                        fallingPiece['y'] = 18
                        if not isValidPosition(board, fallingPiece):
                            lose = True
                            for x in range(BOARDWIDTH):
                                for y in range(BOARDHEIGHT):
                                    drawBox(x, y, board[x][y])
                            drawHiddenBoard()
                            # can't fit a new piece on the board --> game over
                            return 
                    
                if event.key == pygame.K_i:
                    pygame.display.iconify()

            #---------Not KEYUP and KEYDOWN---------------
            elif event.type == pygame.ACTIVEEVENT:
                if event.gain == 1 and event.state == 6:
                    print('maximized')
                elif event.gain == 0 and event.state == 6:
                    print('minimized')  

        #-----------End Event handling Loop------------- 
         
                  
        #----Handle moving the piece from user input----
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > AUTOREPEATRATE and fallingPiece != None:
            if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                fallingPiece['x'] -= 1
            elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()

        if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1) and fallingPiece != None:
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()
            lastFallTime = time.time() + DELAYLOCKIN - fallFreq

        # Let the piece fall if it is time to fall
        if time.time() - lastFallTime > fallFreq:
            # See if the piece has landed
            if not isValidPosition(board, fallingPiece, adjY=1):
                # Falling piece has landed, set it on the board
                addToBoard(board, fallingPiece)
                removeCompleteLines(board)
                fallFreq = 1
                canHolded = True
                fallingPiece = None
            else:
                # Piece did not land, just move the piece down
                fallingPiece['y'] += 1
                lastFallTime = time.time()


        #-----------Draw and Render elements------------- 
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board)
        drawNextPiece(NEXT_PIECES)
        drawHoldPiece(holdPiece)
        drawText('Press h for help', 20, 20)
        if fallingPiece != None:
            drawPiece(GhostPiece(fallingPiece, board))
            drawPiece(fallingPiece)
        drawHiddenBoard()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


#-------------------------------------------------------
#--------------------Main Function----------------------
#-------------------------------------------------------

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
    #--------------Game loop until closed---------------
    while True:
        runGame()
        showTextScreen('Game Over')

if __name__ == '__main__':
    main()