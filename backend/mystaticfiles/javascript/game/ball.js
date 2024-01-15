import * as dc from "./client_define.js"
import * as d from "./define.js"
import {Vec2, getNormalOfSegment, reflectionAlongVec2} from "./vec2.js"
import "./hitbox.js"
import * as hitbox from "./hitbox.js"
import * as paddle from "./paddle.js"

// import pygame as pg

const NB_SHADOW_BALL = 10

export function getPointOfCircle(radius, precision, beginDegree = 0)
{
	let points = []
	for (let i = 0; i < precision; i++)
	{
		let degree = 360 / precision * i + beginDegree
		let radian = degree * (Math.PI / 180)
		let x = radius * Math.cos(radian)
		let y = radius * Math.sin(radian)
		points.push([x, y])
	}
	return points
}



export class Ball {
	constructor ( x, y)
	{
		this.maxXtest = 0;
		// Geometry
		this.pos = new Vec2(x, y)
		this.radius = d.BALL_RADIUS
		this.speed = d.BALL_START_SPEED
		this.direction = new Vec2(1, 0)
		this.htmlObject = document.createElementNS('http://www.w3.org/2000/svg', 'image')
		this.htmlObject.setAttributeNS('http://www.w3.org/1999/xlink','href', "/static/image/game/ball.png");
		// this.htmlObject.setAttribute('transform-origin', "center");
		console.log("create ball at : " + x + "," + y)
		this.shadowBalls = []
		for (let index = 0; index < NB_SHADOW_BALL; index++)
		{
			let array = []
			let newShadowBall = document.createElementNS('http://www.w3.org/2000/svg', 'image')
			newShadowBall.setAttributeNS('http://www.w3.org/1999/xlink','href', "/static/image/game/ball.png");
			newShadowBall.style.opacity = "" + (1 / NB_SHADOW_BALL)
			newShadowBall.setAttribute('x',  x - (this.radius / 2));
			newShadowBall.setAttribute('y',  y - (this.radius / 2));
			array.push(newShadowBall)
			array.push([x - (this.radius / 2), y - (this.radius / 2)])
			this.shadowBalls.push(array)
			
			
		}



		// Graphique
		this.color = d.BALL_COLOR
		// this.originalSprite = pg.image.load("client_side/imgs/ball.png")
		// this.sprite = pg.transform.scale(this.originalSprite, (this.radius * 2, this.radius * 2))

		// Hitbox creation
		this.hitbox = new hitbox.Hitbox(this.pos.x, this.pos.y, d.HITBOX_BALL_COLOR)
		this.hitbox.setPos(this.pos)
		let points = getPointOfCircle(this.radius, d.BALL_HITBOX_PRECISION, 360 / (d.BALL_HITBOX_PRECISION * 2))

		for (let index = 0; index < points.length; index++)
		{
			let p = points[index]
			this.hitbox.addPoint(p[0], p[1]);
		}

		// Modifier
		this.modifierSpeed = 1
		this.modifierSize = 1
		this.modifierSkipCollision = false
		this.modifierInvisibleBall = false
		this.modifierInvisibleBallTimer = 0
		this.modifierWaveBall = false
		this.modifierWaveBallTimer = 0
		this.modifierStopBallTimer = 0

		// Represente the effect on ball [POWER_UP, TIME_EFFECT]
		this.powerUpEffects = []

		this.lastPositions = [];
		this.lastColors = [];
		for (let index = 0; index < d.BALL_TRAIL_LENGTH; index++) {
			this.lastPositions.push([x, y]);
			this.lastColors.push(BALL_COLOR);
		}
		this.state = d.STATE_RUN

		this.lastPaddleHitId = 0
		this.lastPaddleTeam = dc.TEAM_LEFT

		// For stat
		this.numberOfBounce = 0
	}
	


	resetHitbox()
	{
		this.hitbox.setPos(this.pos)
		this.hitbox.clearPoints()
		let points = getPointOfCircle(this.radius * this.modifierSize, d.BALL_HITBOX_PRECISION, 360 / (d.BALL_HITBOX_PRECISION * 2))
		for (let index = 0; index < points.length; index++)
		{
			const p = points[index];
			this.hitbox.addPoint(p[0], p[1]);
		}
	}


	resetModifier()
	{
		this.modifierSpeed = 1
		if (this.modifierSize != 1)
			this.modifySize(1);
		this.modifierSkipCollision = false
		this.modifierInvisibleBall = false
		this.modifierInvisibleBallTimer = 0
		this.modifierWaveBall = false
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

		if (this.state == d.STATE_RUN)
		{
			for (let i = 0; i < d.BALL_TRAIL_LENGTH; i++) {
				let gradiant = i / d.BALL_TRAIL_LENGTH;
				let color = (parseInt(this.lastColors[i][0] * d.BALL_TRAIL_OPACITY),
				parseInt(this.lastColors[i][1] * d.BALL_TRAIL_OPACITY),
				parseInt(this.lastColors[i][2] * d.BALL_TRAIL_OPACITY));
				// if ((! (this.modifierInvisibleBall)) || (parseInt(this.modifierInvisibleBallTimer * 5) % 2))
				// 	pg.draw.circle(win, color, this.lastPositions[i], (this.radius * gradiant) * this.modifierSize)	
			}


		}
		else if (this.lastPositions[-1] != this.pos.asTupple())
		{
			for (let i = 0; i < d.BALL_TRAIL_LENGTH; i++)
			{
				this.lastPositions[i] = this.pos.asTupple()
			}
		}

		// if ((! (this.modifierInvisibleBall)) || (parseInt(this.modifierInvisibleBallTimer * d.POWER_UP_BALL_INVISIBLE_SPEED_FACTOR) % 2))
		// 	win.blit(this.sprite, (this.pos.x - (this.radius * this.modifierSize), this.pos.y - (this.radius * this.modifierSize)));
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

		let powerUpEffectToRemove = [];

		for (let i = 0; i < this.powerUpEffects.length; i++)
		{
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

					if (powerUpEffect[0] == d.POWER_UP_BALL_SLOW)
					{
						this.modifierSpeed *= d.POWER_UP_BALL_SLOW_SPEED_FACTOR
						if (this.modifierSpeed > 1)
							this.modifierSpeed = 1
					}

					else if (powerUpEffect[0] == d.POWER_UP_BALL_BIG){
						this.modifierSize /= d.POWER_UP_BALL_BIG_SIZE_FACTOR
						this.modifySize(this.modifierSize)
					}

					else if (powerUpEffect[0] == d.POWER_UP_BALL_LITTLE)
					{
						this.modifierSize *= d.POWER_UP_BALL_LITTLE_SIZE_FACTOR
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
		realDirection.rotate(d.POWER_UP_BALL_WAVE_DEGREES * Math.sin(this.modifierWaveBallTimer * d.POWER_UP_BALL_WAVE_SPEED_FACTOR))

		return realDirection;
	}


	updatePosition( delta, paddlesLeft, paddlesRight, walls, powerUp)
	{
		// console.log("before :")
		// this.pos.print()



		if (this.state != d.STATE_RUN || this.modifierStopBallTimer > 0)
			return
		// Store last positions
		// Store last colors
		for (let i = 1; i < dc.BALL_TRAIL_LENGTH; i++)
		{
			this.lastPositions[i - 1] = this.lastPositions[i]
			this.lastColors[i - 1] = this.lastColors[i]
		}
		this.lastPositions[-1] = this.pos.asTupple()
		this.lastColors[-1] = this.color

		// Check position along direction and speed
		let deltaSpeed = this.speed * delta * this.modifierSpeed

		let nbCheckCollisionStep = Math.floor(deltaSpeed / d.BALL_MOVE_STEP)
		// console.log("==========")
		// console.log("deltaSpeed : " + deltaSpeed)
		// console.log("nb step : " + nbCheckCollisionStep)
		// console.log("==========")

		let lastStepMove = deltaSpeed - (nbCheckCollisionStep * d.BALL_MOVE_STEP)
		for (let i = 0; i < nbCheckCollisionStep + 1; i++)
		{
			let step = d.BALL_MOVE_STEP
			if (i == nbCheckCollisionStep)
				step = lastStepMove

			let realDirection = this.getRealDirection()
			let newpos = this.pos.dup()
			newpos.translateAlong(realDirection, step)
			// console.log("temp pos vect :")
			// newpos.print()
			this.hitbox.setPos(newpos)

			let collision = false

			// Collision with powerUp
			if (powerUp[0] == d.POWER_UP_VISIBLE && this.hitbox.isCollide(powerUp[1]))
			{
				powerUp[0] = d.POWER_UP_TAKE
				powerUp[2] = this.lastPaddleHitId
			}
			// Collision with paddle
			// console.log("colistion paddle")
			for (const p of paddlesLeft)
			{
				// console.log("test left")

				if (collision)
				{
					realDirection = this.getRealDirection()
					newpos = this.pos.dup()
					newpos.translateAlong(realDirection, step)
					collision = false
				}
				collision = this.makeCollisionWithPaddle(p)
			}
			for (const p of paddlesRight)
			{
				// console.log("test right")

				if (collision){
					realDirection = this.getRealDirection()
					newpos = this.pos.dup()
					newpos.translateAlong(realDirection, step)
					collision = false
				}
				collision = this.makeCollisionWithPaddle(p)
			}
			// console.log(" end colistion paddle")


			// Collision with wall
			for (const w of walls)
			{
				if (collision)
				{
					realDirection = this.getRealDirection()
					newpos = this.pos.dup()
					newpos.translateAlong(realDirection, step)
					collision = false
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
			if (newpos.x - this.radius < dc.AREA_RECT[0])
			{
				this.state = d.STATE_IN_GOAL_LEFT
				this.resetModifier()
				this.powerUpEffects = []
				return
			}

			if (newpos.x + this.radius > dc.AREA_RECT[0] + dc.AREA_RECT[2])
			{
				this.state = d.STATE_IN_GOAL_RIGHT
				this.resetModifier()
				this.powerUpEffects = []
				return
			}

			// Teleport from up to down
			if (newpos.y + this.radius < dc.AREA_RECT[1])
			{
				newpos.y += dc.AREA_RECT[3]
				this.resetHitbox()
			}
			// Teleport from down to up
			else if (newpos.y - this.radius > dc.AREA_RECT[1] + dc.AREA_RECT[3])
			{
				newpos.y -= dc.AREA_RECT[3]
				this.resetHitbox()
			}

			// Affect position along direction and
			//TODO add change trainer ici
			for (let index = 0; index < NB_SHADOW_BALL - 1; index++)
			{
				this.shadowBalls[index][1] = this.shadowBalls[index + 1][1]
				console.log(this.shadowBalls[index])
				this.shadowBalls[index][0].setAttribute('x', "" +  this.shadowBalls[index + 1][1][0]);
				this.shadowBalls[index][0].setAttribute('y', "" +  this.shadowBalls[index + 1][1][1]);
			}
			this.shadowBalls[NB_SHADOW_BALL - 1][1] = [(this.pos.x - (this.radius / 2)), (this.pos.y - (this.radius / 2))]
			
			this.pos = newpos.dup()
			this.htmlObject.setAttribute('x', "" + (this.pos.x - (this.radius / 2)));
			this.htmlObject.setAttribute('y', "" + (this.pos.y - (this.radius / 2)));
			this.hitbox.setPos(this.pos)
		}
		// console.log("after :")
		// this.pos.print()
		// this.direction.print()
		let green_gradient = 0
		let blue_gradient = 0
		if (this.speed < d.BALL_MAX_SPEED / 2)
		{
			green_gradient = 1 - this.speed / d.BALL_MAX_SPEED
			blue_gradient = 1 - this.speed / d.BALL_MAX_SPEED
		}
		else
		{
			green_gradient = this.speed / d.BALL_MAX_SPEED
			blue_gradient = 1 - this.speed / d.BALL_MAX_SPEED
		}

		// Trail color
		// If the ball is faster than normal, change tail color
		if (this.modifierSpeed > 1)
		{
			this.color =	(dc.BALL_COLOR[0] * green_gradient,
							dc.BALL_COLOR[1] * blue_gradient,
							dc.BALL_COLOR[2])
		}
		// Idem if slower
		else if (this.modifierSpeed < 1)
		{
			this.color =	(dc.BALL_COLOR[0] * blue_gradient,
				dc.BALL_COLOR[1],
				dc.BALL_COLOR[2]* green_gradient)
		}
		else
		{
			this.color =	(dc.BALL_COLOR[0],
				dc.BALL_COLOR[1] * green_gradient,
				dc.BALL_COLOR[2] * blue_gradient)
		}

		// Friction
		if (d.BALL_FRICTION && this.speed > 0)
		{
			this.speed -= max(d.BALL_MINIMUM_FRICTION, (this.speed * d.BALL_FRICTION_STRENGTH)) * delta
			if (this.speed < 0)
				this.speed = 0
		}
	}


	setPos( pos)
	{
		this.pos = pos
		this.htmlObject.setAttribute('x', "" + this.pos.x);
		this.htmlObject.setAttribute('y', "" + this.pos.y);
		for (let i = 0; i < BALL_TRAIL_LENGTH; i++)
		{
			this.lastColors[i] = this.color
			this.lastPositions[i] = this.pos.asTupple()		
		}
	}


	makeCollisionWithWall( hitboxe)
	{
		if (this.modifierSkipCollision)
			return false
		
		if (! (hitboxe.isCollide(this.hitbox)))
			return false

		// console.log("colision detected")

		let collideInfos = hitboxe.getCollideInfo(this.hitbox)

		let collide = false

		let hitPos = []
		let newDirections = []

		let nbCollide = 0
		for (const collideInfo of collideInfos)
		{
			if (collideInfo[0])
			{
				hitPos.push(collideInfo[3])
				nbCollide += 1
				let p0 = collideInfo[1]
				let p1 = collideInfo[2]
				let normal = getNormalOfSegment(p0, p1)
				let direction = reflectionAlongVec2(normal, this.direction)
				newDirections.push(direction.dup())
				this.speed += d.BALL_WALL_ACCELERATION
				if (this.speed > d.BALL_MAX_SPEED)
					this.speed = d.BALL_MAX_SPEED
				// Bounce stat
				this.numberOfBounce += 1
				collide = true
			}
		}
		if (newDirections.length == 1)
			this.direction = newDirections[0].dup()
		else if (newDirections.length > 1)
		{
			let p1 = hitPos[0]
			let p2 = hitPos[1]
			let normal = getNormalOfSegment(p1, p2)
			this.direction = reflectionAlongVec2(normal, this.direction)
		}
		// console.log("colide : " + collide)
		return collide
	}


	makeCollisionWithPaddle( paddlee)
	{
		// console.log(" ")
		// console.log(" ")
		// console.log(" ")
		// console.log("test colision")
		// console.log("ball : " + this.state)
		// this.hitbox.print()
		// console.log(" ")
		// console.log(" paddle : " )
		// paddlee.hitbox.print()

		if (!(paddlee.hitbox.isCollide(this.hitbox)))
		{
			// console.log("echec colision")
			return false
		}
		// console.log("colition")
		// Speed stat
		let realSpeed = this.speed * this.modifierSpeed
		if (realSpeed > paddlee.maxSpeedBallTouch)
			paddlee.maxSpeedBallTouch = realSpeed

		// Bounce stat
		this.numberOfBounce = 0

		// New dir of ball
		let diffY = this.pos.y - paddlee.pos.y
		diffY /= (paddlee.h * paddlee.modifierSize) / 2
		let newDir = null
		if (paddlee.pos.x < this.pos.x)
			newDir = new Vec2(1, diffY)
		else
			newDir = new Vec2(-1, diffY)

		newDir.normalize()
		this.direction = newDir

		// Accelerate ball after hit paddle
		this.speed += d.BALL_PADDLE_ACCELERATION
		if (this.speed > d.BALL_MAX_SPEED)
			this.speed = d.BALL_MAX_SPEED

		this.lastPaddleHitId = paddlee.id
		this.lastPaddleTeam = paddlee.team

		// Reset modifier
		this.modifierSkipCollision = false

		this.modifierInvisibleBall = false
		this.modifierInvisibleBallTimer = 0

		this.modifierWaveBall = false
		this.modifierWaveBallTimer = 0
		if (this.modifierSpeed > 1)
			this.modifierSpeed = 1

		// If the paddle have power up in charge, apply them to the ball
		if (paddlee.powerUpInCharge.length > 0)
		{
			for (const powerUp of paddlee.powerUpInCharge)
			{
				if (powerUp == d.POWER_UP_BALL_FAST)
				{
					this.modifierSpeed *= d.POWER_UP_BALL_FAST_FACTOR
					this.modifierStopBallTimer = d.POWER_UP_BALL_FAST_TIME_STOP
					for (let i = 0; i < this.lastPositions.length; i++)
					{
						this.lastPositions[i] = this.pos.asTupple()
						
					}
				}
				else if (powerUp == d.POWER_UP_BALL_WAVE)
					this.modifierWaveBall = true

				else if (powerUp == d.POWER_UP_BALL_INVISIBLE)
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