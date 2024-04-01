import sys
import pygame
from pygame.locals import *

BOX_VALUE = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
GAME_SPRITES = {}
GAME_SOUNDS = {}
SCREEN_WIDTH = 290
SCREEN_HEIGHT = 400
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
STATE = 'start'

def renderPlayObjects(): 
    offset = 4
    for i in range(9):
        value = BOX_VALUE[i]
        if value != ' ':
            actualindex = i
            row = actualindex // 3
            col = actualindex % 3
            blitX = 0.33 * GAME_SPRITES['grid'].get_width() * col + gridx + offset
            blitY = 0.33 * GAME_SPRITES['grid'].get_height() * row + gridy + offset
            SCREEN.blit(player[value], (blitX,blitY))

def isEmpty(box_number):   # Checks whether the given box number is empty or not
    if(BOX_VALUE[box_number] == ' '):
        return True
    return False

def win(): # Checks for all the win conditions
    if((BOX_VALUE[0] == BOX_VALUE[1] and BOX_VALUE[1] == BOX_VALUE[2] and BOX_VALUE[0] != ' ') or (BOX_VALUE[3] == BOX_VALUE[4] and BOX_VALUE[4] == BOX_VALUE[5] and BOX_VALUE[5] != ' ') or (BOX_VALUE[6] == BOX_VALUE[7] and BOX_VALUE[7] == BOX_VALUE[8] and BOX_VALUE[8] != ' ') or (BOX_VALUE[0] == BOX_VALUE[3] and BOX_VALUE[3] == BOX_VALUE[6] and BOX_VALUE[6] != ' ') or (BOX_VALUE[1] == BOX_VALUE[4] and BOX_VALUE[4] == BOX_VALUE[7] and BOX_VALUE[7] != ' ') or (BOX_VALUE[2] == BOX_VALUE[5] and BOX_VALUE[5] == BOX_VALUE[8] and BOX_VALUE[8] != ' ') or (BOX_VALUE[0] == BOX_VALUE[4] and BOX_VALUE[4] == BOX_VALUE[8] and BOX_VALUE[8] != ' ') or (BOX_VALUE[2] == BOX_VALUE[4] and BOX_VALUE[4] == BOX_VALUE[6] and BOX_VALUE[6] != ' ')):
        return True
    return False

def draw(): # Checks for the draw condition
    for value in BOX_VALUE:
        if value == ' ':
            return False
    return True

def destroy(): # Terminates the program
    pygame.quit()
    sys.exit()

def createText(string, size, position, font_family_file): # Generates text on the screen (just loads, doesn't blit)
    font = pygame.font.Font(font_family_file, size)
    text = font.render(string, True, (255,255,255))
    rect = text.get_rect()
    rect.center = position
    renderPlayObjects()
    SCREEN.blit(text, rect)

def welcome(): # Function that handles the home screen
    global STATE, musicButton1Active,musicButton2Active, musicButton3Active
    # Defining values for the music player
    musicBoxX = SCREEN_WIDTH - 0.22 * SCREEN_WIDTH
    musicBoxY = 0.04 * SCREEN_HEIGHT
    musicBoxOffset = 3
    
    play_coords = (SCREEN_WIDTH//2, 2.5 * (SCREEN_HEIGHT//4) - 30)
    help_coords = (SCREEN_WIDTH//2, 3 * (SCREEN_HEIGHT//4) - 30)
    exit_coords = (SCREEN_WIDTH//2, 3.5 * (SCREEN_HEIGHT//4) - 30)

    musicOuterBox = pygame.Rect(musicBoxX, musicBoxY, 60, 25)
    musicInnerBox = pygame.Rect(musicBoxX + musicBoxOffset, musicBoxY + musicBoxOffset, 60 - 2*musicBoxOffset, 25 - 2*musicBoxOffset)

    musicBoxClicked = False
    while True:
        SCREEN.fill((0,0,0))
        pygame.draw.rect(SCREEN, (255,255,255), musicOuterBox, border_radius=20)
        pygame.draw.rect(SCREEN, (0,0,0), musicInnerBox, border_radius=20)
        createText('Music', 15, (musicBoxX + 10*musicBoxOffset, musicBoxY + 4*musicBoxOffset), informationFontFile)

        createText('Tic-Tac-Toe', 41, (SCREEN_WIDTH//2, SCREEN_HEIGHT//4 - 20), headingFontFile)
        createText('Play', 27, play_coords, informationFontFile)
        createText('Help', 27, help_coords, informationFontFile)
        createText('Exit', 27, exit_coords, informationFontFile)

        if(musicBoxClicked):
            pygame.draw.rect(SCREEN, (255,255,255), musicHandlerOuterBox)
            pygame.draw.rect(SCREEN, (0,0,0), mainMusicHandler)
            pygame.draw.rect(SCREEN, (255,255,255), partition1)
            pygame.draw.rect(SCREEN, (255,255,255), partition2)

            
            if(musicButton1Active):
                SCREEN.blit(GAME_SPRITES['pause_btn'], (playBtnX + 2, partition1Y - 27))
            else:
                SCREEN.blit(GAME_SPRITES['play_btn'], (playBtnX, partition1Y - 30))
            if(musicButton2Active):
                SCREEN.blit(GAME_SPRITES['pause_btn'], (playBtnX + 2, partition2Y - 27))
            else:
                SCREEN.blit(GAME_SPRITES['play_btn'], (playBtnX, partition2Y - 30))
            if(musicButton3Active):
                SCREEN.blit(GAME_SPRITES['pause_btn'], (playBtnX + 2, partition2Y))
            else:
                SCREEN.blit(GAME_SPRITES['play_btn'], (playBtnX, partition2Y - 2))


            createText('Let Me', 15, (musicHandlerX + 30, partition1Y - 15), informationFontFile)
            createText('Cradles', 15, (musicHandlerX + 37, partition2Y - 15), informationFontFile)
            createText('Soft BGM', 15, (musicHandlerX + 37, partition2Y + 15), informationFontFile)

        pygame.display.update()

        # Everything above handles all the bliting logic. Below is the event handling for the home screen

        for event in pygame.event.get():
            if event.type == QUIT:
                destroy()

            elif(musicBoxClicked and (event.type == KEYDOWN and event.key == K_ESCAPE)):
                musicBoxClicked = False

            elif event.type == MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()

                if (x > play_coords[0] - 37 and x < play_coords[0] + 33) and (y > play_coords[1] - 13 and y < play_coords[1] + 13):
                    STATE = 'play'
                    return
                elif (x > help_coords[0] - 37 and x < help_coords[0] + 33) and (y > help_coords[1] - 13 and y < help_coords[1] + 13):
                    STATE = 'help'
                    return
                elif (x > exit_coords[0] - 37 and x < exit_coords[0] + 33) and (y > exit_coords[1] - 13 and y < exit_coords[1] + 13):
                    destroy()

                # The above 3 conditions are to check if the player clicked on either of the 3 btns - play, help and exit
                # The below code handles the music player event handling

                elif ((x > musicBoxX and x < musicBoxX + 60) and (y > musicBoxY and y < musicBoxY + 25)): #* add the music handling code
                    if(not musicBoxClicked): # If the user has opens music player, do these things
                        musicBoxClicked = True
                        musicHandlerX = SCREEN_WIDTH - 0.329 * 1.329 * SCREEN_WIDTH
                        musicHandlerY = 0.1 * SCREEN_HEIGHT
                        musicHandlerOuterBox = pygame.Rect(musicHandlerX, musicHandlerY, 100, 90)
                        mainMusicHandler = pygame.Rect(musicHandlerX + musicBoxOffset, musicHandlerY + musicBoxOffset, 100 - 2*musicBoxOffset, 90 - 2*musicBoxOffset)

                        partition1Y = musicHandlerY + 1 * 30
                        partition2Y = musicHandlerY + 2 * 30

                        partition1 = pygame.Rect(musicHandlerX, partition1Y, 100, 2)
                        partition2 = pygame.Rect(musicHandlerX, partition2Y, 100, 2)
                        playBtnX = musicHandlerX + 0.329 * 1.329 * musicHandlerX
                        
                    else: # If it was open, close it
                        musicBoxClicked = False

                if(musicBoxClicked): # Handleing the events once the music player is open
                    if((x > playBtnX + 5 and x < playBtnX + 30) and (y > partition1Y - 30 and y < partition1Y)):
                        if(not musicButton1Active):
                            pygame.mixer.music.load('GameAssets/sounds/let_me_down.mp3')
                            pygame.mixer.music.set_volume(0.1329)
                            pygame.mixer.music.play(-1)
                            musicButton1Active = True
                            musicButton2Active = False
                            musicButton3Active = False
                        else:
                            pygame.mixer.music.stop()
                            musicButton1Active = False
                            
                    elif((x > playBtnX + 5 and x < playBtnX + 30) and (y > partition2Y - 30 and y < partition2Y)):
                        if(not musicButton2Active):
                            pygame.mixer.music.load('GameAssets/sounds/cradles.mp3')
                            pygame.mixer.music.set_volume(0.1329)
                            pygame.mixer.music.play(-1)
                            musicButton1Active = False
                            musicButton2Active = True
                            musicButton3Active = False
                        else:
                            pygame.mixer.music.stop()
                            musicButton2Active = False

                    elif((x > playBtnX + 5 and x < playBtnX + 30) and (y > partition2Y and y < partition2Y + 30)):
                        if(not musicButton3Active):
                            pygame.mixer.music.load('GameAssets/sounds/soft.mp3')
                            pygame.mixer.music.play(-1)
                            musicButton1Active = False
                            musicButton2Active = False
                            musicButton3Active = True
                        else:
                            pygame.mixer.music.stop()
                            musicButton3Active = False

def helpSection():  # Handles the help section screen
    textspeedY = -2.5
    textspacing = 30

    instruct1Y = SCREEN_HEIGHT + textspacing * 0
    instruct2Y = SCREEN_HEIGHT + textspacing * 1
    instruct3Y = SCREEN_HEIGHT + textspacing * 2
    instruct4Y = SCREEN_HEIGHT + textspacing * 3
    global STATE
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                destroy()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    STATE = 'start'
                    return
            
        SCREEN.fill((0,0,0))
        instruct1Y += textspeedY
        instruct2Y += textspeedY
        instruct3Y += textspeedY
        instruct4Y += textspeedY
        createText('A Two Player Game.',20, (SCREEN_WIDTH//2, instruct1Y), informationFontFile)
        createText('Click on Boxes to Play.',20, (SCREEN_WIDTH//2, instruct2Y), informationFontFile)
        createText('Press escape to return',20, (SCREEN_WIDTH//2, instruct3Y), informationFontFile)
        createText('to home screen.',20, (SCREEN_WIDTH//2, instruct4Y), informationFontFile)

        if(instruct4Y <= -7):
            instruct1Y = SCREEN_HEIGHT + textspacing * 0
            instruct2Y = SCREEN_HEIGHT + textspacing * 1
            instruct3Y = SCREEN_HEIGHT + textspacing * 2
            instruct4Y = SCREEN_HEIGHT + textspacing * 3

        pygame.display.update()
        FPSCLOCK.tick(30)

def playagain(lock): # This function handles all events once the game is over 
    global STATE, BOX_VALUE, activePlayer

    playerlock = False
    returnHome = False
    switchoffset = 3

    switchX = SCREEN_WIDTH - 0.15 * SCREEN_WIDTH
    switchY = 0.01 * SCREEN_HEIGHT

    backbtnX = 0.01 * SCREEN_WIDTH
    backbtnY = 0.01 * SCREEN_HEIGHT

    nextPlayerSwitchX = SCREEN_WIDTH - 0.3 * SCREEN_WIDTH
    nextPlayerSwitchY = SCREEN_HEIGHT - 0.2 * SCREEN_HEIGHT

    switch = pygame.Rect(switchX, switchY, 40, 20)
    innerswitch = pygame.Rect(switchX + switchoffset, switchY + switchoffset, 40 - 2*switchoffset, 20 - 2*switchoffset)


    nextplayerswitch = pygame.Rect(nextPlayerSwitchX, nextPlayerSwitchY, 40, 20)
    nextplayerinnerswitch = pygame.Rect(nextPlayerSwitchX + switchoffset, nextPlayerSwitchY + switchoffset, 40 - 2*switchoffset, 20 - 2*switchoffset)

    while True:  

        if(returnHome):
            STATE = 'start'
            BOX_VALUE = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
            return

        pygame.draw.rect(SCREEN, (255,255,255), nextplayerswitch, border_radius=40)
        createText(f'Player {activePlayer} first move', 15, (nextPlayerSwitchX - 85, nextPlayerSwitchY+10), informationFontFile)

        if not lock:
            print('not lock')
            controller = pygame.Rect(switchX + switchoffset, switchY + switchoffset, 20 - 2*switchoffset, 20 - 2*switchoffset)
            pygame.draw.rect(SCREEN, (0,0,0), innerswitch, border_radius=40)
            pygame.draw.rect(SCREEN, (255,0,0), controller, border_radius=40)

            SCREEN.blit(GAME_SPRITES['back'], (backbtnX, backbtnY))
        else:
            controller = pygame.Rect(switchX + switchoffset + 20, switchY + switchoffset, 20 - 2*switchoffset, 20 - 2*switchoffset)
            pygame.draw.rect(SCREEN, (0,0,0), innerswitch, border_radius=40)
            pygame.draw.rect(SCREEN, (0,255,0), controller, border_radius=40)

        if not playerlock:
            playercontroller = pygame.Rect(nextPlayerSwitchX + switchoffset, nextPlayerSwitchY + switchoffset, 20 - 2*switchoffset, 20 - 2*switchoffset)
            pygame.draw.rect(SCREEN, (0,0,0), nextplayerinnerswitch, border_radius=40)
            pygame.draw.rect(SCREEN, (255,0,0), playercontroller, border_radius=40)
        else:
            playercontroller = pygame.Rect(nextPlayerSwitchX + switchoffset + 20, nextPlayerSwitchY + switchoffset, 20 - 2*switchoffset, 20 - 2*switchoffset)
            pygame.draw.rect(SCREEN, (0,0,0), nextplayerinnerswitch, border_radius=40)
            pygame.draw.rect(SCREEN, (0,255,0), playercontroller, border_radius=40)
         
        pygame.display.update()
        FPSCLOCK.tick(30)

        # The above code handles the blitting logic and the below code handles the events

        for event in pygame.event.get():
            if event.type == QUIT:
                destroy()
            if event.type == MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if((x > 45 and x < 247) and (y > 348 and y < 372)): 
                    print('clicked')
                    BOX_VALUE = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
                    STATE = 'play'
                    if not playerlock:
                        if activePlayer == 'x':
                            activePlayer = '0'
                        else:
                            activePlayer = 'x'
                    return

                elif((x > nextPlayerSwitchX and x < nextPlayerSwitchX + 40) and (y > nextPlayerSwitchY and y < nextPlayerSwitchY + 20)):
                    if not playerlock:
                        playerlock = True
                    else:
                        playerlock = False       

                if((x > switchX and x < switchX + 40) and ((y > switchY and y < switchY + 20))):
                    if(lock):
                        lock = False
                    else:
                        lock = True
                elif(not lock and (x > backbtnX and x < backbtnX + 20) and (y > backbtnY and y < backbtnY + 15)):
                    returnHome = True         

def gameLoop():
    global STATE, BOX_VALUE, activePlayer
    winner = '-'
    pygame.mixer.music.load('GameAssets/sounds/move_final.mp3')
    
    lock = False
    returnHome = False

    switchoffset = 3
    switchX = SCREEN_WIDTH - 0.15 * SCREEN_WIDTH
    switchY = 0.01 * SCREEN_HEIGHT

    backbtnX = 0.01 * SCREEN_WIDTH
    backbtnY = 0.01 * SCREEN_HEIGHT

    switch = pygame.Rect(switchX, switchY, 40, 20)
    innerswitch = pygame.Rect(switchX + switchoffset, switchY + switchoffset, 40 - 2*switchoffset, 20 - 2*switchoffset)
    while True:     
        
        if(returnHome):
            STATE = 'start'
            BOX_VALUE = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
            return

        SCREEN.fill((0,0,0))
        SCREEN.blit(GAME_SPRITES['grid'], (gridx, gridy))
        pygame.draw.rect(SCREEN, (255,255,255), switch, border_radius=40)
        createText('Disable Escape Key', 15, (switchX - 85, switchY+10), informationFontFile)

        if not lock:
            controller = pygame.Rect(switchX + switchoffset, switchY + switchoffset, 20 - 2*switchoffset, 20 - 2*switchoffset)
            pygame.draw.rect(SCREEN, (0,0,0), innerswitch, border_radius=40)
            pygame.draw.rect(SCREEN, (255,0,0), controller, border_radius=40)

            SCREEN.blit(GAME_SPRITES['back'], (backbtnX, backbtnY))
        else:
            controller = pygame.Rect(switchX + switchoffset + 20, switchY + switchoffset, 20 - 2*switchoffset, 20 - 2*switchoffset)
            pygame.draw.rect(SCREEN, (0,0,0), innerswitch, border_radius=40)
            pygame.draw.rect(SCREEN, (0,255,0), controller, border_radius=40)
        
        if STATE != 'gameover':
            createText(f"{activePlayer}'s turn!",20, (SCREEN_WIDTH//2, SCREEN_HEIGHT - 0.1 * SCREEN_HEIGHT), informationFontFile)
        else:
            createText(f"Play Again",35, (SCREEN_WIDTH//2, SCREEN_HEIGHT - 0.1 * SCREEN_HEIGHT), informationFontFile)
            if(winner != '-'):
                createText(f'{winner} WINS!', 32, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20), informationFontFile)
            else:
                createText('DRAW!', 32, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20), informationFontFile)
            playagain(lock)
            return

        renderPlayObjects()
        pygame.display.update()
        FPSCLOCK.tick(30)

        # The above code handles all the bliting logic for the play state. And below code handles the events and core mechanics of the game.

        for event in pygame.event.get():
            if event.type == QUIT:
                destroy()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE and not lock:
                    STATE = 'start'
                    BOX_VALUE = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
                    return
            
            if STATE == 'play':
                if event.type == MOUSEBUTTONDOWN:
                    (x,y) = pygame.mouse.get_pos() # Gets the coordinates of the point clicked
                
                    if((x >= gridx and x <= GAME_SPRITES['grid'].get_width() + gridx) and (y <= GAME_SPRITES['grid'].get_height() + gridy and y >= gridy)): # Checks if the click is on the game grid
                        # automated checking for the box number and updating the grid values in memory (in the list)                        
                        x0 = int(gridx)
                        y0 = int(gridy)

                        xl = GAME_SPRITES['grid'].get_width() + x0
                        yl = GAME_SPRITES['grid'].get_height() + y0

                        stepX = GAME_SPRITES['grid'].get_width()//3 
                        stepY = GAME_SPRITES['grid'].get_height()//3 

                        colCounter = 0
                        for valueX in range(x0, xl, stepX):
                            if(x >= colCounter*stepX + x0 and x < colCounter * stepX + stepX + x0):
                                column = colCounter
                            colCounter += 1

                        rowCounter = 0
                        for valueX in range(y0, yl, stepY):
                            if(y >= rowCounter*stepY + y0 and y < rowCounter * stepY + stepY + y0):
                                row = rowCounter
                            rowCounter += 1

                        boxNumberClicked = row * 3 + column

                        if(isEmpty(boxNumberClicked)):
                            pygame.mixer.music.play()
                            BOX_VALUE[boxNumberClicked] = activePlayer # Updating the logic by filling the list with the player character
                            
                            if(win()): # Checking if the active player won
                                winner = activePlayer
                                STATE = 'gameover'
                            elif(draw()): # Checking if it is over
                                STATE = 'gameover'
                            else: # Switching the player
                                if(activePlayer == 'x'): 
                                    activePlayer = '0'
                                else:
                                    activePlayer = 'x' 
                                    
                    if((x > switchX and x < switchX + 40) and ((y > switchY and y < switchY + 20))):
                        if(lock):
                            lock = False
                        else:
                            lock = True
                    elif(not lock and (x > backbtnX and x < backbtnX + 20) and (y > backbtnY and y < backbtnY + 15)):
                        returnHome = True
                        
if __name__ == "__main__":
    # Just the basic initialisations and asset loading
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Tic-Tac-Toe")

    GAME_SPRITES['grid'] = pygame.image.load('GameAssets/sprites/grid.png').convert_alpha()
    GAME_SPRITES['zero'] = pygame.image.load('GameAssets/sprites/zero_final.png').convert_alpha()
    GAME_SPRITES['cross'] = pygame.image.load('GameAssets/sprites/cross_final.png').convert_alpha()
    GAME_SPRITES['back'] = pygame.image.load('GameAssets/sprites/back_btn.png').convert_alpha()
    GAME_SPRITES['play_btn'] = pygame.image.load('GameAssets/sprites/play.png').convert_alpha()
    GAME_SPRITES['pause_btn'] = pygame.image.load('GameAssets/sprites/pause.png').convert_alpha()
    GAME_SPRITES['logo'] = pygame.image.load('GameAssets/sprites/logo.png').convert_alpha()

    pygame.display.set_icon(GAME_SPRITES['logo'])

    headingFontFile = 'GameAssets/fonts/heading.TTF'
    informationFontFile = 'GameAssets/fonts/info.ttf'

    gridx = (SCREEN_WIDTH - GAME_SPRITES['grid'].get_width()) // 2
    gridy = 0.2 * SCREEN_HEIGHT
    player = {
        'x' : GAME_SPRITES['cross'],
        '0' : GAME_SPRITES['zero']
    }

    musicButton1Active = False
    musicButton2Active = False
    musicButton3Active = False

    activePlayer = 'x' 
    while True: # This manages the different screens (play, help and home)

        if STATE == 'start':
            welcome()
        if STATE == 'help':
            helpSection()
        if STATE == 'play':
            gameLoop()