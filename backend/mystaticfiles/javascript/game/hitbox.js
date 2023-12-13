// from client_side.vec2 import *
// from client_side.client_define import *

// import pygame as pg
// import math


function collideBetweenSegments(p1, p2, p3, p4)
{
	divisor = (p1.x - p2.x) * (p3.y - p4.y) - (p1.y - p2.y) * (p3.x - p4.x)
	if (divisor == 0)
		return False, None

	t = (p1.x - p3.x) * (p3.y - p4.y) - (p1.y - p3.y) * (p3.x - p4.x)
	t /= divisor

	if (t < 0 || 1 < t)
		return False, None

	u = (p1.x - p3.x) * (p1.y - p2.y) - (p1.y - p3.y) * (p1.x - p2.x)
	u /= divisor

	if (u < 0 || 1 < u)
		return False, None

	// Point of intersection
	s1Dir = vec2Sub(p2, p1)
	p = p1.dup()
	p.translateAlong(s1Dir, t)

	return true, p1, p2, p
}


class Hitbox {
	constructor ( x, y, color, fillColor = (255, 255, 255))
	{
		this.pos = Vec2(x, y)

		this.color = color
		this.fillColor = fillColor

		this.rect = [0, 0, 0, 0]

		this.rotation = 0

		this.points = []
	}


	print()
	{
		return "<hitbox:" + str(this.pos.x) + ", " + str(this.pos.y) + "| " + str(len(this.points)) + " points >"
	}


	addPoint( x, y)
	{
		this.points.append(Vec2(this.pos.x + x, this.pos.y + y))
		this.computeSurroundingRect()
	}


	addPoints( lst)
	{
		for (const pair of lst)
		{
			const x = pair[0];
			const y = pair[1];
			this.points.append(Vec2(this.pos.x + x, this.pos.y + y))
			this.computeSurroundingRect()
		}
	}


	clearPoints()
	{
		this.points.clear()
	}


	computeSurroundingRect()
	{
		if (this.points.length == 0)
			return

		pos = this.points[0].asTuppleCenter(this.pos.x, this.pos.y)

		xLeft = pos[0]
		xRight = pos[0]
		yUp = pos[1]
		yDown = pos[1]
			const element = array[index];
			

		for (let i = 1; i < this.points.length; i++)
		{
			pos = this.points[i].asTuppleCenter(this.pos.x, this.pos.y)

			if (pos[0] < xLeft)
				xLeft = pos[0]
			else if (pos[0] > xRight)
				xRight = pos[0]

			if (pos[1] < yUp)
				yUp = pos[1]
			else if (pos[1] > yDown)
				yDown = pos[1]
		}

		this.rect[0] = xLeft + this.pos.x
		this.rect[2] = xRight - xLeft + 1
		this.rect[1] = yUp + this.pos.y
		this.rect[3] = yDown - yUp + 1
	}


	setPos( vec)
	{
		dx = vec.x - this.pos.x
		dy = vec.y - this.pos.y
		this.pos = vec
		for (let i = 0; i < this.points.length; i++)
			this.points[i].translate(dx, dy)
		this.computeSurroundingRect()
	}


	move( x, y)
	{
		this.pos.add(Vec2(x, y))
		for (let i = 0; i < this.points.length; i++)
			this.points[i].translate(x, y)
		this.computeSurroundingRect()
	}


	rotate( degrees)
	{
		this.rotation += degrees

		radiant = degrees * (math.pi / 180)
		sinTmp = math.sin(radiant)
		cosTmp = math.cos(radiant)

		for (let i = 0; i < this.points.length; i++)
			this.points[i].rotateAround(this.pos.x, this.pos.y, sinTmp, cosTmp)
		this.computeSurroundingRect()
	}


	drawNormals( win)
	{
		for (let i = 1; i < this.points.length; i++)
		{
			segDir = vec2Sub(this.points[i], this.points[i - 1])
			segNorm = segDir.norm()
			segDir.divide(segNorm)
			segNormal = getNormalOfSegment(this.points[i], this.points[i - 1])

			startPoint = this.points[i - 1].dup()
			startPoint.translateAlong(segDir, segNorm / 2)

			endPoint = startPoint.dup()
			endPoint.translateAlong(segNormal, 20)

			pg.draw.line(win, this.color, startPoint.asTupple(), endPoint.asTupple(), 1)
		}
	}


	draw( win)
	{
		//TODO change to correct transition

		if (DRAW_HITBOX)
			points = []
			for (const p of this.points)
				points.append(p.asTupple())

			pg.draw.polygon(win, this.color, points, 1)

		if (DRAW_HITBOX_NORMALS)
			this.drawNormals(win)
	}


	drawFill( win)
	{
		//TODO change to correct transition

		points = []
		for (const p of this.points)
			points.append(p.asTupple())

		pg.draw.polygon(win, this.fillColor, points)
	}


	isCollide( hitbox)
	{
		pointsSize = this.points.length
		if (pointsSize <= 1)
			return False

		hitboxPointsSize = len(hitbox.points)
		if (hitboxPointsSize <= 1)
			return False

		if (this.rect[0] + this.rect[2] >= hitbox.rect[0] && this.rect[0] <= hitbox.rect[0] + hitbox.rect[2] &&
			this.rect[1] + this.rect[3] >= hitbox.rect[1] && this.rect[1] <= hitbox.rect[1] + hitbox.rect[3])
		{

		for (let i = 1; i < pointsSize; i++)
			{
				p0 = this.points[i - 1]
				p1 = this.points[i]

				for (let j = 1; j < hitboxPointsSize; i++)
				{
					p2 = hitbox.points[j - 1]
					p3 = hitbox.points[j]

					if (collideBetweenSegments(p0, p1, p2, p3)[0])
						return true
				}
			}
		}

		return false
	}


	isInside( hitbox)
	{
		pointsSize = this.points.length
		if (pointsSize <= 1)
			return false

		hitboxPointsSize = hitbox.points.length
		if (hitboxPointsSize <= 1)
			return false

		if (this.rect[0] + this.rect[2] >= hitbox.rect[0] && this.rect[0] <= hitbox.rect[0] + hitbox.rect[2] &&
			this.rect[1] + this.rect[3] >= hitbox.rect[1] && this.rect[1] <= hitbox.rect[1] + hitbox.rect[3])
		{


			for (let i = 0; i < pointsSize; i++)
			{
				p = this.points[i]
				pLeft = Vec2(p.x - 1000, p.y)
				pRight = Vec2(p.x + 1000, p.y)

				nbCollideLeft = 0
				nbCollideRight = 0
				for (let j = 1; j < hitboxPointsSize; i++)
				{
					p2 = hitbox.points[j - 1]
					p3 = hitbox.points[j]

					if (collideBetweenSegments(p, pLeft, p2, p3)[0])
						nbCollideLeft += 1
					if (collideBetweenSegments(p, pRight, p2, p3)[0])
						nbCollideRight += 1
				}

				if (nbCollideLeft > 0 && nbCollideRight > 0 && (nbCollideLeft % 2 == 1 || nbCollideRight % 2 == 1))
					return true
			}
		}
		return false
	}


	isInsideSurrondingBox( hitbox)
	{
		pointsSize = this.points.length
		if (pointsSize <= 1)
			return false

		hitboxPointsSize = hitbox.points.length
		if (hitboxPointsSize <= 1)
			return false

		if (this.rect[0] + this.rect[2] >= hitbox.rect[0] && this.rect[0] <= hitbox.rect[0] + hitbox.rect[2] &&
			this.rect[1] + this.rect[3] >= hitbox.rect[1] && this.rect[1] <= hitbox.rect[1] + hitbox.rect[3])
				return true
		return false
	}


	getCollideInfo( hitbox)
	{
		collideInfos = []
		for (let i = 1; i < this.points.length; i++)
		{
			p0 = this.points[i - 1]
			p1 = this.points[i]

			for (let j = 1; j < hitbox.points.length; i++)
			{
				p2 = hitbox.points[j - 1]
				p3 = hitbox.points[j]

				collideInfos.append(collideBetweenSegments(p0, p1, p2, p3))
			}
		}
		return collideInfos
	}
}