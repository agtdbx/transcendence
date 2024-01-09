import * as dc from "./client_define.js"
import * as d from "./define.js"
import * as paddle from "./paddle.js"
import * as utils from "./pg_utils.js"
// import * as Math from 'math.js'


export class Team {
	constructor ( numberOfPlayers, team){
		if (numberOfPlayers < 1)
			numberOfPlayers = 1
		else if (numberOfPlayers > d.TEAM_MAX_PLAYER)
			numberOfPlayers = d.TEAM_MAX_PLAYER

		this.team = team

		let xPos = 0
		if (this.team == d.TEAM_LEFT)
			xPos = dc.AREA_RECT[0] + d.AREA_BORDER_SIZE * 2
		else
			xPos = dc.AREA_RECT[0] + dc.AREA_RECT[2] - d.AREA_BORDER_SIZE * 2

		this.paddles = []
		if (numberOfPlayers == 1)
		{
			console.log("team create paddle at : [ " + xPos + " ] [ " + dc.AREA_RECT[1] + " + " + dc.AREA_RECT[3] + " / 2  = " + dc.AREA_RECT[1] + dc.AREA_RECT[3] / 2 + " ]")
			this.paddles.push( new paddle.Paddle(xPos, dc.AREA_RECT[1] + dc.AREA_RECT[3] / 2, 0, this.team))
		}
		else
		{
			this.paddles.push( new paddle.Paddle(xPos, dc.AREA_RECT[1] + Math.floor(dc.AREA_RECT[3] / 3), 0, this.team))
			this.paddles.push( new paddle.Paddle(xPos, dc.AREA_RECT[1] + Math.floor(dc.AREA_RECT[3] / 3) * 2, 1, this.team))
		}

		this.score = 0
		// list of power up who try to use : [power up id, paddle id, power up used (bool)]
		this.powerUpTryUse = []
	}


	tick( delta, paddlesKeyState, updateTime){
		// Check input
		for (let i = 0; i < this.paddles.length; i++) 
		{
			if (updateTime)
				this.paddles[i].updateTimes(delta)

			let keyId = i
			if (this.team == d.TEAM_RIGHT)
				keyId += d.TEAM_MAX_PLAYER

			if (paddlesKeyState[keyId * 4 + d.KEY_UP])
				this.paddles[i].move("up", delta)
			if (paddlesKeyState[keyId * 4 + d.KEY_DOWN])
				this.paddles[i].move("down", delta)
		}
	}

	draw( win, powerUpEnable)
	{
		for (const p of this.paddles)
			p.draw(win)

		if (this.team == dc.TEAM_LEFT)
		{			
			utils.drawText(win, "SCORE : " + str(this.score), (75, 75 / 2), (255, 255, 255), 30, null, "mid-left")
			if (powerUpEnable)
			{
				utils.drawText(win, this.paddles[0].powerUp, (50, 70), (255, 255, 255), 30, null, "mid-right")
				if (this.paddles.length == 2)
				utils.drawText(win, this.paddles[1].powerUp, (50, dc.WIN_HEIGHT - 70), (255, 255, 255), 30, null, "mid-right")
			}
		}

		else
		{
			utils.drawText(win, "SCORE : " + this.score, (dc.WIN_WIDTH - 75, 75 / 2), (255, 255, 255), 30, null, "mid-right")
			if (powerUpEnable)
			{
				utils.drawText(win, this.paddles[0].powerUp, (dc.WIN_WIDTH - 50, 70), (255, 255, 255), 30, null, "mid-left")
				if (this.paddles.length == 2)
				utils.drawText(win, this.paddles[1].powerUp, (dc.WIN_WIDTH - 50, dc.WIN_HEIGHT - 70), (255, 255, 255), 30, null, "mid-left")
			}
		}
	}


	applyPowerUpToPaddles( powerUp)
	{
		for (const p of this.paddles)
			p.addPowerUpEffect(powerUp)
	}
}