// from client_side.client_define import *
// from client_side.vec2 import *
// import client_side.hitbox as hitbox
// import client_side.team as team
// import client_side.paddle as paddle
// import client_side.ball as ball

// import pygame as pg
// import random
// import time
// import sys


function createWall(x, y, w, h, color)
{
	halfW = w / 2
	halfH = h / 2

	hit = hitbox.Hitbox(x, y, HITBOX_WALL_COLOR, color)
	hit.addPoint(-halfW, -halfH)
	hit.addPoint(halfW, -halfH)
	hit.addPoint(halfW, halfH)
	hit.addPoint(-halfW, halfH)

	return hit
}


function createObstacle(x, y, listPoint, color)
{
	hit = hitbox.Hitbox(x, y, HITBOX_WALL_COLOR, color)

	for (const p of listPoint)
		hit.addPoint(p[0], p[1])

	return hit
}



class GameClient {
	constructor()
	{
		/*
		This method define all variables needed by the program
		*/
		// Init pygame
		// pg.init()


		// We remove the toolbar of the window's height
		this.winSize = ((WIN_WIDTH, WIN_HEIGHT))
		// We create the window
		this.win = pg.display.set_mode(this.winSize, pg.RESIZABLE)

		this.clock = pg.time.Clock() // The clock be used to limit our fps
		this.fps = 60
		this.time = 0

		this.last = time.time()

		this.runMainLoop = true

		this.inputWait = 0

		// Creation of state list for player keys
		this.paddlesKeyState = PADDLES_KEYS_STATE.copy()

		// Team creation
		this.teamLeft = team.Team(0, TEAM_LEFT)
		this.teamRight = team.Team(0, TEAM_RIGHT)

		// Ball creation
		this.balls = [ball.Ball(WIN_WIDTH / 2, WIN_HEIGHT / 2)]

		// Ball begin left side
		if (random.random() > 0.5)
			this.balls[0].lastPaddleHitId = random.choice(this.teamLeft.paddles).id
		// Ball begin right side
		else
		{
			this.balls[0].lastPaddleHitId = random.choice(this.teamRight.paddles).id
			this.balls[0].direction = Vec2(-1, 0)
			this.balls[0].lastPaddleTeam = TEAM_RIGHT
		}

		// Power up creation
		this.powerUpEnable = False
		this.powerUp = [POWER_UP_SPAWN_COOLDOWN, hitbox.Hitbox(0, 0, (0, 0, 200), POWER_UP_HITBOX_COLOR), -1]
		for ( const p of ball.getPointOfCircle(POWER_UP_HITBOX_RADIUS, POWER_UP_HITBOX_PRECISION, 0))
			this.powerUp[1].addPoint(p[0], p[1])

		// Walls creation
		this.walls = []

		// idPaddle, paddleTeam, Ball speed, Number of bounce, CC, Perfect shoot, time of goal
		this.goals = []

		this.ballNumber = 0

		// For communications
		// (Message type, message content)
		this.messageForServer = []
		// (Message type, message content)
		this.messageFromServer = []
	}

	run()
	{
		//TODO change content to adapt
		/*
		This method is the main loop of the game
		*/

		// Game loop
		while (this.runMainLoop)
		{
			this.input()
			this.tick()
			this.render()
			this.clock.tick(this.fps)
		}
	}


	step()
	{
		/*
		This method is the main function of the game
		Call it in a while, it need to be re call until this.runMainLoop equals to False
		*/
		// Clear the message for server
		this.messageForServer.clear()

		this.parseMessageFromServer()
		// Game loop
		if (this.runMainLoop)
		{
			this.input()
			this.tick()
			this.render()
		}
			// this.clock.tick(this.fps)

		// After compute it, clear message from the server
		this.messageFromServer.clear()
	}


	input()
	{
		//TODO change to accept our input

		/*
		The method catch user's inputs, as key presse or a mouse click
		*/
		// We check each event
		for (const event of pg.event.get())
		{
			// If the event it a click on the top right cross, we quit the game
			if (event.type == pg.QUIT)
				this.runMainLoop = False
		}

		this.keyboardState = pg.key.get_pressed()
		this.mouseState = pg.mouse.get_pressed()
		this.mousePos = pg.mouse.get_pos()

		// Press espace to quit
		if (this.keyboardState[pg.K_ESCAPE])
			this.runMainLoop = False

		// Update paddles keys
		for (let i = 0; i < 4; i++)
		{
			// {id_paddle, id_key, key_action [true = press, False = release]}
			templateContent = {"paddleId" : i, "keyId" : 0, "keyAction" : true}

			if (this.keyboardState[PLAYER_KEYS[i][KEY_UP]] && ! this.paddlesKeyState[i * 4 + KEY_UP])
			{
				this.paddlesKeyState[i * 4 + KEY_UP] = true
				content = templateContent.copy()
				content["keyId"] = KEY_UP
				content["keyAction"] = true
				this.messageForServer.append((CLIENT_MSG_TYPE_USER_EVENT, content))
			}
			else if (! this.keyboardState[PLAYER_KEYS[i][KEY_UP]] && this.paddlesKeyState[i * 4 + KEY_UP])
			{
				this.paddlesKeyState[i * 4 + KEY_UP] = False
				content = templateContent.copy()
				content["keyId"] = KEY_UP
				content["keyAction"] = False
				this.messageForServer.append((CLIENT_MSG_TYPE_USER_EVENT, content))
			}

			if (this.keyboardState[PLAYER_KEYS[i][KEY_DOWN]] && ! this.paddlesKeyState[i * 4 + KEY_DOWN])
			{
				this.paddlesKeyState[i * 4 + KEY_DOWN] = true
				content = templateContent.copy()
				content["keyId"] = KEY_DOWN
				content["keyAction"] = true
				this.messageForServer.append((CLIENT_MSG_TYPE_USER_EVENT, content))
			}
			else if (! this.keyboardState[PLAYER_KEYS[i][KEY_DOWN]] && this.paddlesKeyState[i * 4 + KEY_DOWN])
			{
				this.paddlesKeyState[i * 4 + KEY_DOWN] = False
				content = templateContent.copy()
				content["keyId"] = KEY_DOWN
				content["keyAction"] = False
				this.messageForServer.append((CLIENT_MSG_TYPE_USER_EVENT, content))
			}

			if (this.keyboardState[PLAYER_KEYS[i][KEY_POWER_UP]] && ! this.paddlesKeyState[i * 4 + KEY_POWER_UP])
			{
				this.paddlesKeyState[i * 4 + KEY_POWER_UP] = true
				content = templateContent.copy()
				content["keyId"] = KEY_POWER_UP
				content["keyAction"] = true
				this.messageForServer.append((CLIENT_MSG_TYPE_USER_EVENT, content))
			}
			else if (! this.keyboardState[PLAYER_KEYS[i][KEY_POWER_UP]] && this.paddlesKeyState[i * 4 + KEY_POWER_UP])
			{
				this.paddlesKeyState[i * 4 + KEY_POWER_UP] = False
				content = templateContent.copy()
				content["keyId"] = KEY_POWER_UP
				content["keyAction"] = False
				this.messageForServer.append((CLIENT_MSG_TYPE_USER_EVENT, content))
			}

			if (this.keyboardState[PLAYER_KEYS[i][KEY_LAUNCH_BALL]] && ! this.paddlesKeyState[i * 4 + KEY_LAUNCH_BALL])
			{
				this.paddlesKeyState[i * 4 + KEY_LAUNCH_BALL] = true
				content = templateContent.copy()
				content["keyId"] = KEY_LAUNCH_BALL
				content["keyAction"] = true
				this.messageForServer.append((CLIENT_MSG_TYPE_USER_EVENT, content))
			}
			else if (! this.keyboardState[PLAYER_KEYS[i][KEY_LAUNCH_BALL]] && this.paddlesKeyState[i * 4 + KEY_LAUNCH_BALL])
			{
				this.paddlesKeyState[i * 4 + KEY_LAUNCH_BALL] = False
				content = templateContent.copy()
				content["keyId"] = KEY_LAUNCH_BALL
				content["keyAction"] = False
				this.messageForServer.append((CLIENT_MSG_TYPE_USER_EVENT, content))
			}
		}
	}


	tick()
	{
		/*
		This is the method where all calculations will be done
		*/
		tmp = time.time()
		delta = tmp - this.last
		this.last = tmp

		this.time += delta

		// Check if ball move. If no ball move, all time base event are stopping
		updateTime = False
		for (const b of this.balls)
		{
			if (b.state == STATE_RUN)
			{
				updateTime = true
				break
			}
		}
		if (this.inputWait > 0)
		{
			this.inputWait -= delta
			if (this.inputWait < 0)
				this.inputWait = 0
		}

		if (! updateTime && this.powerUp[0] != POWER_UP_SPAWN_COOLDOWN)
			this.powerUp[0] = POWER_UP_SPAWN_COOLDOWN

		this.teamLeft.tick(delta, this.paddlesKeyState, updateTime)
		this.teamRight.tick(delta, this.paddlesKeyState, updateTime)

		for (const b of this.balls)
		{
			b.updatePosition(delta, this.teamLeft.paddles, this.teamRight.paddles, this.walls, this.powerUp)
			if (updateTime)
				b.updateTime(delta)
		}

		pg.display.set_caption("time : " + str(this.time))
	}


	render(){
		/*
		This is the method where all graphic update will be done
		*/
		// We clean our screen with one color
		this.win.fill((0, 0, 0))

		// Draw area
		// pg.draw.rect(this.win, AREA_COLOR, AREA_RECT)
		pg.draw.rect(this.win, AREA_TEAM_COLOR, AREA_LEFT_TEAM_RECT)
		pg.draw.rect(this.win, AREA_COLOR, AREA_MIDDLE_RECT)
		pg.draw.rect(this.win, AREA_TEAM_COLOR, AREA_RIGTH_TEAM_RECT)

		// Draw walls
		for (const w of this.walls)
		{
			w.drawFill(this.win)
			if (DRAW_HITBOX)
				w.draw(this.win)
		}

		// Power up draw
		if (this.powerUp[0] == POWER_UP_VISIBLE)
		{
			this.powerUp[1].drawFill(this.win)
			if (DRAW_HITBOX)
				this.powerUp[1].draw(this.win)
		}

		// Draw ball
		for (const b of this.balls)
			b.draw(this.win)

		// Draw team
		this.teamLeft.draw(this.win, this.powerUpEnable)
		this.teamRight.draw(this.win, this.powerUpEnable)

		// We update the drawing.
		// Before the function call, any changes will be not visible
		pg.display.update()}


	quit()
	{
		/*
		This is the quit method
		*/
		// Pygame quit
		this.runMainLoop = False
		pg.quit()
	}


	parseMessageFromServer()
	{
		for (const message of this.messageFromServer)
		{
			if (message[0] == SERVER_MSG_TYPE_CREATE_START_INFO)
				this.parseMessageStartInfo(message[1])
			else if (message[0] == SERVER_MSG_TYPE_UPDATE_OBSTACLE)
				this.parseMessageForObstacle(message[1])
			else if (message[0] == SERVER_MSG_TYPE_UPDATE_PADDLES)
				this.parseMessageForPaddles(message[1])
			else if (message[0] == SERVER_MSG_TYPE_UPDATE_BALLS)
				this.parseMessageForBalls(message[1])
			else if (message[0] == SERVER_MSG_TYPE_DELETE_BALLS)
				this.parseMessageForDeleteBalls(message[1])
			else if (message[0] == SERVER_MSG_TYPE_UPDATE_POWER_UP)
				this.parseMessageForPowerUp(message[1])
			else if (message[0] == SERVER_MSG_TYPE_SCORE_UPDATE)
				this.parseMessageForScore(message[1])
		}
	}


	parseMessageStartInfo( messageContent)
	{
		// Content of obstacles :
		// {
		// 	obstables : [ {position:[x, y], points:[[x, y]], color:(r, g, b)} ]
		// 	powerUp : true or False
		// }
		this.walls.clear()

		for (const content of messageContent["obstacles"])
		{
			x = AREA_RECT[0] + content["position"][0]
			y = AREA_RECT[1] + content["position"][1]
			obstacle = createObstacle(x, y, content["points"], content["color"])
			this.walls.append(obstacle)
		}
		this.powerUpEnable = messageContent["powerUp"]
	}


	parseMessageForObstacle( messageContent){
		// Content of obstacles :
		// [
		// 	{id, position, points:[[x, y]]}
		// ]
		for (const content of messageContent)
		{
			this.walls[content["id"]].setPos(vec2Add(Vec2(content["position"][0], content["position"][1]), Vec2(AREA_RECT[0], AREA_RECT[1])))
			this.walls[content["id"]].clearPoints()
			this.walls[content["id"]].addPoints(content["points"])
		}
	}

	parseMessageForPaddles( messageContent)
	{
		// Content of paddles :
		// [
		// 	{id_paddle, id_team, position:[x, y], modifierSize, powerUp, powerUpInCharge}
		// ]
		for (const content of messageContent)
		{
			x = AREA_RECT[0] + content["position"][0]
			y = AREA_RECT[1] + content["position"][1]

			if (content["id_team"] == TEAM_LEFT)
			{
				if (content["id_paddle"] >= len(this.teamLeft.paddles))
				{
					while (content["id_paddle"] > len(this.teamLeft.paddles))
						this.teamLeft.paddles.append(paddle.Paddle(0, 0, len(this.teamLeft.paddles), TEAM_LEFT))
					this.teamLeft.paddles.append(paddle.Paddle(0, 0, content["id_paddle"], TEAM_LEFT))
				}
				this.teamLeft.paddles[content["id_paddle"]].setPos(x, y)
				if (this.teamLeft.paddles[content["id_paddle"]].modifierSize != content["modifierSize"])
					this.teamLeft.paddles[content["id_paddle"]].modifySize(content["modifierSize"])
				this.teamLeft.paddles[content["id_paddle"]].powerUp = content["powerUp"]
				this.teamLeft.paddles[content["id_paddle"]].powerUpInCharge = content["powerUpInCharge"]
			}
			else
			{
				if (content["id_paddle"] >= len(this.teamRight.paddles))
				{
					while (content["id_paddle"] > len(this.teamRight.paddles))
						this.teamRight.paddles.append(paddle.Paddle(0, 0, len(this.teamRight.paddles), TEAM_RIGHT))
					this.teamRight.paddles.append(paddle.Paddle(0, 0, content["id_paddle"], TEAM_RIGHT))
				}
				this.teamRight.paddles[content["id_paddle"]].setPos(x, y)
				if (this.teamRight.paddles[content["id_paddle"]].modifierSize != content["modifierSize"])
					this.teamRight.paddles[content["id_paddle"]].modifySize(content["modifierSize"])
				this.teamRight.paddles[content["id_paddle"]].powerUp = content["powerUp"]
				this.teamRight.paddles[content["id_paddle"]].powerUpInCharge = content["powerUpInCharge"]
			}
		}
	}

	parseMessageForBalls( messageContent)
	{
		// Content of balls :
		// [
		// 	{position:[x, y], direction:[x, y], speed, radius, state, last_paddle_hit_info:[id, team], modifier_state}
		// ]
		i = 0
		numberOfMessageBall = len(messageContent)
		while (i < numberOfMessageBall)
		{
			content = messageContent[i]
			x = AREA_RECT[0] + content["position"][0]
			y = AREA_RECT[1] + content["position"][1]

			// Update ball if exist
			if (i < len(this.balls))
			{
				b = this.balls[i]
				b.pos.x = x
				b.pos.y = y
				b.hitbox.setPos(Vec2(x, y))
				b.direction = Vec2(content["direction"][0], content["direction"][1])
				b.speed = content["speed"]
				b.radius = content["radius"]
				b.state = content["state"]
				b.lastPaddleHitId = content["last_paddle_hit_info"][0]
				b.lastPaddleTeam = content["last_paddle_hit_info"][1]
				b.setModifierByState(content["modifier_state"])
			}

			// Create a new one instead
			else
			{
				b = ball.Ball(x, y)
				b.direction = Vec2(content["direction"][0], content["direction"][1])
				b.speed = content["speed"]
				b.radius = content["radius"]
				b.state = content["state"]
				b.lastPaddleHitId = content["last_paddle_hit_info"][0]
				b.lastPaddleTeam = content["last_paddle_hit_info"][1]
				b.setModifierByState(content["modifier_state"])
				this.balls.append(b)

			i += 1
		}
		}
	}

	parseMessageForDeleteBalls( messageContent)
	{
		// Content of delete balls :
		// [id_ball]
		for (let i = 0; i < messageContent.length; i++) {
			this.balls.pop(messageContent[i] - i)
		}
	}


	parseMessageForPowerUp( messageContent)
	{
		// Content of balls :
		// {position:[x, y], state}
		x = AREA_RECT[0] + messageContent["position"][0]
		y = AREA_RECT[1] + messageContent["position"][1]

		this.powerUp[0] = messageContent["state"]
		this.powerUp[1].setPos(Vec2(x, y))
	}


	parseMessageForScore( messageContent)
	{
		// Content of power up :
		// {leftTeam, rightTeam}
		this.teamLeft.score = messageContent["leftTeam"]
		this.teamRight.score = messageContent["rightTeam"]
	}
}