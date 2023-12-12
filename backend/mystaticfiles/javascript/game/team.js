// from client_side.client_define import *
// from client_side.pg_utils import *
// import client_side.paddle as paddle

class Team {
	constructor ( numberOfPlayers, team){
		if (numberOfPlayers < 1)
			numberOfPlayers = 1
		else if (numberOfPlayers > TEAM_MAX_PLAYER)
			numberOfPlayers = TEAM_MAX_PLAYER

		this.team = team

		if (this.team == TEAM_LEFT)
			xPos = AREA_RECT[0] + AREA_BORDER_SIZE * 2
		else
			xPos = AREA_RECT[0] + AREA_RECT[2] - AREA_BORDER_SIZE * 2

		this.paddles = []
		if (numberOfPlayers == 1)
			this.paddles.append(paddle.Paddle(xPos, AREA_RECT[1] + AREA_RECT[3] / 2, 0, this.team))
		else
			this.paddles.append(paddle.Paddle(xPos, AREA_RECT[1] + AREA_RECT[3] / 3, 0, this.team))
			this.paddles.append(paddle.Paddle(xPos, AREA_RECT[1] + AREA_RECT[3] / 3 * 2, 1, this.team))

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

			keyId = i
			if (this.team == TEAM_RIGHT)
				keyId += TEAM_MAX_PLAYER

			if (paddlesKeyState[keyId * 4 + KEY_UP])
				this.paddles[i].move("up", delta)
			if (paddlesKeyState[keyId * 4 + KEY_DOWN])
				this.paddles[i].move("down", delta)
		}
	}

	draw( win, powerUpEnable)
	{
		for (const p of this.paddles)
			p.draw(win)

		if (this.team == TEAM_LEFT)
		{			
			drawText(win, "SCORE : " + str(this.score), (75, 75 / 2), (255, 255, 255), size=30, align="mid-left")
			if (powerUpEnable)
			{
				drawText(win, str(this.paddles[0].powerUp), (50, 70), (255, 255, 255), size=30, align="mid-right")
				if (this.paddles.length == 2)
					drawText(win, str(this.paddles[1].powerUp), (50, WIN_HEIGHT - 70), (255, 255, 255), size=30, align="mid-right")
			}
		}

		else
		{
			drawText(win, "SCORE : " + str(this.score), (WIN_WIDTH - 75, 75 / 2), (255, 255, 255), size=30, align="mid-right")
			if (powerUpEnable)
			{
				drawText(win, str(this.paddles[0].powerUp), (WIN_WIDTH - 50, 70), (255, 255, 255), size=30, align="mid-left")
				if (this.paddles.length == 2)
					drawText(win, str(this.paddles[1].powerUp), (WIN_WIDTH - 50, WIN_HEIGHT - 70), (255, 255, 255), size=30, align="mid-left")
			}
		}
	}


	applyPowerUpToPaddles( powerUp)
	{
		for (const p of this.paddles)
			p.addPowerUpEffect(powerUp)
	}
}