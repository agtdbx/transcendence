import * as dc from "./client_define.js"
import * as d from "./define.js"
import {Vec2, vec2Add} from "./vec2.js"
import * as hitbox from "./hitbox.js"
import * as team from "./team.js"
import * as paddle from "./paddle.js"
import * as ball from "./ball.js"


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
	let before = document.getElementById('divStartCounter');
	newPath.setAttribute('x', x)
	newPath.setAttribute('y', y)
    newPath.setAttribute('d', d);
    newPath.setAttribute('fill', color);
    content.insertBefore(newPath, before);
	return newPath
}


export class GameClient {
	constructor()
	{

		// We remove the toolbar of the window's height
		this.winSize = ((dc.WIN_WIDTH, dc.WIN_HEIGHT))
		// We create the window
		this.win = document.getElementById("GameBox");

		this.fps = 60
		this.time = 0

		this.last = new Date().getTime();

		this.runMainLoop = false

		this.inputWait = 0

		// Creation of state list for player keys
		this.paddlesKeyState =  [...d.PADDLES_KEYS_STATE]

		// Team creation
		this.teamLeft = null
		this.teamRight = null


		this.balls = []

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
		this.walls = []
		this.wallsHtmlObjects = []

		this.goals = []

		this.ballNumber = 0


		for (let index = 0; index < this.walls.length; index++) {
			const element = this.walls[index];
			// console.log(element)
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

		// Game loop
		if (this.runMainLoop)
		{
			this.inputCoolDownChange()

			this.tick()
		}

		// After compute it, clear message from the server
		this.messageFromServer = []
	}


	input(event, type)
	{
		let i = paddleInfoUser[0];
		if (type == "down" && event.code == dc.PLAYER_KEYS[i][d.KEY_UP] && ! this.paddlesKeyState[i * 4 + d.KEY_UP])
		{
			this.paddlesKeyState[i * 4 + d.KEY_UP] = true
			websockGame.send(JSON.stringify({
				'type' : 'userInput',
				'key' : 'up',
				'value': "press"
			}));
		}
		else if (type == "up" && ( (event.code == dc.PLAYER_KEYS[i][d.KEY_UP])) && this.paddlesKeyState[i * 4 + d.KEY_UP])
		{
			this.paddlesKeyState[i * 4 + d.KEY_UP] = false
			websockGame.send(JSON.stringify({
				'type' : 'userInput',
				'key' : 'up',
				'value': "release"
			}));
		}

		if (type == "down" && event.code == dc.PLAYER_KEYS[i][d.KEY_DOWN] && ! this.paddlesKeyState[i * 4 + d.KEY_DOWN])
		{
			this.paddlesKeyState[i * 4 + d.KEY_DOWN] = true
			websockGame.send(JSON.stringify({
				'type' : 'userInput',
				'key' : 'down',
				'value': "press"
			}));
		}
		else if (type == "up" && ( (event.code == dc.PLAYER_KEYS[i][d.KEY_DOWN])) && this.paddlesKeyState[i * 4 + d.KEY_DOWN])
		{
			this.paddlesKeyState[i * 4 + d.KEY_DOWN] = false
			websockGame.send(JSON.stringify({
				'type' : 'userInput',
				'key' : 'down',
				'value': "release"
			}));
		}



		if (type == "down" && event.code == dc.PLAYER_KEYS[i][d.KEY_POWER_UP] && ! this.paddlesKeyState[i * 4 + d.KEY_POWER_UP])
		{
			this.paddlesKeyState[i * 4 + d.KEY_POWER_UP] = true
			websockGame.send(JSON.stringify({
				'type' : 'userInput',
				'key' : 'powerUp',
				'value': "press"
			}));
		}
		else if (type == "up" && ( (event.code == dc.PLAYER_KEYS[i][d.KEY_POWER_UP])) && this.paddlesKeyState[i * 4 + d.KEY_POWER_UP])
		{
			this.paddlesKeyState[i * 4 + d.KEY_POWER_UP] = false
			websockGame.send(JSON.stringify({
				'type' : 'userInput',
				'key' : 'powerUp',
				'value': "release"
			}));
		}



		if (type == "down" && event.code == dc.PLAYER_KEYS[i][d.KEY_LAUNCH_BALL] && ! this.paddlesKeyState[i * 4 + d.KEY_LAUNCH_BALL])
		{
			this.paddlesKeyState[i * 4 + d.KEY_LAUNCH_BALL] = true
			websockGame.send(JSON.stringify({
				'type' : 'userInput',
				'key' : 'launchBall',
				'value': "press"
			}));
		}
		else if (type == "up" && ( (event.code == dc.PLAYER_KEYS[i][d.KEY_LAUNCH_BALL])) && this.paddlesKeyState[i * 4 + d.KEY_LAUNCH_BALL])
		{
			this.paddlesKeyState[i * 4 + d.KEY_LAUNCH_BALL] = false
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

		if (this.teamLeft == null || this.teamRight == null)
		{
			console.error("TEAM NULLL");
			return
		}
		this.teamLeft.tick(delta, this.paddlesKeyState, updateTime)
		this.teamRight.tick(delta, this.paddlesKeyState, updateTime)

		for (const b of this.balls)
		{
			b.updatePosition(delta, this.teamLeft.paddles, this.teamRight.paddles, this.walls, this.powerUp)
			if (updateTime)
				b.updateTime(delta)
		}
	}


	render(){
		/*
		This is the method where all graphic update will be done
		*/
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
	}

	parseMessageFromServer(event)
	{
		let data = null;
		try
		{
			data = JSON.parse(event.data);
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

			setTimeout(function () {
				if (current_page == 6)
					changePage('3');
			}, 3000);
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
			this.wallsHtmlObjects.push(addPolygon(this.win, 0, 0, obstables, "#DDDDDD"))
		}
	}


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
				this.teamLeft.paddles[content[3]].powerUpInCharge = content[4]
				this.teamLeft.paddles[content[3]].draw();
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
				this.teamRight.paddles[content[3]].powerUpInCharge = content[4]
				this.teamRight.paddles[content[3]].draw();
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
				b.setModifierByState(content[5])
				if (content[4] != 0) //b.state != content[4] &&
				{
					// b.htmlObject.setAttribute("display", "None");
					for (let index = 0; index < b.shadowBalls.length; index++)
					{
						b.shadowBalls[index][0].setAttribute("display", "None");
						b.shadowBalls[index][1] = [(b.pos.x - (b.radius * b.modifierSize)), (b.pos.y - (b.radius * b.modifierSize))]
						b.shadowBalls[index][0].setAttribute('x', "" +  (b.pos.x - (b.radius * b.modifierSize)));
						b.shadowBalls[index][0].setAttribute('y', "" +  (b.pos.y - (b.radius * b.modifierSize)));
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
				b.htmlObject.setAttribute('width', b.radius * 2 * b.modifierSize)
				b.htmlObject.setAttribute('height', b.radius * 2 * b.modifierSize)
				b.htmlObject.setAttribute('x', (b.pos.x - (b.radius * b.modifierSize)))
				b.htmlObject.setAttribute('y', (b.pos.y - (b.radius * b.modifierSize)))
			}

			// Create a new one instead
			else
			{
				let b = new ball.Ball(x, y)
				b.direction = new Vec2(content[1][0], content[1][1])
				b.speed = content[3]
				b.radius = content[2]
				b.state = content[4]
				b.setModifierByState(content[5])
				this.balls.push(b)
				b.htmlObject.setAttribute('width', b.radius * 2)
				b.htmlObject.setAttribute('height', b.radius * 2)
				for (let index = 0; index < b.shadowBalls.length; index++) {
					this.win.insertBefore(b.shadowBalls[index][0], null);
				}
				this.win.insertBefore(b.htmlObject, null);
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
