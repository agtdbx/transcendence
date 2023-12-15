import "./client_define.js"
import "./vec2.js"
import "./hitbox.js"
import * as hitbox from "./hitbox.js"
import * as paddle from "./paddle.js"

// import pygame as pg



function getPointOfCircle(radius, precision, beginDegree = 0)
{
	let points = []
	for (let i = 0; i < precision; i++)
	{
		degree = 360 / precision * i + beginDegree
		radian = degree * (math.pi / 180)
		x = radius * math.cos(radian)
		y = radius * math.sin(radian)
		points.append((x, y))
	}
	return points
}



class Ball {
	constructor ( x, y)
	{
		// Geometry
		this.pos = Vec2(x, y)
		this.radius = BALL_RADIUS
		this.speed = BALL_START_SPEED
		this.direction = Vec2(1, 0)

		// Graphique
		this.color = BALL_COLOR
		this.originalSprite = pg.image.load("client_side/imgs/ball.png")
		this.sprite = pg.transform.scale(this.originalSprite, (this.radius * 2, this.radius * 2))

		// Hitbox creation
		this.hitbox = hitbox.Hitbox(this.pos.x, this.pos.y, HITBOX_BALL_COLOR)
		this.hitbox.setPos(this.pos)
		let points = getPointOfCircle(this.radius, BALL_HITBOX_PRECISION, 360 / (BALL_HITBOX_PRECISION * 2))

		for (let index = 0; index < points.length; index++)
		{
			const p = array[index];
			this.hitbox.addPoint(p[0], p[1]);
		}

		// Modifier
		this.modifierSpeed = 1
		this.modifierSize = 1
		this.modifierSkipCollision = False
		this.modifierInvisibleBall = False
		this.modifierInvisibleBallTimer = 0
		this.modifierWaveBall = False
		this.modifierWaveBallTimer = 0
		this.modifierStopBallTimer = 0

		// Represente the effect on ball [POWER_UP, TIME_EFFECT]
		this.powerUpEffects = []

		this.lastPositions = [];
		this.lastColors = [];
		for (let index = 0; index < BALL_TRAIL_LENGTH; index++) {
			this.lastPositions.push((x, y));
			this.lastColors.push(BALL_COLOR);
		}
		this.state = STATE_IN_FOLLOW

		this.lastPaddleHitId = 0
		this.lastPaddleTeam = TEAM_LEFT

		// For stat
		this.numberOfBounce = 0
	}
	


	resetHitbox()
	{
		this.hitbox.setPos(this.pos)
		this.hitbox.clearPoints()
		let points = getPointOfCircle(this.radius * this.modifierSize, BALL_HITBOX_PRECISION, 360 / (BALL_HITBOX_PRECISION * 2))
		for (let index = 0; index < points.length; index++)
		{
			const p = array[index];
			this.hitbox.addPoint(p[0], p[1]);
		}
	}


	resetModifier()
	{
		this.modifierSpeed = 1
		if (this.modifierSize != 1)
			this.modifySize(1);
		this.modifierSkipCollision = False
		this.modifierInvisibleBall = False
		this.modifierInvisibleBallTimer = 0
		this.modifierWaveBall = False
		this.modifierWaveBallTimer = 0
	}


	modifySize( modifier)
	{
		this.modifierSize = modifier;
		this.sprite = pg.transform.scale(this.originalSprite, ((this.radius * 2) * this.modifierSize, (this.radius * 2) * this.modifierSize));
		this.resetHitbox();
	}


	draw( win)
	{
		//TODO change content to adapt

		if (this.state == STATE_RUN)
		{
			for (let i = 0; i < BALL_TRAIL_LENGTH; i++) {
				gradiant = i / BALL_TRAIL_LENGTH;
				color = (parseInt(this.lastColors[i][0] * BALL_TRAIL_OPACITY),
				parseInt(this.lastColors[i][1] * BALL_TRAIL_OPACITY),
				parseInt(this.lastColors[i][2] * BALL_TRAIL_OPACITY));
				if ((! (this.modifierInvisibleBall)) || (parseInt(this.modifierInvisibleBallTimer * 5) % 2))
					pg.draw.circle(win, color, this.lastPositions[i], (this.radius * gradiant) * this.modifierSize)	
			}


		}
		else if (this.lastPositions[-1] != this.pos.asTupple())
		{
			for (let i = 0; i < BALL_TRAIL_LENGTH; i++)
			{
				this.lastPositions[i] = this.pos.asTupple()
			}
		}

		if ((! (this.modifierInvisibleBall)) || (parseInt(this.modifierInvisibleBallTimer * POWER_UP_BALL_INVISIBLE_SPEED_FACTOR) % 2))
			win.blit(this.sprite, (this.pos.x - (this.radius * this.modifierSize), this.pos.y - (this.radius * this.modifierSize)));
		this.hitbox.draw(win);
	}


	updateTime( delta) {
		if (this.modifierInvisibleBall)
			this.modifierInvisibleBallTimer += delta

		if (this.modifierWaveBall)
			this.modifierWaveBallTimer += delta

		if (this.modifierStopBallTimer > 0)
		{
			this.modifierStopBallTimer -= delta
			if (this.modifierStopBallTimer < 0)
				this.modifierStopBallTimer = 0
		}

		powerUpEffectToRemove = [];

		for (let i = 0; i < this.powerUpEffects.length; i++)
		{
			//TODO : reprrdnre trad ici
			powerUpEffect = this.powerUpEffects[i]
			if (powerUpEffect[1] > 0)
			{
				powerUpEffect[1] -= delta
				// If the time of the power up ended
				if (powerUpEffect[1] < 0)
				{
					powerUpEffect[1] = 0
					powerUpEffectToRemove.append(i)
					// Remove the effect of the power up

					if (powerUpEffect[0] == POWER_UP_BALL_SLOW)
					{
						this.modifierSpeed *= POWER_UP_BALL_SLOW_SPEED_FACTOR
						if (this.modifierSpeed > 1)
							this.modifierSpeed = 1
					}

					else if (powerUpEffect[0] == POWER_UP_BALL_BIG){
						this.modifierSize /= POWER_UP_BALL_BIG_SIZE_FACTOR
						this.modifySize(this.modifierSize)
					}

					else if (powerUpEffect[0] == POWER_UP_BALL_LITTLE)
					{
						this.modifierSize *= POWER_UP_BALL_LITTLE_SIZE_FACTOR
						this.modifySize(this.modifierSize)
					}
				}
			}
		}
		for (let i = 0; i < powerUpEffectToRemove.length; indiex++)
		{
			this.powerUpEffects.pop(powerUpEffectToRemove[i] - i)
		}
	}

	getRealDirection()
	{
		if (! (this.modifierWaveBall))
			return this.direction

		realDirection = this.direction.dup()
		realDirection.rotate(POWER_UP_BALL_WAVE_DEGREES * math.sin(this.modifierWaveBallTimer * POWER_UP_BALL_WAVE_SPEED_FACTOR))

		return realDirection;
	}


	updatePosition( delta, paddlesLeft, paddlesRight, walls, powerUp)
	{
		if (this.state != STATE_RUN || this.modifierStopBallTimer > 0)
			return

		// Store last positions
		// Store last colors
		for (let i = 1; i < BALL_TRAIL_LENGTH; i++)
		{
			this.lastPositions[i - 1] = this.lastPositions[i]
			this.lastColors[i - 1] = this.lastColors[i]
		}
		this.lastPositions[-1] = this.pos.asTupple()
		this.lastColors[-1] = this.color

		// Check position along direction and speed
		deltaSpeed = this.speed * delta * this.modifierSpeed

		nbCheckCollisionStep = int(deltaSpeed / BALL_MOVE_STEP)
		lastStepMove = deltaSpeed - (nbCheckCollisionStep * BALL_MOVE_STEP)
		for (let i = 0; i < nbCheckCollisionStep + 1; i++)
		{
			step = BALL_MOVE_STEP
			if (i == nbCheckCollisionStep)
				step = lastStepMove

			realDirection = this.getRealDirection()
			newpos = this.pos.dup()
			newpos.translateAlong(realDirection, step)
			this.hitbox.setPos(newpos)

			collision = False

			// Collision with powerUp
			if (powerUp[0] == POWER_UP_VISIBLE && this.hitbox.isCollide(powerUp[1]))
			{
				powerUp[0] = POWER_UP_TAKE
				powerUp[2] = this.lastPaddleHitId
			}
			// Collision with paddle
			for (const p of paddlesLeft)
			{
				if (collision)
				{
					realDirection = this.getRealDirection()
					newpos = this.pos.dup()
					newpos.translateAlong(realDirection, step)
					collision = False
				}
				collision = this.makeCollisionWithPaddle(p)
			}
			for (const p of paddlesRight)
			{
				if (collision){
					realDirection = this.getRealDirection()
					newpos = this.pos.dup()
					newpos.translateAlong(realDirection, step)
					collision = False
				}
				collision = this.makeCollisionWithPaddle(p)
			}

			// Collision with wall
			for (const w of walls)
			{
				if (collision)
				{
					realDirection = this.getRealDirection()
					newpos = this.pos.dup()
					newpos.translateAlong(realDirection, step)
					collision = False
				}
				collision = this.makeCollisionWithWall(w)
			}

			if (collision)
			{
				realDirection = this.getRealDirection()
				newpos = this.pos.dup()
				newpos.translateAlong(realDirection, step)
			}

			// Check if ball is in goal
			if (newpos.x - this.radius < AREA_RECT[0])
			{
				this.state = STATE_IN_GOAL_LEFT
				this.resetModifier()
				this.powerUpEffects.clear()
				return
			}

			if (newpos.x + this.radius > AREA_RECT[0] + AREA_RECT[2])
			{
				this.state = STATE_IN_GOAL_RIGHT
				this.resetModifier()
				this.powerUpEffects.clear()
				return
			}

			// Teleport from up to down
			if (newpos.y + this.radius < AREA_RECT[1])
			{
				newpos.y += AREA_RECT[3]
				this.resetHitbox()
			}
			// Teleport from down to up
			else if (newpos.y - this.radius > AREA_RECT[1] + AREA_RECT[3])
			{
				newpos.y -= AREA_RECT[3]
				this.resetHitbox()
			}

			// Affect position along direction and
			this.pos = newpos.dup()
			this.hitbox.setPos(this.pos)
		}

		if (this.speed < BALL_MAX_SPEED / 2)
		{
			green_gradient = 1 - this.speed / BALL_MAX_SPEED
			blue_gradient = 1 - this.speed / BALL_MAX_SPEED
		}
		else
		{
			green_gradient = this.speed / BALL_MAX_SPEED
			blue_gradient = 1 - this.speed / BALL_MAX_SPEED
		}

		// Trail color
		// If the ball is faster than normal, change tail color
		if (this.modifierSpeed > 1)
		{
			this.color =	(BALL_COLOR[0] * green_gradient,
							BALL_COLOR[1] * blue_gradient,
							BALL_COLOR[2])
		}
		// Idem if slower
		else if (this.modifierSpeed < 1)
		{
			this.color =	(BALL_COLOR[0] * blue_gradient,
							BALL_COLOR[1],
							BALL_COLOR[2]* green_gradient)
		}
		else
		{
			this.color =	(BALL_COLOR[0],
							BALL_COLOR[1] * green_gradient,
							BALL_COLOR[2] * blue_gradient)
		}

		// Friction
		if (BALL_FRICTION && this.speed > 0)
		{
			this.speed -= max(BALL_MINIMUM_FRICTION, (this.speed * BALL_FRICTION_STRENGTH)) * delta
			if (this.speed < 0)
				this.speed = 0
		}
	}


	setPos( pos)
	{
		this.pos = pos
		for (let i = 0; i < BALL_TRAIL_LENGTH; i++)
		{
			this.lastColors[i] = this.color
			this.lastPositions[i] = this.pos.asTupple()		
		}
	}


	makeCollisionWithWall( hitboxe)
	{
		if (this.modifierSkipCollision)
			return False

		if (! (hitboxe.isCollide(this.hitbox)))
			return False

		collideInfos = hitboxe.getCollideInfo(this.hitbox)

		collide = False

		hitPos = []
		newDirections = []

		nbCollide = 0
		for (const collideInfo of collideInfos)
		{
			if (collideInfo[0])
			{
				hitPos.append(collideInfo[3])
				nbCollide += 1
				p0 = collideInfo[1]
				p1 = collideInfo[2]
				normal = getNormalOfSegment(p0, p1)
				direction = reflectionAlongVec2(normal, this.direction)
				newDirections.append(direction.dup())
				this.speed += BALL_WALL_ACCELERATION
				if (this.speed > BALL_MAX_SPEED)
					this.speed = BALL_MAX_SPEED
				// Bounce stat
				this.numberOfBounce += 1
				collide = true
			}
		}
		if (len(newDirections) == 1)
			this.direction = newDirections[0].dup()
		else if (len(newDirections) > 1)
		{
			p1 = hitPos[0]
			p2 = hitPos[1]
			normal = getNormalOfSegment(p1, p2)
			this.direction = reflectionAlongVec2(normal, this.direction)
		}
		return collide
	}


	makeCollisionWithPaddle( paddlee)
	{
		if (! (paddlee.hitbox.isCollide(this.hitbox)))
			return False

		// Speed stat
		realSpeed = this.speed * this.modifierSpeed
		if (realSpeed > paddlee.maxSpeedBallTouch)
			paddlee.maxSpeedBallTouch = realSpeed

		// Bounce stat
		this.numberOfBounce = 0

		// New dir of ball
		diffY = this.pos.y - paddlee.pos.y
		diffY /= (paddlee.h * paddlee.modifierSize) / 2

		if (paddlee.pos.x < this.pos.x)
			newDir = Vec2(1, diffY)
		else
			newDir = Vec2(-1, diffY)

		newDir.normalize()
		this.direction = newDir

		// Accelerate ball after hit paddle
		this.speed += BALL_PADDLE_ACCELERATION
		if (this.speed > BALL_MAX_SPEED)
			this.speed = BALL_MAX_SPEED

		this.lastPaddleHitId = paddlee.id
		this.lastPaddleTeam = paddlee.team

		// Reset modifier
		this.modifierSkipCollision = False

		this.modifierInvisibleBall = False
		this.modifierInvisibleBallTimer = 0

		this.modifierWaveBall = False
		this.modifierWaveBallTimer = 0
		if (this.modifierSpeed > 1)
			this.modifierSpeed = 1

		// If the paddle have power up in charge, apply them to the ball
		if (paddle.powerUpInCharge.length > 0)
		{
			for (const powerUp of paddlee.powerUpInCharge)
			{
				if (powerUp == POWER_UP_BALL_FAST)
				{
					this.modifierSpeed *= POWER_UP_BALL_FAST_FACTOR
					this.modifierStopBallTimer = POWER_UP_BALL_FAST_TIME_STOP
					for (let i = 0; i < this.lastPositions.length; i++) {
						const element = array[i];
						this.lastPositions[i] = this.pos.asTupple()
						
					}
				}
				else if (powerUp == POWER_UP_BALL_WAVE)
					this.modifierWaveBall = true

				else if (powerUp == POWER_UP_BALL_INVISIBLE)
					this.modifierInvisibleBall = true
			}

			paddle.powerUpInCharge.clear()
		}
		return true
	}

	setModifierByState( state)
	{
		this.modifierSpeed = state["modifierSpeed"]
		if (this.modifierSize != state["modifierSize"])
		{
			this.modifierSize = state["modifierSize"]
			this.modifySize(this.modifierSize)
		}
		this.modifierStopBallTimer = state["modifierStopBallTimer"]
		this.modifierSkipCollision = state["modifierSkipCollision"]
		this.modifierInvisibleBall = state["modifierInvisibleBall"]
		this.modifierInvisibleBallTimer = state["modifierInvisibleBallTimer"]
		this.modifierWaveBall = state["modifierWaveBall"]
		this.modifierWaveBallTimer = state["modifierWaveBallTimer"]
	}
}