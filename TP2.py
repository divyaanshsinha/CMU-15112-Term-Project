# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 21:31:25 2021

@author: Divyaansh Sinha; Andrew ID: divyaans
"""
import random
import math

#spaceship class. the class of all spacships in the game
class Spaceships(object):
    
    def __init__(self,cx,cy,r,lives):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.lives = lives
        self.x0 = int(self.cx-self.r)
        self.y0 = int(self.cy-self.r)
        self.x1 = int(self.cx+self.r)
        self.y1 = int(self.cy+self.r)
    
    def removeLives(self):
        self.lives -=1

#subclass specifically for the player's spaceship
class playerShip(Spaceships):
    
    def __init__(self,cx,cy,r,lives,powerUp):
        self.powerUp = powerUp
        super().__init__(cx, cy,r,lives)
    
    def __repr__(self):
        return 'Player'
    
    #allows for the players powerups to be changed and displayed
    def changePowerUp(self,newPowerUp):
        powerUp = newPowerUp

#spaceship subclass made for enemy ships
class enemyShip(Spaceships):
    
     def __init__(self,cx,cy,r,lives,version):
        self.version = version
        moveAngle = random.randint(0,360)
        self.dx = round(math.cos(moveAngle), 2)
        self.dy = round(math.sin(moveAngle), 2) 
        super().__init__(cx, cy,r,lives)



#made for all weapons in the game       
class Weapons(object):
    def __init__(self,cx,cy,colour):
        self.cx = cx
        self.cy = cy
        self.colour = colour

class Laser(Weapons):
    def __init__(self,cx,cy,colour,height = 5):
        super().__init__(cx,cy,colour)
        self.x0 = self.cx-2
        self.y0 = self.cy-height
        self.x1 = self.cx+2
        self.y1 = self.cy+height*4

class playerLaser(Laser):
    
    def moveLaserShot(self):
        self.y0 -= 1
        self.y1 -= 1

class enemyLaser(Laser):
    
    def moveLaserShot(self):
        self.y0 += 1
        self.y1 += 1

class Star(object):
    def __init__(self,cx,cy):
        colours = ['dark blue','maroon','white','yellow']
        r = [1,2,3]
        self.cx = cx
        self.cy = cy
        self.r = random.choice(r)
        self.colour = random.choice(colours)
    
    def __repr__(self):
        return f'{self.cy}'
    
    def moveStar(self):
        self.cy += 1
 
    
#General structure taken from CMU 112 graphics questions
from cmu_112_graphics import *



#creates the inital values for the game
def appStarted(app, r=1,stars = []):
    app.timerDelay = 1
    app.gameOver = False
    app.victory = False
    app.proceed = False
    app.round = r
    app.margin = min(app.width,app.height)
    app.enemies = []
    app.player = playerShip(app.width/2, 0.9*app.height,
                            app.margin/20, 30, None)   
    app.playerLasers = []
    app.enemyLasers = []
    app.stars = stars
    app.fires = 0
    #no. of background stars desired
    app.numStars = 15

#generates the stars for the background
#allows one to change the number of stars in the background     
def createStars(app):
    n = app.numStars
    if len(app.stars) < n:
        starsNeeded = n - len(app.stars)
        for i in range(starsNeeded):
            if i == 0:
                cy = 0
            else:
                cy = random.randint(i*app.width//n,
                                (i+1)*app.width//n)
            cx = random.randint(0, app.width)
            newStar = Star(cx,cy)
            app.stars.append(newStar)

        
#takes player input from the keyboard, allowing for movement and firing      
def keyPressed(app, event):
    if app.gameOver or app.victory or not app.proceed:
        if not app.proceed:
            if event.key == 'c':
                app.proceed = True
                app.round += 1
                generateNewEnemies(app)
        else:
            pass
    elif app.margin/20 < app.player.cx and event.key == 'Left':
        app.player.cx -= app.player.r
    elif event.key == 'Right' and app.player.cx < app.width-app.margin/20:
        app.player.cx += app.player.r
    elif event.key == 'Space':
        fireLaser(app, 'player', None)
    if event.key == 'r':
        appStarted(app,app.round-1,app.stars)

#randomly generates new enemies at the begnning of each round,
#within given limits
def generateNewEnemies(app):
    upperBound = int(0.1 * app.height)
    lowerBound = int(0.5 * app.height)
    leftBound = int(0.1* app.width)
    rightBound = int(0.9 * app.width)
    if app.round != 7:
        for num in range(1,app.round):
            cx = random.choice(range(leftBound,rightBound))
            cy = random.choice(range(upperBound, lowerBound))
            while not isLegalPosition(app,cx,cy):
                cx = random.choice(range(leftBound,rightBound))
                cy = random.choice(range(upperBound, lowerBound))
            else:
                app.enemies.append(enemyShip(cx, cy,app.margin/20, 3, 
                                             'Normal'))
    else:
        cx = app.width//2
        cy = app.width//10
        app.enemies.append(enemyShip(cx, cy,app.margin/20, 5, 
                                             'Boss'))

#checks to see whether the enemies are colliding with each other
def isLegalPosition(app,cx,cy):
    for enemy in app.enemies:
        separation = math.sqrt((cx - enemy.cx)**2+(cy-enemy.cy)**2)
        if separation < app.margin/10:
            return False
    return True
        
#creates the laser
def fireLaser(app, shipType, ship):
    if shipType == 'player' and len(app.playerLasers) < 3:
        newLaser = playerLaser(app.player.cx, app.player.cy-app.margin/10, 
                               'green')
        app.playerLasers.append(newLaser)
    elif shipType == 'enemy':
        newLaser = enemyLaser(ship.cx, ship.cy, 'red')
        app.enemyLasers.append(newLaser)




#carries out a movement every time a tick passes
def timerFired(app):
    if not app.gameOver and not app.victory:
        if (app.enemyLasers != [] or app.enemies != []
            or app.playerLasers != []):
            app.fires += 1
            laserProcesses(app)
            killEnemyShips(app)
            if app.fires%3 == 0:
                moveEnemies(app)
            if app.fires%10 == 0:
                starProcesses(app)
            if app.fires%50== 0:
               evadeShots(app)
            if app.fires%250 == 0:
                randomFire(app)
            if app.player.lives <= 0:
                app.gameOver = True
        else:
            changeRound(app)
        print(app.round)

def changeRound(app):
    if app.round == 7:
        app.victory = True
    if app.round < 7:
        app.proceed = False

#carries out all the required laser processes
def laserProcesses(app):
    moveLasers(app)
    deleteLasers(app.playerLasers,app)
    deleteLasers(app.enemyLasers,app)

#carries out all the required star processes
def starProcesses(app):
    createStars(app)
    moveStars(app)
    deleteStars(app)
    
#moves enemies around in a seemingly intelligent way
def moveEnemies(app):
    for enemy in app.enemies:
        if isLegalMove(app, enemy.dx, enemy.dy, enemy, 1):
            enemy.cx += enemy.dx
            enemy.cy += enemy.dy
        else:
            moveAngle = random.randint(0,360)
            enemy.dx = round(math.cos(moveAngle), 2)
            enemy.dy = round(math.sin(moveAngle), 2)

#allows for enemies to randomly fire their weapons
#the fire 'dice roll' happens every quarter of a second            
def randomFire(app):
    for enemy in app.enemies:
        fire = random.choice([True,False])
        if (fire 
            or app.player.cx-app.player.r<enemy.cx<app.player.cx+app.player.r):
            fireLaser(app, 'enemy', enemy)
    
#deletes stars that move off screen
def deleteStars(app):
    i = 0
    while i<len(app.stars) and len(app.stars) != 0:
        currStar = app.stars[i].cy
        if currStar not in range(0,app.height):
            app.stars.pop(i)
        else:
            i += 1

def moveStars(app):
    for star in app.stars:
        star.moveStar()

#moves the lasers
def moveLasers(app):
    allLasers = app.playerLasers+app.enemyLasers
    for laser in allLasers:
        laser.moveLaserShot()

#removes lasers that have passed offscreen
def deleteLasers(L,app):
    i = 0
    while i<len(L) and len(L) != 0:
        currLaser = L[i]
        if (int(currLaser.y0) not in range(0,app.height)
            and int(currLaser.y1) not in range(0,app.height)
            or hasCollided(currLaser,app)):
            L.pop(i)
        else:
            i += 1

#checks for whether a laser has hit a spaceship
#if a laser has collided, remove a life from the ship it has collided with
#then return True, so that the laser can be removed from the board
def hasCollided(L,app):
    
    if L.colour == 'green':
        for enemy in app.enemies:
            leftBound = int(enemy.cx-enemy.r)
            rightBound = int(enemy.cx+enemy.r+1)
            if (leftBound<=L.cx<=rightBound
                and L.y0<enemy.cy+enemy.r):
                enemy.removeLives()
                return True
        return False
    
    elif L.colour == 'red':
        if (app.player.cx-app.player.r<=L.cx<=app.player.cx+app.player.r
            and L.y1 > app.player.cy-app.player.r):
            app.player.removeLives()
            return True
        else:
            return False

#removes dead enemy ships from the board
def killEnemyShips(app):
    i = 0
    while i<len(app.enemies) and len(app.enemies) != 0:
        currShip = app.enemies[i]
        if currShip.lives <= 0:
            app.enemies.pop(i)
        else:
            i += 1

#when a laser is coming towards it, enemy ships attempt to evade it
def evadeShots(app):
    hasMoved = {}
    for enemy in app.enemies:
        hasMoved[enemy] = False
    
    for enemy in app.enemies:
        for laser in app.playerLasers:
            leftBound = int(enemy.cx-enemy.r)
            rightBound = int(enemy.cx+enemy.r+1)
            if (leftBound-5<=laser.cx<=rightBound+5
                   and laser.y0 - int(enemy.cy+enemy.r) <= 50
                   and hasMoved[enemy] == False):
                #check if the evasion is legal (they stay within the board)
                fireLaser(app, 'enemy', enemy)
                fireLaser(app, 'enemy', enemy)
                moveX = random.choice([2,0,-2])
                moveY = random.choice([2,0,-2])
                while not isLegalMove(app,moveX, moveY,enemy,enemy.r):
                    moveX = random.choice([2,-2])
                    moveY = random.choice([2,-2])    
                enemy.cx += moveX*enemy.r
                enemy.cy += moveY*enemy.r
                enemy.dx = moveX//2
                enemy.dy = moveY//2
                hasMoved[enemy] = True

#checks whether the enemy's evade is into a legal position 
def isLegalMove(app,moveX,moveY,enemy,r):
    x = enemy.cx + moveX*r
    y = enemy.cy + moveY*r
    shotAvoided = True
    if r == 1:
        shotAvoided = checkShotsAvoided(app,enemy,x,y)
    return (enemy.r<x<app.width-enemy.r
            and enemy.r<y<0.6*app.height-enemy.r 
            and moveX != 0 and moveY != 0 and shotAvoided)

#checks whether in the
def checkShotsAvoided(app,enemy,x,y):
    shotAvoided = True
    for laser in app.playerLasers:
        leftBound = int(x-enemy.r)
        rightBound = int(x+enemy.r+1)
        if (leftBound-2<=laser.cx<=rightBound+2 
            and y-enemy.r<=laser.cy<=y+enemy.r):
            shotAvoided = False
    return shotAvoided



#calls upon other functions that allow for the objects to be drawn
def redrawAll(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill='black')
    drawStars(app, canvas)
    drawLasers(app, canvas)
    drawPlayer(app,canvas)
    drawEnemies(app, canvas)
    drawLives(app,canvas)
    if not app.proceed:
        drawMessage(app, canvas)
    if app.gameOver:
        drawGameOver(app,canvas)
    if app.victory:
        drawVictory(app,canvas)

def drawMessage(app, canvas):
    if app.round == 1:
        canvas.create_rectangle(0,0.3*app.height,app.width,0.7*app.height,
                                fill = 'gray')
        canvas.create_text(app.width/2,app.height/2,
                           text = 'Press "c" to proceed to begin')
    else:
        canvas.create_rectangle(0,0.3*app.height,app.width,0.7*app.height,
                                fill = 'gray')
        canvas.create_text(app.width/2,app.height/2,
                           text = 'Press "c" to proceed to the next round')

def drawVictory(app,canvas):
    canvas.create_rectangle(0,0.3*app.height,app.width,0.7*app.height,
                            fill = 'blue')
    canvas.create_text(app.width/2,app.height/2, text = 'Victory')

#draws the number of lives the player has left
def drawLives(app,canvas):
    return 0

#draws the game over scene
#this occurs when all of the player's lives have been expended
def drawGameOver(app,canvas):
    canvas.create_rectangle(0,0.3*app.height,app.width,0.7*app.height,
                            fill = 'red')
    canvas.create_text(app.width/2,app.height/2, text = 'Game Over')

#draws a placeholder enemy
def drawEnemies(app,canvas):
    for enemy in app.enemies:
        x0 = enemy.cx 
        y0 = enemy.cy
        r = enemy.r
        if enemy.version == 'Normal':
            canvas.create_rectangle(x0-r,y0-r,x0+r,y0+r,fill='red')
        elif enemy.version == 'Boss':
            canvas.create_rectangle(x0-r,y0-r,x0+r,y0+r,fill='purple')


#possible to check whether 
def drawStars(app, canvas):
    for star in app.stars:
        if star.cy in range(0,app.height+3):
            x0, y0, r = star.cx, star.cy, star.r
            canvas.create_oval(x0-r,y0-r,x0+r,y0+r,fill = star.colour)

#draws the lasers specifically
def drawLasers(app, canvas):
    for laser in app.playerLasers:
        canvas.create_rectangle(laser.x0,laser.y0,
                                laser.x1,laser.y1,
                                fill = 'green')
    for laser in app.enemyLasers:
        canvas.create_rectangle(laser.x0,laser.y0,
                                laser.x1,laser.y1,
                                fill = 'red')

#draws the player, currently the green square is a placeholder for the player
def drawPlayer(app, canvas):
    x0 = app.player.cx 
    y0 = app.player.cy
    r = app.player.r
    canvas.create_rectangle(x0-r,y0-r,x0+r,y0+r,fill='green')



def runGalaga():
    runApp(width=400, height=400)

def main():
    runGalaga()

if (__name__ == '__main__'):
    main()