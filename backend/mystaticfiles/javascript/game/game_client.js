import * as dc from "./client_define.js"
import * as d from "./define.js"
import {Vec2, vec2Add} from "./vec2.js"
import * as hitbox from "./hitbox.js"
import * as team from "./team.js"
import * as paddle from "./paddle.js"
import * as ball from "./ball.js"

// import pygame as pg
// import random
// import time
// import sys


function createWall(x, y, w, h, color)
{
	let halfW = w / 2
	let halfH = h / 2

	let hit = new hitbox.Hitbox(x, y, dc.HITBOX_WALL_COLOR, color)
	hit.addPoint(-halfW, -halfH)
	hit.addPoint(halfW, -halfH)
	hit.addPoint(halfW, halfH)
	hit.addPoint(-halfW, halfH)

	return hit
}


function createObstacle(x, y, listPoint, color)
{
	let hit = new hitbox.Hitbox(x, y, dc.HITBOX_WALL_COLOR, color)

	for (const p of listPoint)
		hit.addPoint(p[0], p[1])

	return hit
}

function createDirectivePath(x , y, pointList)
{
	let d = "M" + (pointList[0][0] + x) + " " + (pointList[0][1] + y);
    for (let index = 1; index < pointList.length ; index++)
    {
            d +=  " L " + (pointList[index][0] + x) + " " + (pointList[index][1] + y) +" ";
    }
    d +=  " Z";
	return d;
}

function addPolygon(content,x , y, pointList, color)
{
	let d = createDirectivePath(x, y, pointList);
    let newPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    //newPath.style.stroke = color;
	newPath.setAttribute('x', x)
	newPath.setAttribute('y', y)
    newPath.setAttribute('d', d);
    newPath.setAttribute('fill', color);
    content.insertBefore(newPath, null);
	return newPath
}

function changePolygon(path, pointList)
{
	let d = "M" + (pointList[0][0]) + " " + pointList[0][1];
    for (let index = 1; index < pointList.length ; index++)
    {
            d +=  " L " + pointList[index][0] + " " + pointList[index][1] +" ";
    }
    d +=  " Z";
    path.setAttribute('d', d);
}



export class GameClient {
	constructor()
	{
		console.log("area rect")
		console.log(dc.AREA_RECT[0])
		console.log(dc.AREA_RECT[1])
		console.log(dc.AREA_RECT[2])
		console.log(dc.AREA_RECT[3])
		/*
		This method define all variables needed by the program
		*/
		// Init pygame
		// pg.init()


		// We remove the toolbar of the window's height
		this.winSize = ((dc.WIN_WIDTH, dc.WIN_HEIGHT))
		// We create the window
		//this.win = pg.display.set_mode(this.winSize, pg.RESIZABLE)
		this.win = document.getElementById("GameBox");

		// this.clock = pg.time.Clock() // The clock be used to limit our fps
		this.fps = 60
		this.time = 0

		// this.last = time.time()
		this.last = new Date().getTime();

		this.runMainLoop = false

		this.inputWait = 0

		// Creation of state list for player keys
		this.paddlesKeyState =  [...d.PADDLES_KEYS_STATE]

		// Team creation
		this.teamLeft = null
		this.teamRight = null
		

		this.balls = []
		// Ball creation
		// this.balls = [ new ball.Ball(dc.WIN_WIDTH / 2, dc.WIN_HEIGHT / 2)]
		// this.win.insertBefore(this.balls[0].htmlObject, null);
		// for (let index = 0; index < this.balls[0].shadowBalls.length; index++) {
		// 	this.win.insertBefore(this.balls[0].shadowBalls[index][0], null);
		// }
		// console.log("nb shadow ball : " + this.balls[0].shadowBalls.length)

		// // Ball begin left side
		// if (random.random() > 0.5)
		// 	this.balls[0].lastPaddleHitId = random.choice(this.teamLeft.paddles).id
		// // Ball begin right side
		// else
		// {
		// 	this.balls[0].lastPaddleHitId = random.choice(this.teamRight.paddles).id
		// 	this.balls[0].direction = Vec2(-1, 0)
		// 	this.balls[0].lastPaddleTeam = TEAM_RIGHT
		// }

		// Power up creation
		this.powerUpEnable = false
		this.powerUp = [d.POWER_UP_SPAWN_COOLDOWN, new hitbox.Hitbox(0, 0, (0, 0, 200), d.POWER_UP_HITBOX_COLOR), -1, null]
		let temp_list = []
		for ( const p of ball.getPointOfCircle(d.POWER_UP_HITBOX_RADIUS, d.POWER_UP_HITBOX_PRECISION, 0))
		{
			temp_list.push([p[0], p[1]])
			this.powerUp[1].addPoint(p[0], p[1])
		}
		this.powerUp[4] = addPolygon(this.win, 0,0, temp_list, "#FFFFFF")
		this.powerUp[4].style.opacity = "0"


		// Walls creation
		//addPolygon(game, [[50,50], [90,50], [90,90], [50, 90]], "#FF00FF");
		
		this.walls = []
		this.wallsHtmlObjects = []

		//test tempo :


		// let cubePointListe = [[-45,-45], [45,-45], [45,45], [-45, 45]]
		// this.walls.push(createObstacle(400, 399, cubePointListe))
		// this.wallsHtmlObjects.push(addPolygon(this.win, 400, 399, cubePointListe, "#FF00FF"))

		// let ys = 420

		// this.walls.push(createObstacle(1400, ys, cubePointListe))
		// this.wallsHtmlObjects.push(addPolygon(this.win, 1400, ys, cubePointListe, "#FF00FF"))

		// this.walls.push(createObstacle(800, 300, cubePointListe))
		// this.wallsHtmlObjects.push(addPolygon(this.win, 800, 300, cubePointListe, "#FF00FF"))

		// this.walls.push(createObstacle(1000, 300, cubePointListe))
		// this.wallsHtmlObjects.push(addPolygon(this.win, 1000, 300, cubePointListe, "#FF00FF"))

		// this.walls.push(createObstacle(1710, 0, cubePointListe))
		// this.wallsHtmlObjects.push(addPolygon(this.win, 1710, 0, cubePointListe, "#FF00FF"))

		// this.walls.push(createObstacle(0, 0, cubePointListe))
		// this.wallsHtmlObjects.push(addPolygon(this.win, 0, 0, cubePointListe, "#FF00FF"))


		// let wallPointListe = [[0,0], [90,0], [90,900], [0, 900]]
		

		// this.walls.push(createObstacle(400, 0, wallPointListe))
		// this.wallsHtmlObjects.push(addPolygon(this.win, 400, 0, wallPointListe, "#FF00FF"))

		// let borderListe = [[-900,-2], [900,-2], [900,2], [-900, 2]]
		// this.walls.push(createObstacle(900, 2, borderListe))
		// this.wallsHtmlObjects.push(addPolygon(this.win, 900, 2, borderListe, "#FF00FF"))
		// this.walls.push(createObstacle(900, 897, borderListe))
		// this.wallsHtmlObjects.push(addPolygon(this.win, 900, 897, borderListe, "#FF00FF"))

		// let testobj = [[-300, 0], [300, 0], [275, 50], [75, 75], [0, 125], [-75, 75], [-275, 50]]
		// this.walls.push(createObstacle(d.AREA_SIZE[0] / 2, 0, testobj))
		// this.wallsHtmlObjects.push(addPolygon(this.win, d.AREA_SIZE[0] / 2, 0, testobj, "#FF00FF"))
		// idPaddle, paddleTeam, Ball speed, Number of bounce, CC, Perfect shoot, time of goal
		this.goals = []

		this.ballNumber = 0


		for (let index = 0; index < this.walls.length; index++) {
			const element = this.walls[index];
			console.log(element)
		}

		// For communications
		// (Message type, message content)
		this.messageForServer = []
		// (Message type, message content)
		this.messageFromServer = []
		this.inputCooldown = 0

		this.inputEventListener = null
	}


	inputCoolDownChange()
	{
		if (this.inputCooldown != 0)
		{
			this.inputCooldown--;
		}
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
			this.tick()
			this.clock.tick(this.fps)
		}
	}


	step()
	{
		/*
		This method is the main function of the game
		Call it in a while, it need to be re call until this.runMainLoop equals to false
		*/
		// Clear the message for server
		this.messageForServer.length = []

		// this.parseMessageFromServer()
		// Game loop
		if (this.runMainLoop)
		{
			this.inputCoolDownChange()

			this.tick()
			//this.render()
		}
			// this.clock.tick(this.fps)

		// After compute it, clear message from the server
		this.messageFromServer = []
	}


	input(event, type)
	{
		console.log("event : " + event.code + " : type : " + type)


		// let templateContent = {"paddleId" : i, "keyId" : 0, "keyAction" : true}
		let i = paddleInfoUser[0];
		if (type == "down" && event.code == dc.PLAYER_KEYS[i][d.KEY_UP] && ! this.paddlesKeyState[i * 4 + d.KEY_UP])
		{
			this.paddlesKeyState[i * 4 + d.KEY_UP] = true
			// let content = templateContent.copy()
			// content["keyId"] = KEY_UP
			// content["keyAction"] = true
			// this.messageForServer.append((CLIENT_MSG_TYPE_USER_EVENT, content))
			websockGame.send(JSON.stringify({
				'type' : 'userInput',
				'key' : 'up',
				'value': "press"
			}));
		}
		else if (type == "up" && ( (event.code == dc.PLAYER_KEYS[i][d.KEY_UP])) && this.paddlesKeyState[i * 4 + d.KEY_UP])
		{
			this.paddlesKeyState[i * 4 + d.KEY_UP] = false
			// let content = templateContent.copy()
			// content["keyId"] = KEY_UP
			// content["keyAction"] = false
			// this.messageForServer.append((CLIENT_MSG_TYPE_USER_EVENT, content))
			websockGame.send(JSON.stringify({
				'type' : 'userInput',
				'key' : 'up',
				'value': "release"
			}));
		}

		// console.log("test for : " + dc.PLAYER_KEYS[i][d.KEY_DOWN])


		if (type == "down" && event.code == dc.PLAYER_KEYS[i][d.KEY_DOWN] && ! this.paddlesKeyState[i * 4 + d.KEY_DOWN])
		{
			this.paddlesKeyState[i * 4 + d.KEY_DOWN] = true
			// let content = templateContent.copy()
			// content["keyId"] = KEY_DOWN
			// content["keyAction"] = true
			// this.messageForServer.append((CLIENT_MSG_TYPE_USER_EVENT, content))
			websockGame.send(JSON.stringify({
				'type' : 'userInput',
				'key' : 'down',
				'value': "press"
			}));
		}
		else if (type == "up" && ( (event.code == dc.PLAYER_KEYS[i][d.KEY_DOWN])) && this.paddlesKeyState[i * 4 + d.KEY_DOWN])
		{
			this.paddlesKeyState[i * 4 + d.KEY_DOWN] = false
			// let content = templateContent.copy()
			// content["keyId"] = KEY_DOWN
			// content["keyAction"] = false
			// this.messageForServer.append((CLIENT_MSG_TYPE_USER_EVENT, content))
			websockGame.send(JSON.stringify({
				'type' : 'userInput',
				'key' : 'down',
				'value': "release"
			}));
		}



		if (type == "down" && event.code == dc.PLAYER_KEYS[i][d.KEY_POWER_UP] && ! this.paddlesKeyState[i * 4 + d.KEY_POWER_UP])
		{
			this.paddlesKeyState[i * 4 + d.KEY_POWER_UP] = true
			// let content = templateContent.copy()
			// content["keyId"] = KEY_POWER_UP
			// content["keyAction"] = true
			// this.messageForServer.append((CLIENT_MSG_TYPE_USER_EVENT, content))
			websockGame.send(JSON.stringify({
				'type' : 'userInput',
				'key' : 'powerUp',
				'value': "press"
			}));
		}
		else if (type == "up" && ( (event.code == dc.PLAYER_KEYS[i][d.KEY_POWER_UP])) && this.paddlesKeyState[i * 4 + d.KEY_POWER_UP])
		{
			this.paddlesKeyState[i * 4 + d.KEY_POWER_UP] = false
			// let content = templateContent.copy()
			// content["keyId"] = KEY_POWER_UP
			// content["keyAction"] = false
			// this.messageForServer.append((CLIENT_MSG_TYPE_USER_EVENT, content))
			websockGame.send(JSON.stringify({
				'type' : 'userInput',
				'key' : 'powerUp',
				'value': "release"
			}));
		}



		if (type == "down" && event.code == dc.PLAYER_KEYS[i][d.KEY_LAUNCH_BALL] && ! this.paddlesKeyState[i * 4 + d.KEY_LAUNCH_BALL])
		{
			this.paddlesKeyState[i * 4 + d.KEY_LAUNCH_BALL] = true
			// let content = templateContent.copy()
			// content["keyId"] = KEY_LAUNCH_BALL
			// content["keyAction"] = true
			// this.messageForServer.append((CLIENT_MSG_TYPE_USER_EVENT, content))
			websockGame.send(JSON.stringify({
				'type' : 'userInput',
				'key' : 'launchBall',
				'value': "press"
			}));
		}
		else if (type == "up" && ( (event.code == dc.PLAYER_KEYS[i][d.KEY_LAUNCH_BALL])) && this.paddlesKeyState[i * 4 + d.KEY_LAUNCH_BALL])
		{
			this.paddlesKeyState[i * 4 + d.KEY_LAUNCH_BALL] = false
			// let content = templateContent.copy()
			// content["keyId"] = KEY_LAUNCH_BALL
			// content["keyAction"] = false
			// this.messageForServer.append((CLIENT_MSG_TYPE_USER_EVENT, content))
			websockGame.send(JSON.stringify({
				'type' : 'userInput',
				'key' : 'launchBall',
				'value': "release"
			}));
		}

		this.inputCooldown = 2
	}


	tick()
	{
		/*
		This is the method where all calculations will be done
		*/

	// if (this.balls[0].state != 0)
	// {
	// 	console.log("ball status : " + this.balls[0].state)
	// }


		let tmp = new Date().getTime()
		let delta = (tmp - this.last) / 1000
		this.last = tmp

		this.time += delta

		// Check if ball move. If no ball move, all time base event are stopping
		let updateTime = false
		for (const b of this.balls)
		{
			if (b.state == d.STATE_RUN)
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

		if (! updateTime && this.powerUp[0] != d.POWER_UP_SPAWN_COOLDOWN)
			this.powerUp[0] = d.POWER_UP_SPAWN_COOLDOWN

		this.teamLeft.tick(delta, this.paddlesKeyState, updateTime)
		this.teamRight.tick(delta, this.paddlesKeyState, updateTime)

		for (const b of this.balls)
		{
			b.updatePosition(delta, this.teamLeft.paddles, this.teamRight.paddles, this.walls, this.powerUp)
			if (updateTime)
				b.updateTime(delta)
		}

		//pg.display.set_caption("time : " + str(this.time))
		// console.log("time : " + this.time);
	}


	render(){
		/*
		This is the method where all graphic update will be done
		*/
		// We clean our screen with one color
		//this.win.fill((0, 0, 0))

		// Draw area
		// pg.draw.rect(this.win, AREA_COLOR, AREA_RECT)
		// pg.draw.rect(this.win, AREA_TEAM_COLOR, AREA_LEFT_TEAM_RECT)
		// pg.draw.rect(this.win, AREA_COLOR, AREA_MIDDLE_RECT)
		// pg.draw.rect(this.win, AREA_TEAM_COLOR, AREA_RIGTH_TEAM_RECT)

		// Draw walls

		for (const w of this.walls)
		{
			w.drawFill(this.win)
			if (DRAW_HITBOX)
				w.draw(this.win)
		}

		// Power up draw
		if (this.powerUp[0] == d.POWER_UP_VISIBLE)
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
		// pg.display.update()
	}


	quit()
	{
		/*
		This is the quit method
		*/
		// Pygame quit
		this.runMainLoop = false
		pg.quit()
	}


	parseMessageFromServer(event)
	{
		// console.log("DATA FROM GWS RECEIVED");
		let data = null;
		try
		{
			data = JSON.parse(event.data);
			console.log("DATA FROM GWS :", data);
			console.log("paddleInfoUser  : " + paddleInfoUser);

		}
		catch (error)
		{
			console.error("GWS : Json parsing error :", event.data, error);
			return ;
		}
	
		const type = data['type'];
	
		if (type === "error")
		{
			console.error("GWS :Error :", data['error']);
		}
		else if (type === "endGame") // Not the movie !
		{
			document.getElementById("body").onclick = function(){
				document.getElementById("body").onclick = null;
				changePage('3');
			};
			document.getElementById("endGameVS").setAttribute("visibility", "visible")
			document.getElementById("endGameScreen").setAttribute("visibility", "visible")
			document.getElementById("EndStatusGame").setAttribute("visibility", "visible")
			document.getElementById("endGameRightTeam").setAttribute("visibility", "visible");
			document.getElementById("endGameLeftTeam").setAttribute("visibility", "visible");
			document.getElementById("endClickToContinue").setAttribute("visibility", "visible");
			document.getElementById("endGameLeftTeam").textContent = data['leftTeamScore']
			document.getElementById("endGameRightTeam").textContent = data['rightTeamScore']
			if (paddleInfoUser[1] == 0)
			{
				if (data['leftTeamScore'] > data['rightTeamScore'])
				{
					document.getElementById("EndStatusGame").textContent = "You  Win"
					document.getElementById("EndStatusGame").setAttributeNS(null,"fill", "#00FF00")
				}
				else
				{
					document.getElementById("EndStatusGame").textContent = "You Lose"
					document.getElementById("EndStatusGame").setAttributeNS(null,"fill", "#FF0000")	
				}
			}
			else
			{
				if (data['leftTeamScore'] < data['rightTeamScore'])
				{
					document.getElementById("EndStatusGame").textContent = "You  Win"
					document.getElementById("EndStatusGame").setAttributeNS(null,"fill", "#00FF00")
				}
				else
				{
					document.getElementById("EndStatusGame").textContent = "You Lose"
					document.getElementById("EndStatusGame").setAttributeNS(null,"fill", "#FF0000")	
				}
			}
			ws_game.onclose = {};
			ws_game.close();
			ws_game = null;
			id_paddle = null;
			id_team = null;
			console.log("GWS CLOSE");
		}
		else if (type === "startInfo")
		{
			console.log("Starting info received");
			this.createObstaclesOnMap(data['obstacles'])
			this.teamLeft = new team.Team(parseInt(data['nbPlayerTeamLeft']), d.TEAM_LEFT)
			this.teamRight = new team.Team(parseInt(data['nbPlayerTeamRight']), d.TEAM_RIGHT)
			for (let nbplayer = 0; nbplayer < parseInt(data['nbPlayerTeamLeft']); nbplayer++)
			{
				this.win.insertBefore(this.teamLeft.paddles[nbplayer].htmlObject, null);
			}
			for (let nbplayer = 0; nbplayer < parseInt(data['nbPlayerTeamRight']); nbplayer++)
			{
				this.win.insertBefore(this.teamRight.paddles[nbplayer].htmlObject, null);
			}
		}
		else if (type === "startCount")
		{
			console.log("Starting in " + data['number']);
			document.getElementById("startCounter").textContent = "" + data['number'];
			if (data['number'] == 0)
			{	
				this.runMainLoop = true;
				document.getElementById("divStartCounter").remove();
				document.getElementById("startStartingIn").remove();
				document.getElementById("startCounter").remove();
			}
		}
		else if (type === "serverInfo") // Not the movie !
		{
			console.log("match info received");
			this.parseMessageForObstacle(data["updateObstacles"])
			this.parseMessageForPaddles(data["updatePaddles"])
			this.parseMessageForBalls(data["updateBalls"])
			this.parseMessageForDeleteBalls(data["deleteBall"])
			this.parseMessageForPowerUp(data["updatePowerUpInGame"])
			this.parseMessageForUserPowerUp(data["changeUserPowerUp"])
			this.parseMessageForScore(data["updateScore"])
		}
		else
			console.error("GWS :Unkown data recieved :", data);
		}

	createObstaclesOnMap(lstObstacle)
	{
		for (const obstables of lstObstacle)
		{
			this.walls.push(createObstacle(0, 0, obstables))
			this.wallsHtmlObjects.push(addPolygon(this.win, 0, 0, obstables, "#FF00FF"))
		}
	}


	// parseMessageStartInfo( messageContent)
	// {
	// 	// Content of obstacles :
	// 	// {
	// 	// 	obstables : [ {position:[x, y], points:[[x, y]], color:(r, g, b)} ]
	// 	// 	powerUp : true or false
	// 	// }
	// 	this.walls.clear()

	// 	for (const content of messageContent["obstacles"])
	// 	{
	// 		x = dc.AREA_RECT[0] + content[0][0]
	// 		y = dc.AREA_RECT[1] + content[0][1]
	// 		obstacle = createObstacle(x, y, content["points"], content["color"])
	// 		this.walls.append(obstacle)
	// 	}
	// 	this.powerUpEnable = messageContent["powerUp"]
	// }


	parseMessageForObstacle( messageContent){
		// Content of obstacles :
		// [
		// 	{id, position, points:[[x, y]]}
		// ]
		for (const content of messageContent)
		{
			this.walls[content[0]].setPos(vec2Add(new Vec2(content[1][0], content[1][1]), new Vec2(dc.AREA_RECT[0], dc.AREA_RECT[1])))
			this.walls[content[0]].clearPoints()
			this.walls[content[0]].addPoints(content[2])
			this.wallsHtmlObjects[content[0]].setAttribute('d', createDirectivePath(content[1][0], content[1][1], content[2]));
			
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
			let x = dc.AREA_RECT[0] + content[0][0]
			let y = dc.AREA_RECT[1] + content[0][1]

			if (content[2] == d.TEAM_LEFT)
			{
				if (content[3] >= this.teamLeft.paddles.length)
				{
					while (content[3] > this.teamLeft.paddles.length)
						this.teamLeft.paddles.append(paddle.Paddle(0, 0, this.teamLeft.paddles.length, d.TEAM_LEFT))
					this.teamLeft.paddles.append(paddle.Paddle(0, 0, content[3], d.TEAM_LEFT))
				}
				this.teamLeft.paddles[content[3]].setPos(x, y)
				if (this.teamLeft.paddles[content[3]].modifierSize != content[1])
					this.teamLeft.paddles[content[3]].modifySize(content[1])
				//this.teamLeft.paddles[content[3]].powerUp = content["powerUp"]
				this.teamLeft.paddles[content[3]].powerUpInCharge = content[4]
			}
			else
			{
				if (content[3] >= this.teamRight.paddles.length)
				{
					while (content[3] > this.teamRight.paddles.length)
						this.teamRight.paddles.append(paddle.Paddle(0, 0, this.teamRight.paddles.length, d.TEAM_RIGHT))
					this.teamRight.paddles.append(paddle.Paddle(0, 0, content[3], d.TEAM_RIGHT))
				}
				this.teamRight.paddles[content[3]].setPos(x, y)
				if (this.teamRight.paddles[content[3]].modifierSize != content[1])
					this.teamRight.paddles[content[3]].modifySize(content[1])
				//this.teamRight.paddles[content[3]].powerUp = content["powerUp"]
				this.teamRight.paddles[content[3]].powerUpInCharge = content[4]
			}
		}
	}

	parseMessageForBalls( messageContent)
	{
		// Content of balls :
		// [
		// 	{position:[x, y], direction:[x, y], speed, radius, state, last_paddle_hit_info:[id, team], modifier_state}
		// ]
		let i = 0
		let numberOfMessageBall = messageContent.length
		while (i < numberOfMessageBall)
		{
			let content = messageContent[i]
			let x = dc.AREA_RECT[0] + content[0][0]
			let y = dc.AREA_RECT[1] + content[0][1]

			// Update ball if exist
			if (i < this.balls.length)
			{
				let b = this.balls[i]
				b.pos.x = x
				b.pos.y = y
				b.hitbox.setPos(new Vec2(x, y))
				b.direction = new Vec2(content[1][0], content[1][1])
				b.speed = content[3]
				b.radius = content[2]
				if (b.state != content[4] && content[4] != 0)
				{
					b.htmlObject.setAttribute("display", "None");
					for (let index = 0; index < b.shadowBalls.length; index++)
					{
						b.shadowBalls[index][0].setAttribute("display", "None");
						b.shadowBalls[index][1] = [(b.pos.x - (b.radius / 2)), (b.pos.y - (b.radius / 2))]
						b.shadowBalls[index][0].setAttribute('x', "" +  (b.pos.x - (b.radius / 2)));
						b.shadowBalls[index][0].setAttribute('y', "" +  (b.pos.y - (b.radius / 2)));
					}
				}
				else if (b.state != content[4] && content[4] == 0)
				{
					b.htmlObject.setAttribute("display", "block");
					for (let index = 0; index < b.shadowBalls.length; index++)
					{
						b.shadowBalls[index][0].setAttribute("display", "block");
					}
				}
				b.state = content[4]
				b.htmlObject.setAttribute('width', b.radius * 2)
				b.htmlObject.setAttribute('height', b.radius * 2)
				// b.lastPaddleHitId = content["last_paddle_hit_info"][0]
				// b.lastPaddleTeam = content["last_paddle_hit_info"][1]
				b.setModifierByState(content[5])
			}

			// Create a new one instead
			else
			{
				let b = new ball.Ball(x, y)
				b.direction = new Vec2(content[1][0], content[1][1])
				b.speed = content[3]
				b.radius = content[2]
				b.state = content[4]
				// b.lastPaddleHitId = content["last_paddle_hit_info"][0]
				// b.lastPaddleTeam = content["last_paddle_hit_info"][1]
				b.setModifierByState(content[5])
				this.balls.push(b)
				this.win.insertBefore(b.htmlObject, null);
				b.htmlObject.setAttribute('width', b.radius * 2)
				b.htmlObject.setAttribute('height', b.radius * 2)
				for (let index = 0; index < b.shadowBalls.length; index++) {
					this.win.insertBefore(b.shadowBalls[index][0], null);
				}
			}
			i += 1;
		}
	}

	parseMessageForDeleteBalls( messageContent)
	{
		// Content of delete balls :
		// [id_ball]
		if (messageContent == "null")
			return ;
		for (let i = 0; i < messageContent.length; i++) {
			this.balls[messageContent[i] - i].htmlObject.remove()
			for (let index = 0; index < this.balls[messageContent[i] - i].shadowBalls.length; index++)
			{
				this.balls[messageContent[i] - i].shadowBalls[index][0].remove()
			}
			this.balls.splice(messageContent[i] - i, 1)
		}
	}


	parseMessageForPowerUp( messageContent)
	{
		// Content of balls :
		// {position:[x, y], state}
		if (messageContent === 'null')
			return ;
		let x = dc.AREA_RECT[0] + messageContent[0][0]
		let y = dc.AREA_RECT[1] + messageContent[0][1]

		this.powerUp[0] = messageContent[1]
		this.powerUp[1].setPos(new Vec2(x, y))
		let temp_list = []
		for ( const p of ball.getPointOfCircle(d.POWER_UP_HITBOX_RADIUS, d.POWER_UP_HITBOX_PRECISION, 0))
		{
			temp_list.push([p[0], p[1]])
		}
		this.powerUp[4].remove()
		this.powerUp[4] = addPolygon(this.win, x,y, temp_list, "#FFFFFF")
		if (messageContent[1])
		{
			this.powerUp[4].style.opacity = 0;
		}
		else
		{
			this.powerUp[4].style.opacity = 1;
		}

	}

	parseMessageForUserPowerUp( messageContent)
	{
		let img = document.getElementById('imgPowerUp')

		// if (messageContent == -1)
		// 	img.src = "";
		// else
		img.src = "/static/image/game/powerUp/sprite_" + messageContent + ".png"
	}

	parseMessageForScore( messageContent)
	{
		// Content of power up :
		// {leftTeam, rightTeam}
		if (messageContent != 'null')
		{
			document.getElementById('scoreLeftTeam').textContent = "Score : " + messageContent[0]
			document.getElementById('scoreRightTeam').textContent = "Score : " + messageContent[1]
		}
	}
}