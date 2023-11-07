/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   HitBox.js                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: lflandri <lflandri@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/11/07 13:28:22 by lflandri          #+#    #+#             */
/*   Updated: 2023/11/07 13:32:01 by lflandri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

from vec2 import *
from define import *

import pygame as pg
import math


def collideBetweenSegments(p1, p2, p3, p4):
	divisor = (p1.x - p2.x) * (p3.y - p4.y) - (p1.y - p2.y) * (p3.x - p4.x)
	if divisor == 0:
		return False, None

	t = (p1.x - p3.x) * (p3.y - p4.y) - (p1.y - p3.y) * (p3.x - p4.x)
	t /= divisor

	if t < 0 or 1 < t:
		return False, None

	u = (p1.x - p3.x) * (p1.y - p2.y) - (p1.y - p3.y) * (p1.x - p2.x)
	u /= divisor

	if u < 0 or 1 < u:
		return False, None

	# Point of intersection
	# s1Dir = vec2Sub(p2, p1)
	# p = p1.dup()
	# p.translateAlong(s1Dir, t)

	return True, p1, p2


class Hitbox:
	def __init__(self, x, y, color, fillColor = (255, 255, 255)):
		self.pos = Vec2(x, y)

		self.color = color
		self.fillColor = fillColor

		self.rect = [0, 0, 0, 0]

		self.rotation = 0

		self.points = []


	def __str__(self):
		return "<hitbox:" + str(self.x) + ", " + str(self.y) + "| " + str(len(self.points)) + " points >"


	def addPoint(self, x, y):
		self.points.append(Vec2(self.pos.x + x, self.pos.y + y))
		self.computeSurroundingRect()


	def computeSurroundingRect(self):
		if len(self.points) == 0:
			return

		pos = self.points[0].asTuppleCenter(self.pos.x, self.pos.y)

		xLeft = pos[0]
		xRight = pos[0]
		yUp = pos[1]
		yDown = pos[1]

		for i in range (1, len(self.points)):
			pos = self.points[i].asTuppleCenter(self.pos.x, self.pos.y)

			if (pos[0] < xLeft):
				xLeft = pos[0]
			elif (pos[0] > xRight):
				xRight = pos[0]

			if (pos[1] < yUp):
				yUp = pos[1]
			elif (pos[1] > yDown):
				yDown = pos[1]

		self.rect[0] = xLeft + self.pos.x
		self.rect[2] = xRight - xLeft + 1
		self.rect[1] = yUp + self.pos.y
		self.rect[3] = yDown - yUp + 1


	def setPos(self, x, y):
		dx = x - self.pos.x
		dy = y - self.pos.y
		self.pos.x = x
		self.pos.y = y
		for i in range (len(self.points)):
			self.points[i].translate(dx, dy)
		self.computeSurroundingRect()


	def move(self, x, y):
		self.pos.add(Vec2(x, y))
		for i in range (len(self.points)):
			self.points[i].translate(x, y)
		self.computeSurroundingRect()


	def rotate(self, degrees):
		self.rotation += degrees

		radiant = degrees * (math.pi / 180)
		sinTmp = math.sin(radiant)
		cosTmp = math.cos(radiant)

		for i in range (len(self.points)):
			self.points[i].rotateAround(self.pos.x, self.pos.y, sinTmp, cosTmp)
		self.computeSurroundingRect()


	def drawNormals(self, win):
		for i in range(1, len(self.points)):
			segDir = vec2Sub(self.points[i], self.points[i - 1])
			segNorm = segDir.norm()
			segDir.divide(segNorm)
			segNormal = getNormalOfSegment(self.points[i], self.points[i - 1])

			startPoint = self.points[i - 1].dup()
			startPoint.translateAlong(segDir, segNorm / 2)

			endPoint = startPoint.dup()
			endPoint.translateAlong(segNormal, 20)

			pg.draw.line(win, self.color, startPoint.asTupple(), endPoint.asTupple(), 1)


	def draw(self, win):
		if DRAW_HITBOX:
			points = []
			for p in self.points:
				points.append(p.asTupple())

			pg.draw.polygon(win, self.color, points, 1)

		if DRAW_HITBOX_NORMALS:
			self.drawNormals(win)


	def drawFill(self, win):
		points = []
		for p in self.points:
			points.append(p.asTupple())

		pg.draw.polygon(win, self.fillColor, points)


	def isCollide(self, hitbox):
		pointsSize = len(self.points)
		if (pointsSize <= 1):
			return False

		hitboxPointsSize = len(hitbox.points)
		if (hitboxPointsSize <= 1):
			return False

		if self.rect[0] + self.rect[2] >= hitbox.rect[0] and self.rect[0] <= hitbox.rect[0] + hitbox.rect[2] and \
			self.rect[1] + self.rect[3] >= hitbox.rect[1] and self.rect[1] <= hitbox.rect[1] + hitbox.rect[3]:

			for i in range (0, pointsSize):
				p0 = self.points[i - 1]
				p1 = self.points[i]

				for j in range (0, hitboxPointsSize):
					p2 = hitbox.points[j - 1]
					p3 = hitbox.points[j]

					if collideBetweenSegments(p0, p1, p2, p3)[0]:
						return True

		return False


	def getCollideInfo(self, hitbox):
		collideInfos = []
		for i in range (0, len(self.points)):
			p0 = self.points[i - 1]
			p1 = self.points[i]

			for j in range (0,  len(hitbox.points)):
				p2 = hitbox.points[j - 1]
				p3 = hitbox.points[j]

				collideInfos.append(collideBetweenSegments(p0, p1, p2, p3))

		return collideInfos
