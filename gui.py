# import pygame module in this program
import pygame

# activate the pygame library
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
 
# assigning values to X and Y variable
X = 900
Y = 900

# create the display surface object
# of specific dimension..e(X, Y).
display_surface = pygame.display.set_mode((X, Y))

# set the pygame window name
pygame.display.set_caption('Vision Based Grasping Visualization')


# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.Font('freesansbold.ttf', 32)

# create a text surface object,
# on which text is drawn on it.
text = font.render(' Intertrial ', True, white, blue)

# create a rectangular object for the
# text surface object
textRect = text.get_rect()
# set the center of the rectangular object.
textRect.center = (430, 700)


text3 = font.render(' Audio Cue ', True, white, blue)
# create a rectangular object for the
# text surface object
textRect3 = text3.get_rect()
# set the center of the rectangular object.
textRect3.center = (430, 700)



text4 = font.render(' Trial 1 ', True, white, blue)
# create a rectangular object for the
# text surface object
textRect4 = text4.get_rect()
# set the center of the rectangular object.
textRect4.center = (430, 800)


text5 = font.render(' Trial 2 ', True, white, blue)
# create a rectangular object for the
# text surface object
textRect5 = text5.get_rect()
# set the center of the rectangular object.
textRect5.center = (430, 800)


text5 = font.render( 'Trial 2 ', True, white, blue)
# create a rectangular object for the
# text surface object
textRect5 = text5.get_rect()
# set the center of the rectangular object.
textRect5.center = (430, 800)

text6 = font.render(' Trial 3 ', True, white, blue)
# create a rectangular object for the
# text surface object
textRect6 = text6.get_rect()
# set the center of the rectangular object.
textRect6.center = (430, 800)


text7 = font.render(' Trial 4 ', True, white, blue)
# create a rectangular object for the
# text surface object
textRect7 = text7.get_rect()
# set the center of the rectangular object.
textRect7.center = (430, 800)

text8 = font.render(' Trial 5 ', True, white, blue)
# create a rectangular object for the
# text surface object
textRect8 = text8.get_rect()
# set the center of the rectangular object.
textRect8.center = (430, 800)



text2 = font.render( 'Smart Glasses Transparent ', True, white, blue)

textRect2 = text2.get_rect()

# set the center of the rectangular object.
textRect2.center = (430, 600)


img_bottle = pygame.image.load(r'C:\Users\annacetera\Downloads\Center-Out-main (4)\Center-Out-main\bottle.jpg') 
img_bottle = pygame.transform.scale(img_bottle, (350, 350))

img_pen = pygame.image.load(r'C:\Users\annacetera\Downloads\Center-Out-main (4)\Center-Out-main\pen.jpg') 
img_pen = pygame.transform.scale(img_pen, (350, 350))

img_empty = pygame.image.load(r'C:\Users\annacetera\Downloads\Center-Out-main (4)\Center-Out-main\empty.jpg')
img_empty = pygame.transform.scale(img_empty, (350, 350))


#image part
# img_bottle = pygame.image.load(r'C:\Users\moacc\Documents\GitHub\Center-Out\bottle.jpg') 
# img_bottle = pygame.transform.scale(img_bottle, (350, 350))

# img_pen = pygame.image.load(r'C:\Users\moacc\Documents\GitHub\Center-Out\pen.jpg') 
# img_pen = pygame.transform.scale(img_pen, (350, 350))

# img_empty = pygame.image.load(r'C:\Users\moacc\Documents\GitHub\Center-Out\empty.jpg')
# img_empty = pygame.transform.scale(img_empty, (350, 350))



img_rot_but1 = pygame.image.load(r'C:\Users\annacetera\Downloads\Center-Out-main (4)\Center-Out-main\bot1.png')
img_rot_but1 = pygame.transform.scale(img_rot_but1, (400, 350))

img_rot_but2 = pygame.image.load(r'C:\Users\annacetera\Downloads\Center-Out-main (4)\Center-Out-main\bot2.png')
img_rot_but2 = pygame.transform.scale(img_rot_but2, (350, 350))




img_rot_pen1 = pygame.image.load(r'C:\Users\annacetera\Downloads\Center-Out-main (4)\Center-Out-main\pen1.png')
img_rot_pen1 = pygame.transform.scale(img_rot_pen1, (350, 350))



img_rot_pen2 = pygame.image.load(r'C:\Users\annacetera\Downloads\Center-Out-main (4)\Center-Out-main\pen2.png')
img_rot_pen2 = pygame.transform.scale(img_rot_pen2, (350, 350))