import pygame, sys, random, time
from pygame.locals import *
from threading import Thread
import mediapipe as mp
import cv2
import numpy as np

pygame.mixer.pre_init()
pygame.init()

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

#get left or right hand 
def get_label(index, hand, results):
    output = None

    for classification in results.multi_handedness:
       
        #if classification.classification[0].index == index:
            
            #process results
            text = classification.classification[0].label #get label from classification
            
            output = text

    return output

# USE CONSTANTS VARIABLES FOR SCREEN SETUP
WIDTH = 1000
HEIGHT = 750
WHITE = (255,255,255)
OBJECT_SPEED = 10

score = 0
life = 3
level = 1
# time = 60

# CREATE THE GAME SCREEN
screen = pygame.display.set_mode((WIDTH,HEIGHT),0,32)

font = pygame.font.SysFont(None, 25)

# SETTING FRAMERATE SPEED
clock = pygame.time.Clock()

# A TIMER TO CHECK EVERY SECOND
pygame.time.set_timer(USEREVENT+1,1000)

# SET DELAY FOR DETECTING IF MOVEMENT KEYS ARE BEING REPEATED
pygame.key.set_repeat(100,30)

# SET GAME NAME
pygame.display.set_caption("DEMO1")

# NAME GRAPHICS IMAGES AND SOUNDS
backgroundImg = "background.jpeg"
hamsterImg = "hamster.png"
bunnyImg = "bunny.png"
piggyImg = "piggy.png"
pusheenImg = "pusheen.png"
froggyImg = "froggy.png"
basketImg = "basket.png"

# IMPORT GRAPHICS IMAGES
background = pygame.image.load(backgroundImg).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
hamster = pygame.image.load(hamsterImg).convert_alpha()
hamster = pygame.transform.scale(hamster,(100,100))
bunny = pygame.image.load(bunnyImg).convert_alpha()
bunny = pygame.transform.scale(bunny,(100,100))
piggy = pygame.image.load(piggyImg).convert_alpha()
piggy = pygame.transform.scale(piggy,(100,100))
pusheen = pygame.image.load(pusheenImg).convert_alpha()
pusheen = pygame.transform.scale(pusheen,(150,150))
froggy = pygame.image.load(froggyImg).convert_alpha()
froggy = pygame.transform.scale(froggy,(150,150))
basket = pygame.image.load(basketImg).convert_alpha()
basket = pygame.transform.scale(basket,(150,150))

# SET INITIAL LOCATION OF IMAGE
background_x, background_y = 0, 0
hamster_x = random.randrange(100,WIDTH-100)
bunny_x = random.randrange(100,WIDTH-100)
piggy_x = random.randrange(100,WIDTH-100)
pusheen_x = random.randrange(100,WIDTH-100)
froggy_x = random.randrange(100,WIDTH-100)
hamster_y, bunny_y, piggy_y, pusheen_y, froggy_y = -10, -100, -200, -300, -400
basket_y = 600
basket_x = 420

# USES A LIST TO STORE X-, Y-COORDINATES
list_xy = [(hamster_x, hamster_y), (bunny_x, bunny_y), (piggy_x,piggy_y), (pusheen_x,pusheen_y),(froggy_x,froggy_y)]

# STARTING THE MIXER
pygame.mixer.init()

# Loading the song0
pygame.mixer.music.load("backgroundmusic.mp3")

# PLAY BACKGROUNG MUSIC
pygame.mixer.music.play(loops=-1)

sound1 = pygame.mixer.Sound("sound1.mp3")
# sound2 = pygame.mixer.Sound("sound2.mp3")
# sound3 = pygame.mixer.Sound("sound3.mp3")
# sound4 = pygame.mixer.Sound("sound4.mp3")
# sound5 = pygame.mixer.Sound("sound5.mp3")

# Setting the volume
pygame.mixer.music.set_volume(0.3)
pygame.mixer.Channel(0).set_volume(1.5)

# TEXT
pygame.font.init()

# FORMAT TEXT
my_font = pygame.font.SysFont("Comic Sans MS", 70)

# INITIAL STATE OF GAMEOVER
gameOver = False

# COLLISION
def collide(x,y):
	return (abs(x - basket_x) <= 100) and (0 <= (basket_y - y) <= 50)

# PLAY INDEX
i = 0

# GAME LOOP
while True:

	# getting webcam feed
	cap = cv2.VideoCapture(0) 
	
	clock.tick(30)

	# close window
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				pygame.quit()
				exit()
    
	with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
		
		#read the frame
		ret, frame = cap.read()

		#detection
		frame = cv2.resize(frame, (400, 400))

		#BGR 2 RGB
		image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		
		image = cv2.flip(image, 1) #flip image horizontal
		#Set flag
		image.flags.writeable = False

		#Detection
		results = hands.process(image)

		#Set flag to true
		image.flags.writeable = True

		#RGB 2 BGR
		image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

		#print detection result
		# print(results)

		#render results
		if results.multi_hand_landmarks:
			#print(results.multi_hand_landmarks)
			for  num, hand in enumerate(results.multi_hand_landmarks):
				
				#render left or right detection
				index = results.multi_handedness[0].classification[0].index
				if (len(results.multi_handedness) < 2):
					if get_label(num, hand, results): #checking if we actually have a result
							
						text = get_label(num, hand, results)

						#If the detection is left hand, move the basket left
						if (text == "Left" and basket_x >= 0):
							basket_x -= 30 

						#If the detection is right hand, move the basket right
						if (text == "Right" and basket_x <= WIDTH-150) :
							basket_x += 30

		#show camera screen
		cv2.imshow("Hand Tracking", image)				
            

	# SHOW BACKGROUND IMAGE
	screen.blit(background,(background_x,background_y))

	# SHOW SCORE
	timer_text = my_font.render(f"Score: {score}", True, (WHITE))
	screen.blit(timer_text,(20,50))

	# GAME OVER HANDLING
	if gameOver:

		# SHOW GAME OVER
		text_surface = my_font.render("GAME OVER", True, (WHITE))
		screen.blit(text_surface, (300,350))
		pygame.display.update()

		# FREEZE SCREEN FOR 5 SECONDS
		time.sleep(5)

		# EXIT GAME
		break

	# hamster_rect = hamster.get_rect(center=(hamster_x,hamster_y))
	screen.blit(hamster,((hamster_x,hamster_y)))
	screen.blit(bunny,(bunny_x,bunny_y))
	screen.blit(piggy,(piggy_x,piggy_y))
	screen.blit(basket,(basket_x,basket_y))
	screen.blit(pusheen,(pusheen_x,pusheen_y))
	screen.blit(froggy,(froggy_x,froggy_y))

	# HANDLE THE BOUNDARIES
	bunny_y += OBJECT_SPEED
	hamster_y += OBJECT_SPEED
	piggy_y += OBJECT_SPEED
	pusheen_y += OBJECT_SPEED
	froggy_y += OBJECT_SPEED

	
	if hamster_y >= HEIGHT or collide(hamster_x,hamster_y):
		#If the player catches the hamster, add score and play sound
		if hamster_y < HEIGHT:
			score += 1
			pygame.mixer.Channel(0).play(sound1, maxtime=500)

		#Else, decrease points from life
		else:
			life -= 1
			if life <= 0:
				gameOver = True
		hamster_x = random.randrange(100,WIDTH-100)
		hamster_y = random.randrange(-60,-20)

	if bunny_y >= HEIGHT or collide(bunny_x,bunny_y):
		#If the player catches the bunny, add score and play sound
		if bunny_y < HEIGHT:
			score += 1
			pygame.mixer.Channel(0).play(sound1, maxtime=500)

		#Else, decrease points from life
		else:
			life -= 1
			if life <= 0:
				gameOver = True
		bunny_x = random.randrange(100,WIDTH-100)
		bunny_y = random.randrange(-60,-20)

	if piggy_y >= HEIGHT or collide(piggy_x,piggy_y):
		#If the player catches the piggy, add score and play sound
		if piggy_y < HEIGHT:
			score += 1
			pygame.mixer.Channel(0).play(sound1, maxtime=500)
		
		#Else, decrease points from life
		else:
			life -= 1
			if life <= 0:
				gameOver = True
		piggy_x = random.randrange(100,WIDTH-100)
		piggy_y = random.randrange(-60,-20)
	
	if pusheen_y >= HEIGHT or collide(pusheen_x,pusheen_y):
		#If the player catches pusheen, add score and play sound
		if pusheen_y < HEIGHT:
			score += 1
			pygame.mixer.Channel(0).play(sound1, maxtime=500)

		#Else, decrease points from life
		else:
			life -= 1
			if life <= 0:
				gameOver = True
		pusheen_x = random.randrange(100,WIDTH-100)
		pusheen_y = random.randrange(-60,-20)
	
	if froggy_y >= HEIGHT or collide(froggy_x,froggy_y):
		#If the player catches the froggy, add score and play sound
		if froggy_y < HEIGHT:
			score += 1
			pygame.mixer.Channel(0).play(sound1, maxtime=500)

		#Else, decrease points from life
		else:
			life -= 1
			if life <= 0:
				gameOver = True
		froggy_x = random.randrange(100,WIDTH-100)
		froggy_y = random.randrange(-60,-20)

	# UPDATE THE SCREEN
	pygame.display.update()