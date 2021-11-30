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
        moveAngle = 2*math.pi*random.randint(0,360)/360
        self.flockLeader = False
        if self.flockLeader:
            self.dx = round(math.cos(moveAngle), 2)
            self.dy = round(math.sin(moveAngle), 2)
        else:
            self.dx = 0
            self.dy = 0
        self.firing = False
        super().__init__(cx, cy,r,lives)

class bossShip(enemyShip):
    
    def __init__(self,cx,cy,r,lives,version):
        super().__init__(cx,cy,r,lives,version)
        self.shielded = True
        self.chargingBomb = False


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

class Bomb(Weapons):
    
    def __init__(self,cx,cy,colour,r):
        self.r = r
        super().__init__(cx,cy,colour)

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
def appStarted(app, r=5,stars = [], lasersFired = 0, hits = 0, lives = 5):
    app.timerDelay = 1
    app.gameOver = False
    app.victory = False
    app.proceed = False
    app.round = r
    app.margin = min(app.width,app.height)
    app.enemies = []
    app.player = playerShip(app.width/2, 0.9*app.height,
                            app.margin/20, lives, None)   
    app.playerLasers = []
    app.enemyLasers = []
    app.stars = stars
    app.fires = 0
    #no. of background stars desired
    app.numStars = 15
    app.lasersFired = lasersFired
    app.hits = hits
    app.bomb = []
    app.fireBomb = False
    app.tempFire = None; app.shieldLostTime = None
    app.fireCount = 1
    app.exploded = (False,None)
    
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
                scaleEnemies(app)
                if app.round != 2:
                    app.player.lives += 1
        else:
            pass
    elif app.margin/20 < app.player.cx and event.key == 'Left':
        app.player.cx -= app.player.r
    elif event.key == 'Right' and app.player.cx < app.width-app.margin/20:
        app.player.cx += app.player.r
    elif event.key == 'Space':
        fireLaser(app, 'player', None)
    elif event.key == 'r':
        app.player.lives -=1
        appStarted(app,app.round-1,app.stars,app.lasersFired,app.hits,
                   app.player.lives)

#changes enemy parameters, and thus the difficulty based on
# hit ratios
def scaleEnemies(app):
    if app.lasersFired == 0:
        lasersFired = 1
    else:
        lasersFired = app.lasersFired
    hitRatio = round(app.hits/lasersFired*100,1)
    if hitRatio >= 30 or app.round > 3:
        for enemy in app.enemies:
            enemy.r//=2
            
    if hitRatio >= 50:
        app.fireCount = 2
    else:
        app.fireCount = 1

#randomly generates new enemies at the begnning of each round,
#within given limits
def generateNewEnemies(app):
    upperBound = int(0.1 * app.height)
    lowerBound = int(0.5 * app.height)
    leftBound = int(0.1* app.width)
    rightBound = int(0.9 * app.width)
    if app.round != 7:
        for num in range(1,3*app.round-2):
            cx = random.choice(range(leftBound,rightBound))
            cy = random.choice(range(upperBound, lowerBound))
            while not isLegalPosition(app,cx,cy):
                cx = random.choice(range(leftBound,rightBound))
                cy = random.choice(range(upperBound, lowerBound))
            else:
                app.enemies.append(enemyShip(cx, cy,app.margin/30, 1, 
                                             'Normal'))
    else:
        cx = app.width//2
        cy = app.width//10
        app.enemies.append(bossShip(cx, cy,app.margin/20, 5, 
                                             'Boss'))

def chooseFirers(app):
    firers = 0
    for enemy in app.enemies:
        if enemy.firing:
            firers += 1
    while firers < app.round-1 and firers < len(app.enemies):
        index = random.choice(range(len(app.enemies)))
        while app.enemies[index].firing:
            index = random.choice(range(len(app.enemies)))
        app.enemies[index].firing = True
        firers += 1

#randomly chooses a flockLeader out of all the enemies
def chooseFlockLeader(app):
    noFlockLeader = True
    for enemy in app.enemies:
        if enemy.flockLeader == True:
            noFlockLeader = False
    if noFlockLeader and app.enemies != []:
        leaderIndex = random.choice(range(len(app.enemies)))
        app.enemies[leaderIndex].flockLeader = True
        app.flockLeader = app.enemies[leaderIndex]

#checks to see whether the enemies are colliding with each other
def isLegalPosition(app,cx,cy):
    for otherEnemy in app.enemies:
        oX = otherEnemy.cx
        oY = otherEnemy.cy
        if abs(oX-cx) <= 2*otherEnemy.r+1 and abs(oY-cy) <= 2*otherEnemy.r+1:
            return False
    return True
        
#creates the laser
def fireLaser(app, shipType, ship):
    if shipType == 'player' and len(app.playerLasers) < 1:
        newLaser = playerLaser(app.player.cx, app.player.cy-app.margin/10, 
                               'green')
        app.playerLasers.append(newLaser)
        app.lasersFired +=1
    elif shipType == 'enemy':
        newLaser = enemyLaser(ship.cx, ship.cy, 'red')
        app.enemyLasers.append(newLaser)




#carries out a movement every time a tick passes
def timerFired(app):
    if not app.gameOver and not app.victory:
        if (app.enemyLasers != [] or app.enemies != []
            or app.playerLasers != []):
            app.fires += 1
            chooseFirers(app)
            chooseFlockLeader(app)
            
            #this is the implementation of Boids
            changeDirection(app)
            
            laserProcesses(app)
            killEnemyShips(app)
            if app.fires%3 == 0:
                moveEnemies(app)
            if app.fires%40 == 0:
                starProcesses(app)
                pass
            if app.fires%40== 0:
                evadeShots(app)
            if app.fires%250 == 0:
                randomFire(app)
            if app.player.lives <= 0:
                app.gameOver = True
            if (app.round == 7 and app.enemies != [] 
                and app.enemies[0].shielded and app.fires%5000 == 0 
                and app.round == 7
                and app.enemies[0].chargingBomb == False):
                app.enemies[0].chargingBomb = True
            if app.fires%4000 and app.round == 7:
                if app.enemies != [] and app.enemies[0].chargingBomb == True:
                    chargeBomb(app)
                    if (app.bomb[0].r == 5
                        and app.tempFire != None 
                        and app.fires - app.tempFire == 750):
                        app.fireBomb = True
            if app.fireBomb == True:
                moveBomb(app)
            explodeBomb(app,0)
            deleteBomb(app)
            if (app.shieldLostTime!= None 
                and app.fires - app.shieldLostTime == 2000):
                app.shieldLostTime = None
                app.enemies[0].shielded = True
        else:
            changeRound(app)

#acts as the collision detector for the bomb
#also deletes the bomb right after
def deleteBomb(app):
    if app.bomb != [] and app.bomb[0].r == 50:
        bomb = app.bomb[0]
        for enemy in app.enemies:
            if (abs(enemy.cx-bomb.cx) < bomb.r+enemy.r
                and abs(enemy.cy-bomb.cy) < bomb.r+enemy.r):
                if enemy.shielded == True:
                    enemy.shielded = False
                    app.shieldLostTime = app.fires
                elif enemy.shielded == False:
                    enemy.removeLives()
        if (abs(app.player.cx-bomb.cx) < bomb.r+enemy.r
            and abs(app.player.cy-bomb.cy) < bomb.r+enemy.r):
            app.player.removeLives()
        app.bomb.pop()
    if app.enemies == []:
        app.bomb.clear()

#expands the bombs radius and sets back all parameters used for the bomb
def explodeBomb(app,r):
    if app.bomb != []:
        bomb = app.bomb[0]
        if bomb.cy >= app.player.cy or r:
            bomb.r = 50
            app.fireBomb = False
            app.tempFire = None
            app.chargingBomb = False
            
#move the bomb down towards the player        
def moveBomb(app):
    if app.bomb != []:
        bomb = app.bomb[0]
        if bomb.cy < app.player.cy:
            bomb.cy += 0.5

#generates the bomb and makes sure the boss ship holds it until it is fired
def chargeBomb(app):
    boss = app.enemies[0]
    if app.bomb == []:
        bomb = Bomb(boss.cx, boss.cy+boss.r+6, 'red', 1)
        app.bomb.append(bomb)
    else:
        if app.fireBomb == False:
            bomb = app.bomb[0]
            bomb.cx, bomb.cy = boss.cx, boss.cy+boss.r+6
            if bomb.r < 5:
                bomb.r += 1
            elif bomb.r == 5 and app.tempFire == None:
                app.tempFire = app.fires

#allows for the round to be changed
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
        if isinstance(enemy, bossShip):
            if enemy.chargingBomb == True:
                pass
            else:
                for num in range(app.fireCount):
                    fireLaser(app, 'enemy', enemy)
        else:
            fire = random.choice([True,False])
            cx = app.player.cx
            r = app.player.r
            if (enemy.firing and (fire 
                or cx-r<enemy.cx<cx+r)):
                for num in range(app.fireCount):
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

#moves stars downwards
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

#if a laser collides with the boss when it is holding a bomb,
#if the shields are active, they are deactivated for a time
#if they are inactive, removes a life
def hasCollided(L,app):
    
    if L.colour == 'green':
        for enemy in app.enemies:
            leftBound = int(enemy.cx-enemy.r)
            rightBound = int(enemy.cx+enemy.r)
            if (leftBound<=L.cx<=rightBound
                and L.y0<enemy.cy+enemy.r
                and L.y1>=enemy.cy-enemy.r):
                if app.round == 7:
                    if enemy.shielded == True:
                        if (app.bomb != [] 
                            and app.bomb[0].cx == enemy.cx
                            and app.bomb[0].cy == enemy.cy+enemy.r+6):
                            explodeBomb(app, 1)
                            deleteBomb(app)
                    else:
                        enemy.removeLives()
                else:
                    enemy.removeLives()
                app.hits += 1
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
            executeEvade(app,enemy,laser,hasMoved)

def executeEvade(app,enemy,laser,hasMoved):
    choices = None
    leftBound = int(enemy.cx-enemy.r)-2
    rightBound = int(enemy.cx+enemy.r)+2
    if (leftBound<=laser.cx<enemy.cx<app.width-3*enemy.r
           and laser.y0 - int(enemy.cy+enemy.r) <= 50
           and hasMoved[enemy] == False):
        #check if the evasion is legal (they stay within the board)
        choices = range(-45,45)
    elif (3*enemy.r<enemy.cx<=laser.cx<=rightBound
           and laser.y0 - int(enemy.cy+enemy.r) <= 50
           and hasMoved[enemy] == False):
        choices = range(135,225)
    if choices != None:
        moveX, moveY = 0,0
        while not isLegalMove(app,moveX, moveY,enemy,enemy.r):
            moveAngle = 2*math.pi*random.choice(choices)/360
            moveX = round(math.cos(moveAngle), 2)
            moveY = round(math.sin(moveAngle), 2)
        if enemy.firing:
            fireLaser(app, 'enemy', enemy)
        enemy.cx += 2*moveX*enemy.r
        enemy.cy += 2*moveY*enemy.r
        enemy.dx = moveX
        enemy.dy = moveY
        hasMoved[enemy] = True
    

#checks whether the enemy's movement is into a legal position 
def isLegalMove(app,moveX,moveY,enemy,r):
    x = enemy.cx + 2*moveX*r
    y = enemy.cy + 2*moveY*r
    shotAvoided = True
    if r == 1:
        shotAvoided = checkShotsAvoided(app,enemy,x,y)
    return (enemy.r<x<app.width-enemy.r
            and enemy.r<y< 0.6*app.height-enemy.r and 
            moveX != 0 and moveY != 0 
            and shotAvoided)

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

def changeDirection(app):
    for enemy in app.enemies:
        if not enemy.flockLeader == True:
            v1 = cohesiveMovement(app,enemy)
            v2 = followLeader(app,enemy)
            v3 = distancing(app, enemy)
            v4 = controlVelocity(app, enemy)
            v = [v1[0]+v2[0]+v3[0]+v4[0],v1[1]+v2[1]+v3[1]+v4[1]]
            v[0] += enemy.dx; v[1] += enemy.dy 
            lengthV = math.sqrt(v[0]**2+v[1]**2)
            v[0] /= lengthV; v[1] /= lengthV
            enemy.dx = v[0]; enemy.dy = v[1]
    
def followLeader(app,enemy):
    leader = app.flockLeader
    x = len(app.enemies)-1
    direction = [x*(leader.cx-enemy.cx)/10,x*(leader.cy-enemy.cy)/10]
    return direction

def distancing(app,enemy):
    distance = [0,0]
    for otherEnemy in app.enemies:
        if enemy != otherEnemy:
            if not isNoOverlap(app,enemy, enemy.cx, enemy.cy,otherEnemy):
                distance[0] -= (otherEnemy.cx-enemy.cx)
                distance[1] -= (otherEnemy.cy-enemy.cy)
    return distance

def cohesiveMovement(app,enemy):
    nearbyEnemies = []
    for otherEnemy in app.enemies:
        if otherEnemy != enemy and isInRange(app,enemy,otherEnemy):
            nearbyEnemies.append(otherEnemy)
    centreOfMass = [0,0]
    for otherEnemy in nearbyEnemies:
        if otherEnemy != enemy:
            centreOfMass[0] += otherEnemy.cx
            centreOfMass[1] += otherEnemy.cy
    centreOfMass[0] /= (len(app.enemies)-1)
    centreOfMass[1] /= (len(app.enemies)-1)
    centreOfMass[0] -= enemy.cx
    centreOfMass[1] -= enemy.cy
    centreOfMass[0] /= 100
    centreOfMass[1] /= 100
    return centreOfMass

def controlVelocity(app,enemy):
    meanVelocity = [0,0]
    for otherEnemy in app.enemies:
        if enemy != otherEnemy:
            meanVelocity[0] += otherEnemy.dx
            meanVelocity[1] += otherEnemy.dy
    meanVelocity[0] -= enemy.dx; meanVelocity[1] -= enemy.dy
    meanVelocity[0] /= 8; meanVelocity[1] /= 8
    return meanVelocity

def isInRange(app,enemy,other):
    distance = math.sqrt((other.cx-enemy.cx)**2+(other.cy-enemy.cy)**2)
    return distance <= 3*enemy.r

#checks to make sure the enemies don't overlap during any movements
def isNoOverlap(app,enemy,x,y,otherEnemy):
        oX = otherEnemy.cx
        oY = otherEnemy.cy
        if (abs(oX-x) <= 3*enemy.r+1 and abs(oY-y) <= 3*enemy.r+1
            and otherEnemy != enemy):
            return False
        return True

#calls upon other functions that allow for the objects to be drawn
def redrawAll(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill='black')
    drawStars(app, canvas)
    drawLasers(app, canvas)
    drawBomb(app, canvas)
    drawPlayer(app,canvas)
    drawEnemies(app, canvas)
    if not app.proceed:
        drawMessage(app, canvas)
    if app.gameOver:
        drawGameOver(app,canvas)
    if app.victory:
        drawVictory(app,canvas)
    drawLives(app,canvas)
    drawHitRatio(app, canvas)

#draws the hit ratio info on the canvas
def drawHitRatio(app, canvas):
    if app.lasersFired == 0:
        lasersFired = 1
    else:
        lasersFired = app.lasersFired
    hitRatio = round(app.hits/lasersFired*100,1)
    canvas.create_text(app.width*0.9,app.height*0.1, fill = 'white', 
                       text = f'Hit Ratio: {hitRatio}')

#draws the messages before each round
def drawMessage(app, canvas):
    if app.round == 1:
        canvas.create_rectangle(0,0.3*app.height,app.width,0.7*app.height,
                                fill = 'gray')
        canvas.create_text(app.width/2,app.height/2,
                           text = 'Press "c" to begin')
    else:
        canvas.create_rectangle(0,0.3*app.height,app.width,0.7*app.height,
                                fill = 'gray')
        canvas.create_text(app.width/2,app.height/2,
                           text = 'Press "c" to proceed to the next round')

#draws the victory screen
def drawVictory(app,canvas):
    canvas.create_rectangle(0,0.3*app.height,app.width,0.7*app.height,
                            fill = 'blue')
    canvas.create_text(app.width/2,app.height/2, text = 'Victory')

#draws the number of lives the player has left
def drawLives(app,canvas):
    canvas.create_text(app.width//10,app.height*0.1, fill = 'white', 
                       text = f'Lives: {app.player.lives}')

#draws the game over scene
#this occurs when all of the player's lives have been expended
def drawGameOver(app,canvas):
    canvas.create_rectangle(0,0.3*app.height,app.width,0.7*app.height,
                            fill = 'red')
    canvas.create_text(app.width/2,app.height/2, text = 'Game Over')

#draws a placeholder enemy
def drawEnemies(app,canvas):
    if app.round == 7 and app.enemies != []:
        drawBoss(app,canvas)
    else:
        for enemy in app.enemies:
            x0 = enemy.cx 
            y0 = enemy.cy
            r = enemy.r
            if enemy.version == 'Normal':
                canvas.create_rectangle(x0-r,y0-r,x0+r,y0+r,fill='red')
                
#draws the boss character, including the shields (the light blue outline)
def drawBoss(app,canvas):
    boss = app.enemies[0]
    x0 = boss.cx
    y0 = boss.cy
    r = boss.r
    if boss.shielded == True:
        canvas.create_rectangle(x0-r,y0-r,x0+r,y0+r,fill='light blue')
        canvas.create_rectangle(x0-r//2,y0-r//2,x0+r//2,y0+r//2,fill='purple')
    else:
        canvas.create_rectangle(x0-r,y0-r,x0+r,y0+r,fill='purple')
    canvas.create_text(app.width//2,app.height*0.1, fill = 'white', 
                       text = f'Boss lives: {boss.lives}')

#draws the bomb
def drawBomb(app,canvas):
    for bomb in app.bomb:
        x0 = bomb.cx - bomb.r
        x1 = bomb.cx + bomb.r
        y0 = bomb.cy - bomb.r
        y1 = bomb.cy + bomb.r
        canvas.create_oval(x0,y0,x1,y1, fill = bomb.colour)


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