Project Name: Galaga
Programming Language: Python

Project Description: 
Galaga is a classic space shooter and this is my take on it.The player will directly control a spaceship, 
and face enemy spaceships in a series of rounds, culminating in a final round where the player will face 
a boss ship. The player wins if they manage to complete all rounds while making sure the number of lives 
they have left never falls to zero.

Features:
Enemies evade shots
Enemies move in a leader flock (which itself moves randomly) using a modified leader led implementation
of boids algorithm
Round 6 is a boss battle. The boss has a shield, multiple lives, and fires a bomb in addition to lasers
Difficulty scales based on player's hit ratio



How to run the project:
1. Download all files to a sigle folder (especially cmu_112_grpahics and TP3)
2. Run TP3 in an editor


Libraries to be installed:
None, as far as I know. This should be able to run with cmu_112_graphics alone


Shortcut commands:

Most shortcut commands are parameters in appStarted and are as such:

1. r. This is the round number. To initiate round x (note there are only 6 rounds), let r=x
   example: r=5 and running will cause round 5 to be initiated. r=6 and running will cause the boss round to start

2. lasersFired and hits. These two work in tandem. hitRatio = hits/lasersFired.
   Enemies scale based on hitRatio. hitRatio>=30 means enemies are half the size. 
                                    hitRatio>=40 means enemy fire is twice as intense
   Enter values for lasersFired and hits such that these criteria are met

3. lives. To give yourself as many lives as you want, let the lives parameter in appStarted be any positive integer

4. app.numStars. This is not a parameter but a variable set in appStarted. This controls the number of stars in
   the background of the game. Set it to whatever you want to have that many stars in the background.
   Note: If the game is running slow, you may be able to speed it up by letting app.numStars = 0 and commenting out
         the starProcesses function in timerFired

