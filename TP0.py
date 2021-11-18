# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 21:31:25 2021

@author: User
"""
import random
import math

#spaceship class. the class of all spacships in the game
class Spaceships(object):
    
    def __init__(self,cx,cy,lives):
        self.cx = cx
        self.cy = cy
        self.lives = lives
    
    def removeLives(self):
        self.lives -=1

#subclass specifically for the player's spaceship
class playerShip(Spaceships):
    
    def __init__(self,cx,cy,lives,powerUp):
        self.powerUp = powerUp
        super().__init__(cx, cy, lives)
    
    def __repr__(self):
        return 'Player'
    
    #allows for the players powerups to be changed and displayed
    def changePowerUp(self,newPowerUp):
        powerUp = newPowerUp

#spaceship subclass made for enemy ships
class enemyShip(Spaceships):
    
     def __init__(self,cx,cy,lives,version):
        self.version = version
        super().__init__(cx, cy, lives)


#made for all weapons in the game       
class Weapons(object):
    def __init__(self,cx,cy,colour):
        self.cx = cx
        self.cy = cy
        self.colour = colour

class playerLaser(Weapons):
    
    def moveLaserShot(self):
        self.cy -= 1

class enemyLaser(Weapons):
    
    def moveLaserShot(self):
        self.cy += 1


class Star(object):
    def __init__(self,cx,cy):
        colours = ['dark blue','maroon','white','yellow']
        r = [1,2,3]
        self.cx = cx
        self.cy = cy
        self.r = random.choice(r)
        self.colour = random.choice(colours)
    
    def moveStar(self):
        self.cy += 1
 
    
#General structure taken from CMU 112 graphics questions
from cmu_112_graphics import *

#creates the inital values for the game
def appStarted(app):
    app.player = playerShip(app.width/2, 0.9*app.height, 3, None)   
    app.margin = min(app.width,app.height)
    app.lasers = []
    app.stars = []
    app.fires = 0

def createStars(app):
    if len(app.stars) <= 10:
        i = 0
        for star in app.stars:
            if star.cy >= app.height/10:
                i+=1
        while i <= 1:
            cx = random.randint(0, app.width)
            newStar = Star(cx,10)
            app.stars.append(newStar)
            i += 1
        
#takes player input from the keyboard, allowing for movement and firing      
def keyPressed(app, event):
    if app.margin/20 < app.player.cx and event.key == 'Left':
        app.player.cx -= app.margin/40
    if event.key == 'Right' and app.player.cx < app.width-app.margin/20:
        app.player.cx += app.margin/40
    if event.key == 'Space':
        fireLaser(app, 'player')

#creates the laser
def fireLaser(app, shipType):
    if shipType == 'player':
        newLaser = playerLaser(app.player.cx, app.player.cy-app.margin/10, 
                               'green')
    else:
        newLaser = enemyLaser(enemy.cx, enemy.cy, 'red')
    app.lasers.append(newLaser)

#carries out a movement every time a tick passes
def timerFired(app):
    app.timerDelay = 1
    app.fires += 1
    moveLasers(app)
    deleteLasers(app)
    if app.fires%10 == 0:
        createStars(app)
        moveStars(app)
        deleteStars(app)

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
    for laser in app.lasers:
        laser.moveLaserShot()

#removes lasers that have passed offscreen
def deleteLasers(app):
    i = 0
    while i<len(app.lasers) and len(app.lasers) != 0:
        currLaser = app.lasers[i].cy
        if (currLaser not in range(0,app.height) 
            or hasCollided(currLaser)):
            app.lasers.pop(i)
        else:
            i += 1

#checks for whether a laser has hit a spaceship
def hasCollided(num):
    return 0

#calls upon other functions that allow for the objects to be drawn
def redrawAll(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill='black')
    drawStars(app, canvas)
    drawPlayer(app,canvas)
    drawLasers(app, canvas)

#possible to check whether 
def drawStars(app, canvas):
    for star in app.stars:
        x0, y0, r = star.cx, star.cy, star.r
        canvas.create_oval(x0-r,y0-r,x0+r,y0+r,fill = star.colour)

#draws the lasers specifically
def drawLasers(app, canvas):
    for laser in app.lasers:
        if laser.colour == 'green':
            canvas.create_rectangle(laser.cx-2,laser.cy-app.margin/40,
                                    laser.cx+2,laser.cy+app.margin/40,
                                    fill = 'green')

#draws the player, currently the green square is a placeholder for the player
def drawPlayer(app, canvas):
    x0 = app.player.cx 
    y0 = app.player.cy
    r = app.margin/20
    canvas.create_rectangle(x0-r,y0-r,x0+r,y0+r,fill='green')

def runGalaga():
    runApp(width=400, height=400)

def main():
    runGalaga()

if (__name__ == '__main__'):
    main()