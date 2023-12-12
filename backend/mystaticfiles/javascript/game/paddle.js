// from client_side.client_define import *
// from client_side.vec2 import *
// import client_side.hitbox as hitbox

class Paddle {
	def	constructor ( x, y, id, team) -> None:
		this.id = id
		this.pos = Vec2(x, y)
		this.w = PADDLE_WIDTH
		this.h = PADDLE_HEIGHT
		this.halfW = PADDLE_WIDTH / 2
		this.halfH = PADDLE_HEIGHT / 2

		this.hitbox = hitbox.Hitbox(x, y, HITBOX_PADDLE_COLOR, PADDLE_COLOR)
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

		this.powerUp = POWER_UP_NONE

		this.powerUpInCharge = []

		// For stats
		this.numberOfGoal = 0
		this.maxSpeedBallTouch = 0
		this.maxBounceBallGoal = 0
		this.numberOfContreCamp = 0
		this.numberOfPerfectShoot = 0


	def updateTimes(this, delta):
		if this.waitLaunch > 0:
			this.waitLaunch -= delta
			if this.waitLaunch < 0:
				this.waitLaunch = 0

		if this.waitUsePowerUp > 0:
			this.waitUsePowerUp -= delta
			if this.waitUsePowerUp < 0:
				this.waitUsePowerUp = 0

		powerUpEffectToRemove = []

		for i in range(len(this.powerUpEffects)):
			powerUpEffect = this.powerUpEffects[i]
			if powerUpEffect[1] > 0:
				powerUpEffect[1] -= delta
				// If the time of the power up ended
				if powerUpEffect[1] < 0:
					powerUpEffect[1] = 0
					powerUpEffectToRemove.append(i)
					// Remove the effect of the power up
					if powerUpEffect[0] == POWER_UP_PADDLE_FAST:
						this.modifierSpeed /= POWER_UP_PADDLE_FAST_SPEED_FACTOR

					else if powerUpEffect[0] == POWER_UP_PADDLE_SLOW:
						this.modifierSpeed *= POWER_UP_PADDLE_SLOW_SPEED_FACTOR

					else if powerUpEffect[0] == POWER_UP_PADDLE_BIG:
						this.modifierSize /= POWER_UP_PADDLE_BIG_SIZE_FACTOR
						this.modifySize(this.modifierSize)

					else if powerUpEffect[0] == POWER_UP_PADDLE_LITTLE:
						this.modifierSize *= POWER_UP_PADDLE_LITTLE_SIZE_FACTOR
						this.modifySize(this.modifierSize)

		for i in range(len(powerUpEffectToRemove)):
			this.powerUpEffects.pop(powerUpEffectToRemove[i] - i)


	def move(this, dir, delta):
		if dir == "up":
			this.pos.y -= PADDLE_SPEED * this.modifierSpeed * delta
			if this.pos.y - (this.halfH * this.modifierSize) < AREA_RECT[1] + PERFECT_SHOOT_SIZE:
				this.pos.y = AREA_RECT[1] + PERFECT_SHOOT_SIZE + (this.halfH * this.modifierSize)
			this.hitbox.setPos(this.pos.dup())

		else if dir == "down":
			this.pos.y += PADDLE_SPEED * this.modifierSpeed * delta
			if this.pos.y + (this.halfH * this.modifierSize) > AREA_RECT[1] + AREA_RECT[3] - PERFECT_SHOOT_SIZE:
				this.pos.y = AREA_RECT[1] + AREA_RECT[3] - PERFECT_SHOOT_SIZE - (this.halfH * this.modifierSize)
			this.hitbox.setPos(this.pos.dup())


	def modifySize(this, modifier):
		this.modifierSize = modifier
		this.hitbox.clearPoints()
		this.hitbox.addPoint(-this.halfW, -this.halfH * this.modifierSize)
		this.hitbox.addPoint(this.halfW, -this.halfH * this.modifierSize)
		this.hitbox.addPoint(this.halfW, this.halfH * this.modifierSize)
		this.hitbox.addPoint(-this.halfW, this.halfH * this.modifierSize)

		if this.pos.y - (this.halfH * this.modifierSize) < AREA_RECT[1] + PERFECT_SHOOT_SIZE:
			this.pos.y = AREA_RECT[1] + PERFECT_SHOOT_SIZE + (this.halfH * this.modifierSize)
			this.hitbox.setPos(this.pos.dup())
		if this.pos.y + (this.halfH * this.modifierSize) > AREA_RECT[1] + AREA_RECT[3] - PERFECT_SHOOT_SIZE:
			this.pos.y = AREA_RECT[1] + AREA_RECT[3] - PERFECT_SHOOT_SIZE - (this.halfH * this.modifierSize)
			this.hitbox.setPos(this.pos.dup())

		if modifier != 1:
			this.modifierTimeEffect = 5


	def draw(this, win):
		if len(this.powerUpInCharge) > 0:
			if this.powerUpInCharge[0] == POWER_UP_BALL_FAST:
				this.hitbox.fillColor = POWER_UP_BALL_FAST_COLOR
			else if this.powerUpInCharge[0] == POWER_UP_BALL_WAVE:
				this.hitbox.fillColor = POWER_UP_BALL_WAVE_COLOR
			else if this.powerUpInCharge[0] == POWER_UP_BALL_INVISIBLE:
				this.hitbox.fillColor = POWER_UP_BALL_INVISIBLE_COLOR
		else:
			this.hitbox.fillColor = PADDLE_COLOR
		this.hitbox.drawFill(win)
		if DRAW_HITBOX:
			this.hitbox.draw(win)


	def setPos(this, x, y):
		this.pos = Vec2(x, y)
		this.hitbox.setPos(Vec2(x, y))
}