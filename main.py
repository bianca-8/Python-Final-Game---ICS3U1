from pygame import * 
import random
import math
init()
size = width, height = 1000, 700
screen = display.set_mode(size)

#define colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255,255,255)
BLACK = (0,0,0)

stickmanColour = BLACK
owlColour = BLACK
penguinColour = BLACK

# define fonts
menuFont = font.SysFont("Times New Roman",60)
doneFont = font.SysFont("Times New Roman",100) #game over font
smallFont = font.SysFont("Times New Roman",20)

#Variables
grass = [0,180,380,580,680] #the place of the grass blocks
charY = 600 #y position of the character
grassY = 650 #y-coordinate of grass blocks
amount = 20 #amount subtracted from grassY
moveDown = False #character falls down
moveLeft = False #character moving left
moveRight = False #character moving right
backgroundY = 0 #y coordinate of the background
standing = True #character is standing on a block
score = 0 #score of # of blocks jumped up
currentGrass = 1 #character on first block (2 for 2nd, 3 for 3rd)
spikeMade = False #spike is made

#Uploaded images
owl = image.load("normal owl.png") #owl character
owlWidth = owl.get_width()//1.5
owlHeight = owl.get_height()//1.5
owl = transform.scale(owl,(owlWidth,owlHeight))

lPenguin = image.load("penguin.png") #penguin character
rPenguin = image.load("rightPenguin.png") #right facing penguin
penguinWidth = lPenguin.get_width()//3.5
penguinHeight = lPenguin.get_height()//3.5
lPenguin = transform.scale(lPenguin,(penguinWidth,penguinHeight))
rPenguin = transform.scale(rPenguin,(penguinWidth,penguinHeight))
penguin = lPenguin

spike = image.load("spike.png")
spike = transform.scale(spike,(10,45))

sky = image.load("sky.png")
skyWidth = sky.get_width()*2.5
skyHeight = sky.get_height()*2.5
sky = transform.scale(sky,(1000,700))

grassBlock = image.load("grassblock.png")
grassWidth = 350
grassHeight = 60
grassBlock = transform.scale(grassBlock,(grassWidth,grassHeight))

homeButton = image.load("home.png")
homeButton = transform.scale(homeButton,(45,45))

#Characters
characters = ["stickman", "owl", "penguin"]
character = characters[random.randint(0,len(characters)-1)] #random character when none are selected
if character == "stickman":
  charWidth = 200
elif character == "owl":
  charWidth = owlWidth
elif character == "penguin":
  charWidth = penguinWidth

#Grass and character X coordinates
grassX = random.choice(grass) #x coordinate of grass block chosen
grassX2 = random.choice(grass) #x coordinate of 2nd grass block chosen
grassX3 = random.choice(grass) #x coordinate of 3rd grass block chosen
while abs(grassX - grassX2) > 100:
  grassX2 = random.choice([grassX - 80,grassX + 80])
while abs(grassX2 - grassX3) > 100:
  grassX2 = random.choice([grassX2 - 80,grassX2 + 80])
while grassX2 == grassX: #chooses new if grassX = grassX2
  grassX2 = random.choice(grass)
while grassX3 == grassX2: #chooses new if grassX2 = grassX3
  grassX3 = random.choice(grass)
charX = grassX

#Background: menu, game and characters
def background(currentState,backY):
  if currentState == "menu":
    draw.rect(screen,WHITE,(0,0,1000,700))
    draw.rect(screen,RED,(200,100,500,150)) #Play Game Button
    draw.rect(screen,RED,(200,400,500,150)) #Characters Button
    screen.blit(menuFont.render("Play Game", 1, BLACK),(280,135,500,150))
    screen.blit(menuFont.render("Characters", 1, BLACK),(280,435,500,150))
  
  if currentState == "game":
    screen.blit(sky,(0,backY-700,1000,700)) #top picture
    screen.blit(sky,(0,backY,1000,700)) #middle picture
    screen.blit(sky,(0,backY+700,1000,700)) #bottom picture
    screen.blit(grassBlock,(grassX,grassY,grassWidth,grassHeight)) #first grass block
    screen.blit(grassBlock,(grassX2,grassY-200,grassWidth,grassHeight)) #second grass block
    screen.blit(grassBlock,(grassX3,grassY-400,grassWidth,grassHeight)) #third grass block
    screen.blit(smallFont.render("Score: " + str(score), 1, BLACK),(0,0,50,20)) #score
    if score >= 3:
      screen.blit(spike,(spikeX,605,10,10))
      screen.blit(spike,(spike2X,405,10,10))
      screen.blit(spike,(spike3X,205,10,10))
  
  if currentState == "characters":
    draw.rect(screen,WHITE,(0,0,1000,700))
    characterMenu()

  if currentState == "done":
    #black background
    draw.rect(screen,BLACK,(0,0,1000,700)) 
    screen.blit(doneFont.render("Game Over", 1, RED),(250,250,500,500))
    #Play again button
    draw.rect(screen,WHITE,(80,450,350,100)) 
    screen.blit(menuFont.render("Play Again", 1, RED),(90,460,350,100))
    #Quit button
    draw.rect(screen,WHITE,(580,450,350,100)) 
    screen.blit(menuFont.render("Quit", 1, RED),(670,460,350,100))
    #Score
    screen.blit(doneFont.render("Score: " + str(score), 1, RED),(350,50,500,500))

def stickman(x,y): #draw stickman
  draw.circle(screen,BLACK,(x,y-45),20,2) #head
  draw.line(screen,BLACK,(x,y+20),(x,y-25),2) #body
  draw.line(screen,BLACK,(x,y-10),(x-20,y+10),2) #left arm
  draw.line(screen,BLACK,(x,y-10),(x+20,y+10),2) #right arm
  draw.line(screen,BLACK,(x,y+20),(x-20,y+50),2) #left leg
  draw.line(screen,BLACK,(x,y+20),(x+20,y+50),2) #right leg

def gameCharacters(character,x,y):
  if currentState == "game":
    if character == 'stickman':
      stickman(x,y)
      
    if character == "owl":
      screen.blit(owl,(x-60,y-75,10,10))

    if character == "penguin":
      screen.blit(penguin,(x-60,y-95,10,10))

def characterMenu():
  if currentState == "characters":
    stickman(centreBox(100,25,200,200,10,10)[0],centreBox(100,25,200,200,10,10)[1])
    draw.rect(screen,stickmanColour,(100,25,200,200),5)
    screen.blit(owl,(centreBox(400,25,200,200,owlWidth,owlHeight)[0],centreBox(400,25,200,200,owlWidth,owlHeight)[1],25,25))
    draw.rect(screen,owlColour,(400,25,200,200),5)
    screen.blit(penguin,(centreBox(700,25,200,200,penguinWidth,penguinHeight)[0],centreBox(700,25,200,200,penguinWidth,penguinHeight)[1],25,25))
    draw.rect(screen,penguinColour,(700,25,200,200),5)

def distance(x1,x2,y1,y2):
  distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
  return distance

def centreBox(boxX,boxY,boxW,boxH,objW,objH): #centering objects and text
  objX = boxX + (boxW-objW)//2
  objY = boxY + (boxH-objH)//2
  return objX,objY

currentState = "menu"
running = True
myClock = time.Clock()

# Game Loop
while running:
  
  if charY >= 700:
    currentState = "done"
  
  for e in event.get():  # checks all events that happen
    if e.type == QUIT:
      running = False
      
    #mouse clicked
    if e.type == MOUSEBUTTONDOWN:
      if currentState == "menu":
        if e.pos[0] >= 200 and e.pos[0] <= 700 and e.pos[1] >= 100 and e.pos[1] <= 250: #Play game button clicked
          currentState = "game"
          #resets to normal
          grass = [0,180,380,580,680]
          #Grass and character X coordinates
          grassX = random.choice(grass) #x coordinate of grass block chosen
          grassX2 = random.choice(grass) #x coordinate of 2nd grass block chosen
          grassX3 = random.choice(grass) #x coordinate of 3rd grass block chosen
          while abs(grassX - grassX2) > 100:
            grassX2 = random.choice([grassX - 80,grassX + 80])
          while abs(grassX2 - grassX3) > 100:
            grassX2 = random.choice([grassX2 - 80,grassX2 + 80])
          while grassX2 == grassX: #chooses new if grassX = grassX2
            grassX2 = random.choice(grass)
          while grassX3 == grassX2: #chooses new if grassX2 = grassX3
            grassX3 = random.choice(grass)
          grassY = 650
          charX = grassX
          charY = 600
          score = 0
          currentGrass = 1
        
        if e.pos[0] >= 200 and e.pos[0] <= 700 and e.pos[1] >= 400 and e.pos[1] <= 550: #Characters button clicked
          currentState = "characters"
          
      if currentState == "game":  
        if e.pos[0] >= 950 and e.pos[0] <= 995 and e.pos[1] >= 5 and e.pos[1] <= 50: #home button clicked
          currentState = "menu"
      
      if currentState == "characters":
        if e.pos[0] >= 25 and e.pos[0] <= 225 and e.pos[1] >= 25 and e.pos[1] <= 225: #stickman character clicked
          character = "stickman"
          stickmanColour = GREEN
          owlColour = BLACK
          penguinColour = BLACK
          charWidth = 10
        elif e.pos[0] >= 300 and e.pos[0] <= 500 and e.pos[1] >= 25 and e.pos[1] <= 225: #owl character clicked
          character = "owl"
          owlColour = GREEN
          stickmanColour = BLACK
          penguinColour = BLACK
          charWidth = owlWidth
        elif e.pos[0] >= 700 and e.pos[0] <= 900 and e.pos[1] >= 25 and e.pos[1] <= 225: #owl character clicked
          character = "penguin"
          owlColour = BLACK
          stickmanColour = BLACK
          penguinColour = GREEN
          charWidth = penguinWidth
        if e.pos[0] >= 950 and e.pos[0] <= 995 and e.pos[1] >= 5 and e.pos[1] <= 50: #home button clicked
          currentState = "menu"
      
      if currentState == "done":
        if e.pos[0] >= 80 and e.pos[0] <= 430 and e.pos[1] >= 450 and e.pos[1] <= 550: #Play Again button
          currentState = "menu"
          #resets to normal
          grass = [0,180,380,580,680]
          #Grass and character X coordinates
          grassX = random.choice(grass) #x coordinate of grass block chosen
          grassX2 = random.choice(grass) #x coordinate of 2nd grass block chosen
          grassX3 = random.choice(grass) #x coordinate of 3rd grass block chosen
          while abs(grassX - grassX2) > 100:
            grassX2 = random.choice([grassX - 80,grassX + 80])
          while abs(grassX2 - grassX3) > 100:
            grassX2 = random.choice([grassX2 - 80,grassX2 + 80])
          while grassX2 == grassX: #chooses new if grassX = grassX2
            grassX2 = random.choice(grass)
          while grassX3 == grassX2: #chooses new if grassX2 = grassX3
            grassX3 = random.choice(grass)
          grassY = 650
          charX = grassX
          charY = 600
          score = 0
          currentGrass = 1
        
        if e.pos[0] >= 580 and e.pos[0] <= 930 and e.pos[1] >= 450 and e.pos[1] <= 550:
          running = False
    
    #mouse clicked
    if e.type == KEYDOWN: #clicking keys to move character
      if currentState == "game":
        #Character jumping up
        if e.key == K_w and standing == True: #w clicked and character is currently standing
          if currentGrass == 1 and charX < grassX2 or currentGrass == 1 and charX + charWidth > grassX2 + grassWidth or currentGrass == 2 and charX < grassX3 or currentGrass == 2 and charX + charWidth > grassX3 + grassWidth: #character is not under another block
            charY -= 250
            
        #a held/clicked - move left
        if e.key == K_a:
          moveLeft = True
          penguin = lPenguin
        #d held/clicked - move right
        if e.key == K_d:
          moveRight = True
          penguin = rPenguin
    
    elif e.type == KEYUP: #not clicking keys to move character
      if e.key == K_a:
        moveLeft = False
      if e.key == K_d:
        moveRight = False

  background(currentState,backgroundY)
  gameCharacters(character,charX,charY)
  
  #Home button
  if currentState == "characters" or currentState == "game":
    draw.rect(screen,RED,(950,5,45,45))
    screen.blit(homeButton,(950,5,45,45))
  
  #Character not on grass block
  if charX < grassX or charX > grassX + grassWidth or charX < grassX2 or charX > grassX2 + 100 or charX < grassX3 or charX > grassX3 + 100: #x not on grass block
    standing = False
    moveDown = True
  if charY+50 > grassY + grassHeight or charY+50 > grassY - 200 + grassHeight or charY+50 > grassY - 400 + grassHeight: #y not on grass block
    standing = False
    moveDown = True
    
  #Character on grass block
  if charX >= grassX and charX <= grassX + grassWidth and charY+50 == grassY or charX >= grassX2 and charX <= grassX2 + grassWidth and charY+50 == grassY-200 or charX >= grassX3 and charX <= grassX3 + grassWidth and charY+50 == grassY-400:
    standing = True
    moveDown = False
    #grass block character is on
    if charY == 600:
      currentGrass = 1
    if charY == 400:
      currentGrass = 2
      
  if charY == 200 and standing == True:
    backgroundY += 200
    charY += 250
    #Chooses next x coordinate of grass block
    grassX = grassX3
    grassX2 = random.choice(grass) #x coordinate of 2nd grass block chosen
    grassX3 = random.choice(grass) #x coordinate of 3rd grass block chosen
    while abs(grassX - grassX2) > 100:
      grassX2 = random.choice([grassX - 80,grassX + 80])
    while abs(grassX2 - grassX3) > 100:
      grassX2 = random.choice([grassX2 - 80,grassX2 + 80])
    while grassX2 == grassX: #chooses new if grassX = grassX2
      grassX2 = random.choice(grass)
    while grassX3 == grassX2: #chooses new if grassX2 = grassX3
      grassX3 = random.choice(grass)
    grassY = 650
    currentGrass = 1
    score += 3
    spikeX = grassX + random.randint(50,100)
    spike2X = grassX2 + random.randint(50,100)
    spike3X = grassX3 + random.randint(50,100)
    spikeMade = False
  
  if currentState == "game" and spikeMade == False:
    while score >= 3:
      if charX == charX >= spikeX and charX <= spikeX + 10 and standing == True: #touching spike
        currentState = "done"
      spikeMade = True
  
  #Moving off screen
  if charX <= 0 or charX >= 1000:
    if charX <= 0:
      charX = 1
    else:
      charX = 999
    moveLeft = False
    moveRight = False
  if charY == 700:
    currentState = "done"

  #MOVING BACKGROUND
  if backgroundY >= 700:
    backgroundY = 0
  
  if moveDown == True:
    charY += 10
  if moveLeft == True:
    charX -= 10
  if moveRight == True:
    charX += 10
  
  
  display.flip()
  myClock.tick(60)  # waits long enough to have 60 fps

quit()