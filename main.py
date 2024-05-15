import pygame
## pong game, plays to 21, splash screen displays winner as first to reach 21 points
## power ups are given after a player reaches 10 points, opponents paddle becomes smaller

### Colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

### Constants
W = 600
H = 600
pygame.font.init()
comic = pygame.font.SysFont('Comic Sans MS', 30)

### Variables
## Wait time between screens
wt = 10
mplay = False

## initial paddle 1 location
p1x = W/30
p1y = H/2 - ((W/60)**2)/2

## initial paddle 2 location
p2x = W-(W/30)
p2y = H/2 - ((W/60)**2)/2

##initialize player scores (0,0)
p1score = 0
p2score = 0
p1score_old = 0
p2score_old = 0

## w_p is w key pressed
## s_p is s key pressed
w_p = False
s_p = False
wsr = False
## u_p is up key pressed
## d_p is down key pressed
u_p = False
d_p = False
udr = False

scored = False

## distance paddle moves each time a key is pushed
dm = H/60

paddle_width = W/60
paddle_height_orig = paddle_width**2
paddle_height1 = paddle_height_orig
paddle_height2 = paddle_height_orig

##bsd = 1
## initial ball position
bx = W/2
by = H/2

## ball size/width
bw = W/65

## initial ball velocity
bxv = H/60
bxv = -bxv
byv = 0
accel = 1

### Functions
def drawpaddle(x, y, w, h):
    pygame.draw.rect(screen, WHITE, (x, y, w, h))

def drawball(x, y, bw):
    pygame.draw.circle(screen, GREEN, (int(x), int(y)), int(bw))

def uploc():  ## Update paddle locations
    global p1y
    global p2y
    if w_p:
      ## if w key pressed, move p1 paddle up, keep paddle on screen
        if p1y-(dm) < 0:
            py1 = 0
        else:
            p1y -= dm
    elif s_p:
      ## if s key pressed, move p1 paddle down, keep paddle on screen
        if p1y+(dm)+paddle_height1 > H:
            p1y = H-paddle_height1
        else:
            p1y += dm
    if u_p:
      ## if up arrow key pressed, move p2 paddle up, keep paddle on screen
        if p2y-(dm) < 0:
            p2y = 0
        else:
            p2y -= dm
    elif d_p:
      ## if down arrow key pressed, move p2 paddle up, keep paddle on screen
        if p2y+(dm)+paddle_height2 > H:
            p2y = H-paddle_height2
        else:
            p2y += dm

def upblnv():## update ball position and velocity
    global bx
    global bxv
    global by
    global byv
    global p2score
    global p1score
    global scored

    if (bx+bxv < p1x+paddle_width) and ((p1y < by+byv+bw) and (by+byv-bw < p1y+paddle_height1)):
       ## ball hits paddle 1
        bxv = -bxv
        byv = ((p1y+(p1y+paddle_height1))/2)-by
        byv = -byv/((5*bw)/7)
    elif bx+bxv < 0:
       ## ball goes out left side, player 2 scores
        p2score += 1
        scored = True
        bx = W/2
        bxv = H/60
        by = H/2
        byv = 0
    if (bx+bxv > p2x) and ((p2y < by+byv+bw) and (by+byv-bw < p2y+paddle_height2)):
       ## ball hits paddle 2
        bxv = -bxv
        byv = ((p2y+(p2y+paddle_height2))/2)-by
        byv = -byv/((5*bw)/7)
    elif bx+bxv > W:
       ## ball goes out right side, player 1 scores
        p1score += 1
        scored = True
        bx = W/2
        bxv = -H/60
        by = H/2
        byv = 0
    if by+byv > H or by+byv < 0:
       ## ball hits upper or lower boundaries
        byv = -byv

## updates both x and y position of the ball
    bx += bxv
    by += byv

def drawscore():
    score = comic.render(str(p1score) + " - " + str(p2score), False, WHITE)
    screen.blit(score, (W/2,30))

def drawwinner():
    if p1score>p2score:
        winner = comic.render(  "Player 1 Wins", False, RED)
        screen.blit(winner, (W/2,30))
    else:
        winner = comic.render(  "Player 2 Wins", False, RED)
        screen.blit(winner, (W/2,30))

### Initialize
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Snake ML v.1.0.0')
screen.fill(BLACK)
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN: ## key is pressed down
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_w:
                w_p = True
                if s_p == True:
                    s_p = False
                    wsr = True
            if event.key == pygame.K_s:
                s_p = True
                if w_p == True:
                    w_p = False
                    wsr = True
            if event.key == pygame.K_UP:
                u_p = True
                if d_p == True:
                    d_p = False
                    udr = True
            if event.key == pygame.K_DOWN:
                d_p = True
                if u_p == True:
                    u_p = False
                    udr = True
        if event.type == pygame.KEYUP: ## key is released
            if event.key == pygame.K_w:
                w_p = False
                if wsr == True:
                    s_p = True
                    wsr = False
            if event.key == pygame.K_s:
                s_p = False
                if wsr == True:
                    w_p = True
                    wsr = False
            if event.key == pygame.K_UP:
                u_p = False
                if udr == True:
                    d_p = True
                    udr = False
            if event.key == pygame.K_DOWN:
                d_p = False
                if udr == True:
                    u_p = True
                    udr = False

    screen.fill(BLACK)
    uploc()  ## Update paddle locations
    if scored:
      p1score_old = p1score
      p2score_old = p2score
    upblnv() ## Update ball location and velocity
    scored = False
    drawscore()
    drawball(bx, by, bw)

    ## if p1score == 10, make paddle_height2 half as big until p2 scores again
    ## if p2score == 10, make paddle_height1 half as big until p1 scores again

    if p1score >= 10 and p2score == p2score_old: 
      paddle_height2 = 0.5*paddle_height_orig
    else:
      paddle_height2 = paddle_height_orig

    if p2score >= 10 and p1score == p1score_old:
      paddle_height1 = 0.5*paddle_height_orig
    else:
      paddle_height1 = paddle_height_orig

    drawpaddle(p1x, p1y, paddle_width, paddle_height1)
    drawpaddle(p2x, p2y, paddle_width, paddle_height2)
    pygame.display.flip()
    pygame.time.wait(wt)

## End game
    if p1score == 21 or p2score == 21:
       ## Make splash screen announcing winner
       screen.fill(BLACK)
       drawwinner()
       pygame.display.flip()
       pygame.time.wait(200*wt)
       running = False 

