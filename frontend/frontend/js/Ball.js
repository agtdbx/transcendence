/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   Ball.js                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: lflandri <lflandri@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/11/07 13:26:59 by lflandri          #+#    #+#             */
/*   Updated: 2023/11/07 13:51:44 by lflandri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

import '/js/define.js';
import '/js/vec2.js';
import '/js/hitbox.js';


class Ball
{
	constructor(x, y)
	{
		this.pos = Vec2(x, y)
		this.radius = BALL_RADIUS
		this.color = BALL_COLOR
		sprite = "/image/ball.png"
		this.sprite 
		this.hitbox = hitbox.Hitbox(x, y, HITBOX_BALL_COLOR)
		this.hitbox.addPoint(0, -18.5)
		this.hitbox.addPoint(11.5, - 14.5)
		this.hitbox.addPoint(18.5, - 5.5)
		this.hitbox.addPoint(17.5, 7.5)
		this.hitbox.addPoint(11.5, 15.5)
		this.hitbox.addPoint(0, 18.5)
		this.hitbox.addPoint(-10.5, 15.5)
		this.hitbox.addPoint(-16.5, 6.5)
		this.hitbox.addPoint(-16.5, -6.5)
		this.hitbox.addPoint(-9.5, -13.5)
		this.speed = 0
		this.direction = Vec2(0, 0)
		this.lastPositions = [];
		for (let index = 0; index < BALL_TRAIL_LENGTH; index++)
		{
			this.lastPositions.push((x, y));
		}
		this.inWaiting = False
	}


	draw(win)
	{
		if (this.inWaiting)
			return;

		for (let i = 0; i < BALL_TRAIL_LENGTH; i++) {
			gradiant = i / BALL_TRAIL_LENGTH
			color = (int(this.lastColors[i][0] * BALL_TRAIL_OPACITY),
					int(this.lastColors[i][1] * BALL_TRAIL_OPACITY),
					int(this.lastColors[i][2] * BALL_TRAIL_OPACITY))
			pg.draw.circle(win, color, this.lastPositions[i], this.radius * gradiant)	
		}
		win.blit(this.sprite, (this.pos.x - this.radius, this.pos.y - this.radius))
		this.hitbox.draw(win)
	}

	affecteDirection(this, mousePos)
	{
		if (this.inWaiting)
			return

		vecDir = Vec2(mousePos[0] - this.pos.x, mousePos[1] - this.pos.y)
		norm = vecDir.norm()
		vecDir.divide(norm)

		if (norm != 0)
		{
			this.speed += norm
			if (this.speed > BALL_MAX_SPEED)
			{
				this.speed = BALL_MAX_SPEED
			}

			this.direction.add(vecDir)
			this.direction.normalize()
		}
	}

	def updatePosition(this, delta, walls):
		if this.inWaiting:
			return

		# Store last positions
		for i in range (1, BALL_TRAIL_LENGTH):
			this.lastPositions[i - 1] = this.lastPositions[i]
		this.lastPositions[-1] = this.pos.asTupple()

		# Store last colors
		for i in range (1, BALL_TRAIL_LENGTH):
			this.lastColors[i - 1] = this.lastColors[i]
		this.lastColors[-1] = this.color

		# Check position along direction and speed
		deltaSpeed = this.speed * delta

		# Collision with wall
		newpos = this.pos.dup()
		newpos.translateAlong(this.direction, deltaSpeed)
		this.hitbox.setPos(newpos.x, newpos.y)
		for w in walls:
			this.makeCollisionWithWall(w)

		newpos = this.pos.dup()
		newpos.translateAlong(this.direction, deltaSpeed)

		# Ball in goal
		if newpos.x - this.radius < AREA_RECT[0] or newpos.x + this.radius > AREA_RECT[0] + AREA_RECT[2]:
			this.inWaiting = True

		# Teleport into the other x wall
		if newpos.y + this.radius < AREA_RECT[1]:
			newpos.y += AREA_BORDER_RECT[3]
		elif newpos.y - this.radius > AREA_RECT[1] + AREA_RECT[3]:
			newpos.y -= AREA_BORDER_RECT[3]

		# Affect position along direction and
		this.pos = newpos

		this.hitbox.setPos(this.pos.x, this.pos.y)

		if this.speed < BALL_MAX_SPEED / 2:
			green_gradient = 1 - this.speed / BALL_MAX_SPEED
			blue_gradient = 1 - this.speed / BALL_MAX_SPEED
		else:
			green_gradient = this.speed / BALL_MAX_SPEED
			blue_gradient = 1 - this.speed / BALL_MAX_SPEED
		this.color =	(BALL_COLOR[0],
						BALL_COLOR[1] * green_gradient,
						BALL_COLOR[2] * blue_gradient)

		# Friction
		if this.speed > 0:
			this.speed -= max(BALL_MINIMUM_FRICTION, (this.speed * BALL_FRICTION_STRENGTH)) * delta
			if this.speed < 0:
				this.speed = 0


	def makeCollisionWithWall(this, hitbox):
		if not hitbox.isCollide(this.hitbox):
			return

		collideInfos = hitbox.getCollideInfo(this.hitbox)

		for collideInfo in collideInfos:
			if collideInfo[0]:
				p0 = collideInfo[1]
				p1 = collideInfo[2]
				normal = getNormalOfSegment(p0, p1)
				this.direction = reflectionAlongVec2(normal, this.direction)
				break
}