import * as dc from "./client_define.js"
import * as d from "./define.js"
import {Vec2} from "./vec2.js"
import * as hitbox from "./hitbox.js"

export class Paddle {
	constructor ( x, y, id, team)
	{
		this.id = id
		this.pos = new Vec2(x, y)
		this.w = d.PADDLE_WIDTH
		this.h = d.PADDLE_HEIGHT
		this.halfW = d.PADDLE_WIDTH / 2
		this.halfH = d.PADDLE_HEIGHT / 2
		this.htmlObject = document.createElementNS('http://www.w3.org/2000/svg', 'rect')
		console.log("create paddle at : " + x + "," + y)
		this.htmlObject.setAttribute('x',  x - this.halfW);
		this.htmlObject.setAttribute('y',  y - this.halfH);
		this.htmlObject.setAttribute('width', this.w);
		this.htmlObject.setAttribute('height',  this.h);
		this.htmlObject.setAttribute('transform-origin', "center");


		this.hitbox = new hitbox.Hitbox(x, y, dc.HITBOX_PADDLE_COLOR, dc.PADDLE_COLOR)
		this.hitbox.addPoint(-this.halfW, -this.halfH)
		this.hitbox.addPoint(this.halfW, -this.halfH)
		this.hitbox.addPoint(this.halfW, this.halfH)
		this.hitbox.addPoint(-this.halfW, this.halfH)

		this.team = team

		this.waitLaunch = 0
		this.waitUsePowerUp = 0

		this.modifierSpeed = 1
		this.modifierSize = 1

		// Represente the effect on paddle [POWER_UP, TIME_EFFECT]
		this.powerUpEffects = []

		this.powerUp = d.POWER_UP_NONE

		this.powerUpInCharge = []

		// For stats
		this.numberOfGoal = 0
		this.maxSpeedBallTouch = 0
		this.maxBounceBallGoal = 0
		this.numberOfContreCamp = 0
		this.numberOfPerfectShoot = 0
	}


	updateTimes( delta)
	{
		if (this.waitLaunch > 0)
		{
			this.waitLaunch -= delta
			if (this.waitLaunch < 0)
				this.waitLaunch = 0
		}

		if (this.waitUsePowerUp > 0)
		{
			this.waitUsePowerUp -= delta
			if (this.waitUsePowerUp < 0)
				this.waitUsePowerUp = 0
		}

		let powerUpEffectToRemove = []
		for (let i = 0; i < this.powerUpEffects.length; i++)
		{
			let powerUpEffect = this.powerUpEffects[i]
			if (powerUpEffect[1] > 0)
			{
				powerUpEffect[1] -= delta
				// If the time of the power up ended
				if (powerUpEffect[1] < 0)
				{
					powerUpEffect[1] = 0
					powerUpEffectToRemove.append(i)
					// Remove the effect of the power up
					if (powerUpEffect[0] == POWER_UP_PADDLE_FAST)
						this.modifierSpeed /= POWER_UP_PADDLE_FAST_SPEED_FACTOR

					else if (powerUpEffect[0] == POWER_UP_PADDLE_SLOW)
						this.modifierSpeed *= POWER_UP_PADDLE_SLOW_SPEED_FACTOR

					else if (powerUpEffect[0] == POWER_UP_PADDLE_BIG)
					{
						this.modifierSize /= POWER_UP_PADDLE_BIG_SIZE_FACTOR
						this.modifySize(this.modifierSize)
					}

					else if (powerUpEffect[0] == POWER_UP_PADDLE_LITTLE)
					{
						this.modifierSize *= POWER_UP_PADDLE_LITTLE_SIZE_FACTOR
						this.modifySize(this.modifierSize)
					}
				}
			}
		}

		for (let i = 0; i < powerUpEffectToRemove.length; i++)
			this.powerUpEffects.pop(powerUpEffectToRemove[i] - i)
	}

	move( dir, delta)
	{
		if (dir == "up")
		{
			this.pos.y -= PADDLE_SPEED * this.modifierSpeed * delta
			if (this.pos.y - (this.halfH * this.modifierSize) < AREA_RECT[1] + PERFECT_SHOOT_SIZE)
				this.pos.y = AREA_RECT[1] + PERFECT_SHOOT_SIZE + (this.halfH * this.modifierSize)
			this.hitbox.setPos(this.pos.dup())
		}

		else if (dir == "down")
		{
			this.pos.y += PADDLE_SPEED * this.modifierSpeed * delta
			if (this.pos.y + (this.halfH * this.modifierSize) > AREA_RECT[1] + AREA_RECT[3] - PERFECT_SHOOT_SIZE)
				this.pos.y = AREA_RECT[1] + AREA_RECT[3] - PERFECT_SHOOT_SIZE - (this.halfH * this.modifierSize)
			this.hitbox.setPos(this.pos.dup())
		}
		this.htmlObject.setAttribute('y', "" + this.pos.y);
	}


	modifySize( modifier)
	{
		this.modifierSize = modifier
		this.hitbox.clearPoints()
		this.hitbox.addPoint(-this.halfW, -this.halfH * this.modifierSize)
		this.hitbox.addPoint(this.halfW, -this.halfH * this.modifierSize)
		this.hitbox.addPoint(this.halfW, this.halfH * this.modifierSize)
		this.hitbox.addPoint(-this.halfW, this.halfH * this.modifierSize)

		if (this.pos.y - (this.halfH * this.modifierSize) < AREA_RECT[1] + PERFECT_SHOOT_SIZE)
		{
			this.pos.y = AREA_RECT[1] + PERFECT_SHOOT_SIZE + (this.halfH * this.modifierSize)
			this.hitbox.setPos(this.pos.dup())
		}
		if (this.pos.y + (this.halfH * this.modifierSize) > AREA_RECT[1] + AREA_RECT[3] - PERFECT_SHOOT_SIZE)
		{
			this.pos.y = AREA_RECT[1] + AREA_RECT[3] - PERFECT_SHOOT_SIZE - (this.halfH * this.modifierSize)
			this.hitbox.setPos(this.pos.dup())
		}

		if (modifier != 1)
			this.modifierTimeEffect = 5
	}


	draw( win)
	{
		if (this.powerUpInCharge.length > 0)
		{
			if (this.powerUpInCharge[0] == d.POWER_UP_BALL_FAST)
				this.hitbox.fillColor = dc.POWER_UP_BALL_FAST_COLOR
			else if (this.powerUpInCharge[0] == d.POWER_UP_BALL_WAVE)
				this.hitbox.fillColor = dc.POWER_UP_BALL_WAVE_COLOR
			else if (this.powerUpInCharge[0] == d.POWER_UP_BALL_INVISIBLE)
				this.hitbox.fillColor = dc.POWER_UP_BALL_INVISIBLE_COLOR
		}
		else
			this.hitbox.fillColor = d.PADDLE_COLOR
		this.hitbox.drawFill(win)
		if (d.DRAW_HITBOX)
			this.hitbox.draw(win)
	}


	setPos( x, y)
	{
		this.pos = Vec2(x, y)
		this.hitbox.setPos(Vec2(x, y))
	}
}