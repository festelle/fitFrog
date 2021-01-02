from pygame_functions import *

screenSize(600,600)
setBackgroundColour("dark green")
testSprite = makeSprite("imagenes\sprites\Frog-Man Hop.gif", 12)

moveSprite(testSprite,300,300,True)
showSprite(testSprite)

nextFrame = clock()

frame = 0

while True:
    if clock() > nextFrame:
        frame = (frame+1)%5
        nextFrame += 50
    
    if keyPressed("right"):
        changeSpriteImage(testSprite, 0*8+frame)
    
    if keyPressed("down"):
        changeSpriteImage(testSprite, 1*8+frame)
    
    if keyPressed("left"):
        changeSpriteImage(testSprite, 1*5+frame)
    
    if keyPressed("down"):
        changeSpriteImage(testSprite, 2*8+frame)
    
    tick(100)