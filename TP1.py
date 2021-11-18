# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 21:31:25 2021

@author: User
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
def appStarted(app):
    app.gameOver = False
    app.margin = min(app.width,app.height)
    app.enemies = [enemyShip(app.width/2, 0.1*app.height,
                             app.margin/20, 3, 'Test')]
    app.player = playerShip(app.width/2, 0.9*app.height,
                            app.margin/20, 3, None)   
    app.playerLasers = []
    app.enemyLasers = []
    app.stars = []
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
    if app.gameOver:
        pass
    elif app.margin/20 < app.player.cx and event.key == 'Left':
        app.player.cx -= app.player.r
    elif event.key == 'Right' and app.player.cx < app.width-app.margin/20:
        app.player.cx += app.player.r
    elif event.key == 'Space':
        fireLaser(app, 'player', None)
    if event.key == 'r':
        appStarted(app)

#creates the laser
def fireLaser(app, shipType, ship):
    if shipType == 'player' and len(app.playerLasers) < 2:
        newLaser = playerLaser(app.player.cx, app.player.cy-app.margin/10, 
                               'green')
        app.playerLasers.append(newLaser)
    elif shipType == 'enemy':
        newLaser = enemyLaser(ship.cx, ship.cy, 'red')
        app.enemyLasers.append(newLaser)




#carries out a movement every time a tick passes
def timerFired(app):
    if not app.gameOver:
        app.timerDelay = 1
        app.fires += 1
        moveLasers(app)
        deleteLasers(app.playerLasers,app)
        deleteLasers(app.enemyLasers,app)
        killEnemyShips(app)
        if app.fires%10 == 0:
            createStars(app)
            moveStars(app)
            deleteStars(app)
        if app.fires%50== 0:
            evadeShots(app)
        if app.fires%500 == 0:
            for enemy in app.enemies:
                fire = random.choice([True,False])
                if fire:
                    fireLaser(app, 'enemy', enemy)
        if app.player.lives == 0:
            app.gameOver = True
    
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
        if (currLaser.y0 not in range(0,app.height)
            and currLaser.y1 not in range(0,app.height)
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
        if (L.cx in range(int(app.player.cx-app.player.r), 
                          int(app.player.cx+app.player.r+1))
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
        if currShip.lives == 0:
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
            move = random.choice([2,-2])
            if (leftBound<=laser.cx<=rightBound
                   and laser.y0 - int(enemy.cy+enemy.r) <= 50
                   and hasMoved[enemy] == False):
                #check if the evasion is legal (they stay within the board)
                x=copy.copy(enemy.cx)
                fireLaser(app, 'enemy', enemy)
                if isLegalEvade(app,move,x):
                    enemy.cx = enemy.cx + move*enemy.r
                else:    
                    move *= -1
                    enemy.cx = enemy.cx + move*enemy.r
                hasMoved[enemy] = True

def isLegalEvade(app,move,x):
    x = x + move*app.margin/40
    return app.margin/40<x<app.width-app.margin/40



#calls upon other functions that allow for the objects to be drawn
def redrawAll(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill='black')
    drawStars(app, canvas)
    drawLasers(app, canvas)
    drawPlayer(app,canvas)
    drawTestEnemy(app, canvas)
    if app.gameOver:
        drawGameOver(app,canvas)

def drawGameOver(app,canvas):
    canvas.create_rectangle(0,0.3*app.height,app.width,0.7*app.height,
                            fill = 'red')
    canvas.create_text(app.width/2,app.height/2, text = 'Game Over')

def drawTestEnemy(app,canvas):
    for enemy in app.enemies:
        x0 = enemy.cx 
        y0 = enemy.cy
        r = enemy.r
        canvas.create_rectangle(x0-r,y0-r,x0+r,y0+r,fill='red')


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