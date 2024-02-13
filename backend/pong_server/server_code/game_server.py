from define import *
from server_code.vec2 import *
import server_code.hitbox as hitbox
import server_code.team as team
import server_code.ball as ball
import server_code.obstacle as obstacle
import server_code.ia as ia

import random
import time


def createWallObstacle(x, y, w, h, color, routine=[]) -> hitbox.Hitbox:
    obs = obstacle.Obstacle(x, y, color)
    obs.createWallHitbox(w, h)
    obs.addRoutine(routine)

    return obs


def createPolygonObstacle(x:int, y:int, listPoint:list, color, routine=[]) -> hitbox.Hitbox:
    obs = obstacle.Obstacle(x, y, color)
    obs.createPolygonHitbox(listPoint)
    obs.addRoutine(routine)

    return obs


def createCircleObstacle(x:int, y:int, radius:int, precision:int, color, routine=[]) -> hitbox.Hitbox:
    obs = obstacle.Obstacle(x, y, color)
    obs.createCircleHitbox(radius, precision)
    obs.addRoutine(routine)

    return obs



class GameServer:
    def __init__(self, powerUpEnable, paddles_left, paddles_right, idMap):
        """
        This method define all variables needed by the program
        """
        self.fps = 60
        self.time = 0

        self.last = time.time()
        self.delta = 1 / 60

        self.runMainLoop = True

        self.inputWait = 0

        # Creation of state list for player keys
        self.paddlesKeyState = PADDLES_KEYS_STATE.copy()

        # Team creation
        self.teamLeft = team.Team(len(paddles_left), TEAM_LEFT)
        self.teamRight = team.Team(len(paddles_right), TEAM_RIGHT)

        # Ball creation
        self.balls = [ball.Ball(0, 0)]

        # IA creation
        self.iaTimer = 0
        self.iaList = []
        for i in range(len(paddles_left)):
            if paddles_left[i] == PADDLE_IA:
                self.iaList.append(ia.Ia(TEAM_LEFT, i))
        for i in range(len(paddles_right)):
            if paddles_right[i] == PADDLE_IA:
                self.iaList.append(ia.Ia(TEAM_RIGHT, i))

        # Ball begin left side
        if random.random() > 0.5:
            self.balls[0].lastPaddleHitId = random.choice(self.teamLeft.paddles).id
        # Ball begin right side
        else:
            self.balls[0].lastPaddleHitId = random.choice(self.teamRight.paddles).id
            self.balls[0].direction = Vec2(-1, 0)
            self.balls[0].lastPaddleTeam = TEAM_RIGHT

        # Power up creation
        self.powerUpEnable = powerUpEnable
        # {state, hitbox, paddleWhoGet:[id, team]}
        self.powerUp = {"state" : POWER_UP_SPAWN_COOLDOWN, "hitbox" : hitbox.Hitbox(0, 0, (0, 0, 0)), "paddleWhoGet" : (-1, -1)}
        for p in ball.getPointOfCircle(POWER_UP_HITBOX_RADIUS, POWER_UP_HITBOX_PRECISION, 0):
            self.powerUp["hitbox"].addPoint(p[0], p[1])

        # Walls creation
        self.createMap(idMap)

        # idPaddle, paddleTeam, Ball speed, Number of bounce, CC, Perfect shoot, time of goal
        self.goals = []

        self.ballNumber = 0

        # For communications
        self.timeBeforeUpdateClient = TIME_SEND_UPDATE_INFO_TO_CLIENT
        # (Message type, message content)
        self.messageForClients = []
        # (Message type, message content)
        self.messageFromClients = []

        self.createMessageStartInfo()


    def run(self):
        """
        This method is the main loop of the game
        """
        # Game loop
        targetTime = 1 / self.fps
        while self.runMainLoop:
            self.input()
            self.tick()
            timeToSleep = max(0, targetTime - self.delta)
            time.sleep(timeToSleep)


    def step(self):
        """
        This method is the main function of the game
        Call it in a while, it need to be re call until self.runMainLoop equals to False
        """
        # Clear the message for server
        self.messageForClients.clear()

        # Game loop
        if self.runMainLoop:
            self.input()
            self.tick()

        # After compute it, clear message from the server
        self.messageFromClients.clear()

        self.timeBeforeUpdateClient -= self.delta
        if self.timeBeforeUpdateClient <= 0:
            # Create new message for clients
            self.createMessageUpdateObstacle()
            self.createMessageInfoPaddles()
            self.createMessageInfoBalls()
            if self.powerUpEnable:
                self.createMessageInfoPowerUp()
            self.timeBeforeUpdateClient = TIME_SEND_UPDATE_INFO_TO_CLIENT


    def input(self):
        """
        The method catch user's inputs, as key presse or a mouse click
        """
        # Pass input recieved from client
        for message in self.messageFromClients:
            if message[0] == CLIENT_MSG_TYPE_USER_EVENT:
                content = message[1]
                # Content of user event :
                # # {id_paddle, id_key, key_action [True = press, False = release]}
                self.paddlesKeyState[content["id_paddle"] * 4 + content["id_key"]] = content["key_action"]


    def tick(self):
        """
        This is the method where all calculations will be done
        """
        tmp = time.time()
        self.delta = tmp - self.last
        self.last = tmp

        self.time += self.delta

        # Update timers
        if self.inputWait > 0:
            self.inputWait -= self.delta
            if self.inputWait < 0:
                self.inputWait = 0

        if self.iaTimer > 0:
            self.iaTimer -= self.delta
            if self.iaTimer < 0:
                self.iaTimer = 0

        # Check if ball move. If no ball move, all time base event are stopping
        updateTime = False
        numberOfBall = len(self.balls)
        for i in range(numberOfBall):
            if self.balls[i].state == STATE_RUN:
                updateTime = True
                break

        # For stats
        if numberOfBall > self.ballNumber:
            self.ballNumber = numberOfBall

        # Update power up
        if self.powerUpEnable and not updateTime and self.powerUp["state"] != POWER_UP_SPAWN_COOLDOWN:
            self.powerUp["state"] = POWER_UP_SPAWN_COOLDOWN

        if self.powerUpEnable and updateTime and self.powerUp["state"] > POWER_UP_VISIBLE:
            self.powerUp["state"] -= self.delta
            if self.powerUp["state"] <= POWER_UP_VISIBLE:
                self.powerUp["state"] = POWER_UP_VISIBLE
                self.createPowerUp()

        # Update walls routine
        for w in self.walls:
            w.updateRoutine(self.delta)

        # Ia tick
        for ia in self.iaList:
            if self.iaTimer == 0:
                ia.updateGameEnvironement(self.walls, self.teamLeft.paddles, self.teamRight.paddles, self.balls, self.powerUp)
            ia.tick(self.delta)
            self.paddlesKeyState[ia.globalId * 4 + KEY_UP] = ia.keyToEmulate[KEY_UP]
            self.paddlesKeyState[ia.globalId * 4 + KEY_DOWN] = ia.keyToEmulate[KEY_DOWN]
            self.paddlesKeyState[ia.globalId * 4 + KEY_POWER_UP] = ia.keyToEmulate[KEY_POWER_UP]
            self.paddlesKeyState[ia.globalId * 4 + KEY_LAUNCH_BALL] = ia.keyToEmulate[KEY_LAUNCH_BALL]

        if self.iaTimer == 0:
            self.iaTimer = IA_COOLDOWN_GET_GAME_STATE

        # Paddles tick
        self.teamLeft.tick(self.delta, self.paddlesKeyState, updateTime)
        self.teamRight.tick(self.delta, self.paddlesKeyState, updateTime)

        # Balls tick
        ballToDelete = []
        for i in range(len(self.balls)):
            b = self.balls[i]
            b.updatePosition(self.delta, self.teamLeft.paddles, self.teamRight.paddles, self.walls, self.powerUp)
            if updateTime:
                b.updateTime(self.delta)

            # if the ball is in left goal
            if b.state == STATE_IN_GOAL_LEFT:
                self.ballInLeftGoal(b, i, ballToDelete)
                self.createMessageInfoScore()

            # if the ball is in right goal
            elif b.state == STATE_IN_GOAL_RIGHT:
                self.ballInRightGoal(b, i, ballToDelete)
                self.createMessageInfoScore()

            # case of ball follow player
            elif b.state == STATE_IN_FOLLOW:
                if b.lastPaddleTeam == TEAM_LEFT:
                    pad = self.teamLeft.paddles[b.lastPaddleHitId]
                else:
                    pad = self.teamRight.paddles[b.lastPaddleHitId]
                b.setPos(pad.pos.dup())
                b.pos.translateAlong(b.direction.dup(), PADDLE_WIDTH * 2)
                id = pad.id
                if pad.team == TEAM_RIGHT:
                    id += TEAM_MAX_PLAYER
                if self.paddlesKeyState[id * 4 + KEY_LAUNCH_BALL] and pad.waitLaunch == 0:
                    b.state = STATE_RUN
                    pad.waitLaunch = PADDLE_LAUNCH_COOLDOWN

            # case of ball is Moving
            else:
                for w in self.walls:
                    # if not b.modifierSkipCollision and b.hitbox.isInside(w) and not b.hitbox.isCollide(w):
                    if not b.modifierSkipCollision and b.hitbox.isInside(w.hitbox):
                        outOfCenter = vec2Sub(b.pos, w.hitbox.pos)
                        if outOfCenter.norm() == 0:
                            outOfCenter = Vec2(1, 0)
                        outOfCenter.normalize()
                        b.direction = outOfCenter
                        if not b.hitbox.isCollide(w.hitbox):
                            dir = outOfCenter.dup()
                            dir.multiply(BALL_RADIUS * 2 + 5)
                            pos = vec2Add(b.pos, dir)
                            b.setPos(pos)

        numberOfBallToDelete = len(ballToDelete)
        if numberOfBallToDelete > 0:
            self.createMessageDeleteBalls(ballToDelete)
            for i in range(numberOfBallToDelete):
                self.balls.pop(ballToDelete[i] - i)

        # Verify if power can be use, and use it if possible
        if self.powerUpEnable and updateTime:
            self.checkPowerUp(self.teamLeft, LEFT_TEAM_RECT, self.teamRight, RIGTH_TEAM_RECT)
            self.checkPowerUp(self.teamRight, RIGTH_TEAM_RECT, self.teamLeft, LEFT_TEAM_RECT)

            if self.powerUp["state"] == POWER_UP_TAKE:
                # Generate power up
                powerUp = random.randint(0, 12)
                if self.powerUp["paddleWhoGet"][1] == TEAM_LEFT:
                    self.teamLeft.paddles[self.powerUp["paddleWhoGet"][0]].powerUp = powerUp
                else:
                    self.teamRight.paddles[self.powerUp["paddleWhoGet"][0]].powerUp = powerUp
                self.powerUp["state"] = POWER_UP_SPAWN_COOLDOWN

        if self.teamLeft.score >= TEAM_WIN_SCORE or self.teamRight.score >= TEAM_WIN_SCORE:
            self.printFinalStat()


    def quit(self):
        """
        This is the quit method
        """
        self.runMainLoop = False


    def createPowerUp(self):
        collide = True

        while collide:
            collide = False

            x = random.randint(LEFT_TEAM_RECT[0] + LEFT_TEAM_RECT[2], RIGTH_TEAM_RECT[0])
            y = random.randint(0, AREA_SIZE[1])

            self.powerUp["hitbox"].setPos(Vec2(x, y))

            for w in self.walls:
                collide = self.powerUp["hitbox"].isInsideSurrondingBox(w.hitbox)
                if collide:
                    break


    def checkPowerUp(self, team:team.Team, teamArea:tuple, ennemyTeam:team.Team, ennemyTeamArea:tuple):
        teamAreaNoBall = True
        ennemyTeamAreaNoBall = True

        for b in self.balls:
            if b.state == STATE_RUN:
                if b.pos.x >= teamArea[0] and b.pos.x <= teamArea[0] + teamArea[2]:
                    teamAreaNoBall = False
                elif b.pos.x >= ennemyTeamArea[0] and b.pos.x <= ennemyTeamArea[0] + ennemyTeamArea[2]:
                    ennemyTeamAreaNoBall = False

                if not teamAreaNoBall and not ennemyTeamAreaNoBall:
                    break

        ballPowerUp = []

        # powerUpTryUse = [power up id, paddle id, power up used (bool)]
        for powerUpTryUse in team.powerUpTryUse:
            if powerUpTryUse[0] == POWER_UP_BALL_FAST:
                if teamAreaNoBall:
                    powerUpTryUse[2] = True

            elif powerUpTryUse[0] == POWER_UP_BALL_WAVE:
                if teamAreaNoBall:
                    powerUpTryUse[2] = True

            elif powerUpTryUse[0] == POWER_UP_BALL_INVISIBLE:
                if teamAreaNoBall:
                    powerUpTryUse[2] = True

            elif powerUpTryUse[0] == POWER_UP_BALL_NO_COLLISION:
                ballPowerUp.append(POWER_UP_BALL_NO_COLLISION)
                powerUpTryUse[2] = True

            elif powerUpTryUse[0] == POWER_UP_DUPLICATION_BALL:
                if ennemyTeamAreaNoBall:
                    newBalls = []
                    for b in self.balls:
                        if b.state == STATE_RUN:
                            newBalls.append(b.dup())
                    self.balls.extend(newBalls)
                    powerUpTryUse[2] = True

            elif powerUpTryUse[0] == POWER_UP_BALL_SLOW:
                ballPowerUp.append(POWER_UP_BALL_SLOW)
                powerUpTryUse[2] = True

            elif powerUpTryUse[0] == POWER_UP_BALL_STOP:
                ballPowerUp.append(POWER_UP_BALL_STOP)
                powerUpTryUse[2] = True

            elif powerUpTryUse[0] == POWER_UP_BALL_BIG:
                ballPowerUp.append(POWER_UP_BALL_BIG)
                powerUpTryUse[2] = True

            elif powerUpTryUse[0] == POWER_UP_BALL_LITTLE:
                ballPowerUp.append(POWER_UP_BALL_LITTLE)
                powerUpTryUse[2] = True

            elif powerUpTryUse[0] == POWER_UP_PADDLE_FAST:
                ennemyTeam.applyPowerUpToPaddles(POWER_UP_PADDLE_FAST)
                powerUpTryUse[2] = True

            elif powerUpTryUse[0] == POWER_UP_PADDLE_SLOW:
                ennemyTeam.applyPowerUpToPaddles(POWER_UP_PADDLE_SLOW)
                powerUpTryUse[2] = True

            elif powerUpTryUse[0] == POWER_UP_PADDLE_BIG:
                team.applyPowerUpToPaddles(POWER_UP_PADDLE_BIG)
                powerUpTryUse[2] = True

            elif powerUpTryUse[0] == POWER_UP_PADDLE_LITTLE:
                ennemyTeam.applyPowerUpToPaddles(POWER_UP_PADDLE_LITTLE)
                powerUpTryUse[2] = True

        for b in self.balls:
            for powerUp in ballPowerUp:
                if powerUp == POWER_UP_BALL_NO_COLLISION:
                    b.modifierSkipCollision = True
                elif powerUp == POWER_UP_BALL_SLOW:
                    b.addPowerUpEffect(POWER_UP_BALL_SLOW)
                elif powerUp == POWER_UP_BALL_STOP:
                    b.modifierStopBallTimer += POWER_UP_BALL_STOP_TIMER_EFFECT
                elif powerUp == POWER_UP_BALL_BIG:
                    b.addPowerUpEffect(POWER_UP_BALL_BIG)
                elif powerUp == POWER_UP_BALL_LITTLE:
                    b.addPowerUpEffect(POWER_UP_BALL_LITTLE)


    def ballInLeftGoal(self, ball:ball.Ball, i:int, ballToDelete:list):
        self.teamRight.score += 1
        # for stats
        contreCamp = False
        if ball.lastPaddleTeam == TEAM_LEFT:
            paddle = self.teamLeft.paddles[ball.lastPaddleHitId]
            paddle.numberOfContreCamp += 1
            contreCamp = True
        else:
            paddle = self.teamRight.paddles[ball.lastPaddleHitId]
        paddle.numberOfGoal += 1

        if ball.numberOfBounce > paddle.maxBounceBallGoal:
            paddle.maxBounceBallGoal = ball.numberOfBounce

        perfectShoot = False
        if ball.pos.y < PERFECT_SHOOT_SIZE or ball.pos.y > AREA_SIZE[1] - PERFECT_SHOOT_SIZE:
            paddle.numberOfPerfectShoot += 1
            perfectShoot = True

        # idPaddle, paddleTeam, Ball speed, Number of bounce, CC, Perfect shoot, time of goal
        self.goals.append((paddle.id, paddle.team, ball.speed, ball.numberOfBounce, contreCamp, perfectShoot, self.time))

        if self.powerUpEnable:
            for p in self.teamLeft.paddles:
                p.powerUp = random.randint(0, 12)
                # p.powerUp = 12

        if len(self.balls) - len(ballToDelete) > 1:
            ballToDelete.append(i)
            return

        ball.direction = Vec2(1, 0)
        ball.speed = BALL_START_SPEED
        ball.state = STATE_IN_FOLLOW
        ball.modifierSkipCollision = False
        ball.lastPaddleHitId = random.choice(self.teamLeft.paddles).id
        ball.lastPaddleTeam = TEAM_LEFT


    def ballInRightGoal(self, ball:ball.Ball, i:int, ballToDelete:list):
        self.teamLeft.score += 1
        # for stats
        contreCamp = False
        if ball.lastPaddleTeam == TEAM_LEFT:
            paddle = self.teamLeft.paddles[ball.lastPaddleHitId]
        else:
            paddle = self.teamRight.paddles[ball.lastPaddleHitId]
            paddle.numberOfContreCamp += 1
            contreCamp = True
        paddle.numberOfGoal += 1
        if ball.numberOfBounce > paddle.maxBounceBallGoal:
            paddle.maxBounceBallGoal = ball.numberOfBounce

        perfectShoot = False
        if ball.pos.y < PERFECT_SHOOT_SIZE or ball.pos.y > AREA_SIZE[1] - PERFECT_SHOOT_SIZE:
            paddle.numberOfPerfectShoot += 1
            perfectShoot = True

        # idPaddle, paddleTeam, Ball speed, Number of bounce, CC, Perfect shoot, time of goal
        self.goals.append((paddle.id, paddle.team, ball.speed, ball.numberOfBounce, contreCamp, perfectShoot, self.time))

        if self.powerUpEnable:
            for p in self.teamRight.paddles:
                p.powerUp = random.randint(0, 12)

        if len(self.balls) - len(ballToDelete) > 1:
            ballToDelete.append(i)
            return

        ball.direction = Vec2(-1, 0)
        ball.speed = BALL_START_SPEED
        ball.state = STATE_IN_FOLLOW
        ball.modifierSkipCollision = False
        ball.lastPaddleHitId = random.choice(self.teamRight.paddles).id
        ball.lastPaddleTeam = TEAM_RIGHT


    def printFinalStat(self):
        if self.teamLeft.score > self.teamRight.score:
            print("Team left win !")
        else:
            print("Team right win !")

        print("=====================================")
        print("|             GAME STATS            |")
        print("=====================================")
        print("Team left score :", self.teamLeft.score)
        print("Team right score :", self.teamRight.score)
        print("Team left number of player :", len(self.teamLeft.paddles))
        print("Team right number of player :", len(self.teamRight.paddles))
        print("Number of ball :", self.ballNumber)
        print("Duration of match :", self.time)
        print()
        print("=====================================")
        print("|           PADDLES STATS           |")
        print("=====================================")
        print("Team left players :")
        print("\t----------------------------")
        for p in self.teamLeft.paddles:
            print("\tPaddle id :", p.id)
            print("\tNumber of goal :", p.numberOfGoal)
            print("\tMax speed ball touch :", p.maxSpeedBallTouch)
            print("\tMax bounce of goal ball :", p.maxBounceBallGoal)
            print("\tNumber of CC :", p.numberOfContreCamp)
            print("\tNumber of perfect shoot :", p.numberOfPerfectShoot)
            print("\t----------------------------")
        print("Team right players :")
        print("\t----------------------------")
        for p in self.teamRight.paddles:
            print("\tPaddle id :", p.id)
            print("\tNumber of goal :", p.numberOfGoal)
            print("\tMax speed ball touch :", p.maxSpeedBallTouch)
            print("\tMax bounce of goal ball :", p.maxBounceBallGoal)
            print("\tNumber of CC :", p.numberOfContreCamp)
            print("\tNumber of perfect shoot :", p.numberOfPerfectShoot)
            print("\t----------------------------")
        print()
        print("=====================================")
        print("|            BALLS STATS            |")
        print("=====================================")
        # idPaddle, paddleTeam, Ball speed, Number of bounce, CC, Perfect shoot, time of goal
        for goal in self.goals:
            print("Paddle id :", goal[0])
            print("Paddle team :", goal[1])
            print("Ball speed ball :", goal[2])
            print("Number of bounce :", goal[3])
            print("Is CC :", goal[4])
            print("Is Perfect Shoot :", goal[5])
            print("Time :", goal[6])
            print("----------------------------")

        self.quit()


    def createMessageStartInfo(self):
        # Content of obstacles :
        # {
        #     obstables : [ {position:[x, y], points:[[x, y]], color:(r, g, b)} ]
        #     powerUp : True or False
        # }
        content = {"obstacles" : [], "powerUp" : self.powerUpEnable}

        for wall in self.walls:
            obstacle = {"position" : wall.hitbox.pos.asTupple(),"points" : wall.hitbox.getPointsCenter(), "color" : wall.hitbox.color}
            content["obstacles"].append(obstacle)

        message = [SERVER_MSG_TYPE_CREATE_START_INFO, content]

        self.messageForClients.append(message)


    def createMessageUpdateObstacle(self):
        # Content of obstacles :
        # [
        #     {id, position, points:[[x, y]]}
        # ]
        content = []

        for i in range(len(self.walls)):
            wall = self.walls[i]
            if wall.numberOfRoutines != 0:
                obstacle = {"id" : i, "position" : wall.hitbox.pos.asTupple(), "points" : wall.hitbox.getPointsCenter()}
                content.append(obstacle)

        message = [SERVER_MSG_TYPE_UPDATE_OBSTACLE, content]

        self.messageForClients.append(message)


    def createMessageInfoPaddles(self):
        # Content of paddles :
        # [
        #     {id_paddle, id_team, position:[x, y], modifierSize, powerUp, powerUpInCharge}
        # ]
        content = []

        # Left team paddles
        for paddle in self.teamLeft.paddles:
            paddleInfo = {"id_paddle" : paddle.id, "id_team" : TEAM_LEFT, "position" : paddle.pos.asTupple(),
                             "modifierSize" : paddle.modifierSize, "powerUp" : paddle.powerUp, "powerUpInCharge" : paddle.powerUpInCharge.copy()}
            content.append(paddleInfo)

        # Right team paddles
        for paddle in self.teamRight.paddles:
            paddleInfo = {"id_paddle" : paddle.id, "id_team" : TEAM_RIGHT, "position" : paddle.pos.asTupple(),
                            "modifierSize" : paddle.modifierSize, "powerUp" : paddle.powerUp, "powerUpInCharge" : paddle.powerUpInCharge.copy()}
            content.append(paddleInfo)

        message = [SERVER_MSG_TYPE_UPDATE_PADDLES, content]

        self.messageForClients.append(message)


    def createMessageInfoBalls(self):
        # Content of balls :
        # [
        #     {position:[x, y], direction:[x, y], speed, radius, state, last_paddle_hit_info:[id, team], modifier_state}
        # ]
        content = []

        # Right team paddles
        for ball in self.balls:
            ballInfo = {"position" : ball.pos.asTupple(), "direction" : ball.direction.asTupple(), "speed" : ball.speed,
                             "radius" : ball.radius, "state" : ball.state, "last_paddle_hit_info" : [ball.lastPaddleHitId, ball.lastPaddleTeam],
                            "modifier_state" : ball.getModiferState()}
            content.append(ballInfo)

        message = [SERVER_MSG_TYPE_UPDATE_BALLS, content]

        self.messageForClients.append(message)


    def createMessageDeleteBalls(self, ballToDelete:list[int]):
        # Content of delete balls :
        # [id_ball]
        content = ballToDelete.copy()

        message = [SERVER_MSG_TYPE_DELETE_BALLS, content]

        self.messageForClients.append(message)


    def createMessageInfoPowerUp(self):
        # Content of power up :
        # {position:[x, y], state}
        content = {"position" : self.powerUp["hitbox"].pos.asTupple(), "state" :  self.powerUp["state"]}

        message = [SERVER_MSG_TYPE_UPDATE_POWER_UP, content]

        self.messageForClients.append(message)


    def createMessageInfoScore(self):
        # Content of power up :
        # {leftTeam, rightTeam}
        content = {"leftTeam" : self.teamLeft.score, "rightTeam" :  self.teamRight.score}

        message = [SERVER_MSG_TYPE_SCORE_UPDATE, content]

        self.messageForClients.append(message)


    def createMap(self, idMap:int):
        # Basic map
        self.walls = [
            # Wall up
            createWallObstacle(
                AREA_SIZE[0] / 2,
                 AREA_BORDER_SIZE / 2,
                AREA_SIZE[0],
                AREA_BORDER_SIZE * 2,
                (50, 50, 50)
            ),
            # Wall down
            createWallObstacle(
                AREA_SIZE[0] / 2,
                AREA_SIZE[1] - AREA_BORDER_SIZE / 2,
                AREA_SIZE[0],
                AREA_BORDER_SIZE * 2,
                (50, 50, 50)
            )
        ]

        #TODO removed at the end
        # idMap = 2

        if idMap == 1:
            self.walls.append(createPolygonObstacle(
                                AREA_SIZE[0] / 2,
                                0,
                                [(-300, 0), (300, 0), (275, 50), (75, 75), (0, 125), (-75, 75), (-275, 50)],
                                (200, 200, 0)
                            ))
            self.walls.append(createPolygonObstacle(
                                AREA_SIZE[0] / 2,
                                AREA_SIZE[1],
                                [(-300, 0), (300, 0), (275, -50), (0, -25), (-275, -50)],
                                (200, 200, 0)
                            ))
            self.walls.append(createCircleObstacle(
                                AREA_SIZE[0] / 2,
                                AREA_SIZE[1] / 2,
                                100,
                                32,
                                (200, 0, 200)
                            ))

        elif idMap == 2:
            self.walls.append(createPolygonObstacle(
                                AREA_SIZE[0] / 2,
                                0,
                                [(-300, 0), (300, 0), (275, 50), (75, 75), (0, 125), (-75, 75), (-275, 50)],
                                (200, 200, 0)
                            ))
            self.walls.append(createPolygonObstacle(
                                AREA_SIZE[0] / 2,
                                AREA_SIZE[1],
                                [(-300, 0), (300, 0), (275, -50), (0, -25), (-275, -50)],
                                (200, 200, 0)
                            ))
            self.walls.append(createCircleObstacle(
                                AREA_SIZE[0] / 2,
                                AREA_SIZE[1] / 2,
                                100,
                                32,
                                (200, 0, 200)
                            ))
            self.walls.append(createPolygonObstacle(
                                AREA_SIZE[0] / 2,
                                AREA_SIZE[1] / 2,
                                [(10, 200), (-10, 200), (-10, -200), (10, -200)],
                                (200, 0, 200),
                                [
                                    {"type" : OBSTACLE_ROUTINE_TYPE_ROTATION,
                                        "time" : OBSTACLE_ROUTINE_TIME_INFINITE,
                                        "effect" : 360}
                                ]
                            ))
            self.walls.append(createPolygonObstacle(
                                AREA_SIZE[0] / 2,
                                AREA_SIZE[1] / 2,
                                [(10, 200), (-10, 200), (-10, -200), (10, -200)],
                                (200, 0, 200),
                                [
                                    {"type" : OBSTACLE_ROUTINE_TYPE_ROTATION,
                                        "time" : OBSTACLE_ROUTINE_TIME_INFINITE,
                                        "effect" : -360}
                                ]
                            ))
            self.walls.append(createPolygonObstacle(
                                AREA_SIZE[0] / 3,
                                30,
                                [(-30, 0), (0, -30), (0, 30)],
                                (0, 200, 200),
                                [
                                    {"type" : OBSTACLE_ROUTINE_TYPE_TRANSLATION,
                                        "time" : 5,
                                        "effect" : Vec2(0, 168)},
                                    {"type" : OBSTACLE_ROUTINE_TYPE_TRANSLATION,
                                        "time" : 5,
                                        "effect" : Vec2(0, -168)}
                                ]
                            ))
            self.walls.append(createPolygonObstacle(
                                AREA_SIZE[0] / 3 * 2,
                                AREA_SIZE[1] - 30,
                                [(30, 0), (0, -30), (0, 30)],
                                (0, 200, 200),
                                [
                                    {"type" : OBSTACLE_ROUTINE_TYPE_TRANSLATION,
                                        "time" : 5,
                                        "effect" : Vec2(0, -168)},
                                    {"type" : OBSTACLE_ROUTINE_TYPE_TRANSLATION,
                                        "time" : 5,
                                        "effect" : Vec2(0, 168)}
                                ]
                            ))
            self.walls.append(createPolygonObstacle(
                                AREA_SIZE[0] / 3 * 2,
                                30,
                                [(-30, 0), (0, -30), (0, 30)],
                                (0, 200, 200),
                                [
                                    {"type" : OBSTACLE_ROUTINE_TYPE_TRANSLATION,
                                        "time" : 5,
                                        "effect" : Vec2(0, 168)},
                                    {"type" : OBSTACLE_ROUTINE_TYPE_TRANSLATION,
                                        "time" : 5,
                                        "effect" : Vec2(0, -168)}
                                ]
                            ))
            self.walls.append(createPolygonObstacle(
                                AREA_SIZE[0] / 3,
                                AREA_SIZE[1] - 30,
                                [(30, 0), (0, -30), (0, 30)],
                                (0, 200, 200),
                                [
                                    {"type" : OBSTACLE_ROUTINE_TYPE_TRANSLATION,
                                        "time" : 5,
                                        "effect" : Vec2(0, -168)},
                                    {"type" : OBSTACLE_ROUTINE_TYPE_TRANSLATION,
                                        "time" : 5,
                                        "effect" : Vec2(0, 168)}
                                ]
                            ))
        elif idMap == 3:
            self.walls.append(createPolygonObstacle(
                                1400,
                                399,
                                [(-45, -45), (45, -45), (45, 45), (-45, 45)],
                                (0, 200, 200)
                            ))

