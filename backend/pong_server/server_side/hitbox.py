from define import *
from server_side.vec2 import *

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
	s1Dir = vec2Sub(p2, p1)
	p = p1.dup()
	p.translateAlong(s1Dir, t)

	return True, p1, p2, p


class Hitbox:
	def __init__(self, x, y, color):
		self.pos = Vec2(x, y)

		self.rect = [0, 0, 0, 0]

		self.rotation = 0

		self.points = []

		self.color = color


	def __str__(self):
		return "<hitbox:" + str(self.pos.x) + ", " + str(self.pos.y) + "| " + str(len(self.points)) + " points >"


	def addPoint(self, x, y):
		self.points.append(Vec2(self.pos.x + x, self.pos.y + y))
		self.computeSurroundingRect()


	def addPoints(self, lst:list[tuple[int, int]]):
		for x, y in lst:
			self.points.append(Vec2(self.pos.x + x, self.pos.y + y))
			self.computeSurroundingRect()


	def clearPoints(self):
		self.points.clear()


	def getPoints(self) -> list[tuple[int, int]]:
		points = []

		for p in self.points:
			points.append(p.asTupple())

		return points


	def getPointsCenter(self) -> list[tuple[int, int]]:
		points = []

		for p in self.points:
			points.append(p.asTuppleCenter(self.pos.x, self.pos.y))

		return points


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


	def setPos(self, vec):
		dx = vec.x - self.pos.x
		dy = vec.y - self.pos.y
		self.pos = vec
		for i in range (len(self.points)):
			self.points[i].translate(dx, dy)
		self.computeSurroundingRect()


	def move(self, x, y):
		self.pos.add(Vec2(x, y))
		for i in range (len(self.points)):
			self.points[i].translate(x, y)
		self.computeSurroundingRect()


	def rotate(self, degrees):
		if degrees == 0:
			return

		self.rotation += degrees

		radiant = degrees * (math.pi / 180)
		sinTmp = math.sin(radiant)
		cosTmp = math.cos(radiant)

		for i in range (len(self.points)):
			self.points[i].rotateAround(self.pos.x, self.pos.y, sinTmp, cosTmp)
		self.computeSurroundingRect()


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


	def isInside(self, hitbox):
		pointsSize = len(self.points)
		if (pointsSize <= 1):
			return False

		hitboxPointsSize = len(hitbox.points)
		if (hitboxPointsSize <= 1):
			return False

		if self.rect[0] + self.rect[2] >= hitbox.rect[0] and self.rect[0] <= hitbox.rect[0] + hitbox.rect[2] and \
			self.rect[1] + self.rect[3] >= hitbox.rect[1] and self.rect[1] <= hitbox.rect[1] + hitbox.rect[3]:


			for i in range (0, pointsSize):
				p = self.points[i]
				pLeft = Vec2(p.x - 1000, p.y)
				pRight = Vec2(p.x + 1000, p.y)

				nbCollideLeft = 0
				nbCollideRight = 0
				for j in range (0, hitboxPointsSize):
					p2 = hitbox.points[j - 1]
					p3 = hitbox.points[j]

					if collideBetweenSegments(p, pLeft, p2, p3)[0]:
						nbCollideLeft += 1
					if collideBetweenSegments(p, pRight, p2, p3)[0]:
						nbCollideRight += 1

				if nbCollideLeft > 0 and nbCollideRight > 0 and (nbCollideLeft % 2 == 1 or nbCollideRight % 2 == 1):
					return True
		return False


	def isInsideSurrondingBox(self, hitbox):
		pointsSize = len(self.points)
		if (pointsSize <= 1):
			return False

		hitboxPointsSize = len(hitbox.points)
		if (hitboxPointsSize <= 1):
			return False

		if self.rect[0] + self.rect[2] >= hitbox.rect[0] and self.rect[0] <= hitbox.rect[0] + hitbox.rect[2] and \
			self.rect[1] + self.rect[3] >= hitbox.rect[1] and self.rect[1] <= hitbox.rect[1] + hitbox.rect[3]:
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


	def copy(self):
		copy = Hitbox(self.pos.x, self.pos.y, self.color)

		points = []
		for p in self.points:
			points.append(p.dup())
		copy.addPoints(points)

		copy.rotation = self.rotation

		return copy
