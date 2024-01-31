from define import *
from server_side.vec2 import *

import server_side.hitbox as hitbox
import server_side.ball as ball

class Obstacle:
	def __init__(self, x:int, y:int, color:tuple[int, int, int]=(200, 200, 200)) -> None:
		self.hitbox = hitbox.Hitbox(x, y, color)
		# [
		# 	{type, time, effect}
		# ]
		# effect can be degrees for rotation, vec2 for translation, or None for wait
		self.routine = []
		self.routineIndex = 0
		self.routineTime = 0
		self.numberOfRoutines = len(self.routine)


	def createWallHitbox(self, w:int, h:int) -> None:
		halfW = w / 2
		halfH = h / 2
		self.hitbox.addPoint(-halfW, -halfH)
		self.hitbox.addPoint(halfW, -halfH)
		self.hitbox.addPoint(halfW, halfH)
		self.hitbox.addPoint(-halfW, halfH)


	def createPolygonHitbox(self, points:list[tuple[int, int]]) -> None:
		self.hitbox.addPoints(points)


	def createCircleHitbox(self, radius:int, precision:int) -> None:
		self.hitbox.addPoints(ball.getPointOfCircle(radius, precision))


	def addRoutine(self, routine:list[int, int, int | Vec2 | None]=[]) -> None:
		# [
		# 	{type, time, effect}
		# ]
		# effect can be degrees for rotation, vec2 for translation, or None for wait
		self.routine = routine
		self.numberOfRoutines = len(self.routine)


	def updateRoutine(self, delta:float):
		# check in there is a routine
		if self.numberOfRoutines == 0:
			return

		# update time
		self.routineTime += delta

		# get current routine
		currentRoutine = self.routine[self.routineIndex]

		# if time pass, change to next routine
		if currentRoutine["time"] != OBSTACLE_ROUTINE_TIME_INFINITE and self.routineTime >= currentRoutine["time"]:
			self.routineTime = 0
			self.routineIndex += 1
			if self.routineIndex >= self.numberOfRoutines:
				self.routineIndex = 0
			currentRoutine = self.routine[self.routineIndex]

		# do translation
		if currentRoutine["type"] == OBSTACLE_ROUTINE_TYPE_TRANSLATION:
			vec = currentRoutine["effect"].dup()
			vec.multiply(delta)
			self.hitbox.move(vec.x, vec.y)
		# do rotation
		elif currentRoutine["type"] == OBSTACLE_ROUTINE_TYPE_ROTATION:
			self.hitbox.rotate(currentRoutine["effect"] * delta)


	def copy(self):
		copy = Obstacle(self.hitbox.pos.x, self.hitbox.pos.y, self.hitbox.color)
		copy.hitbox.addPoints(self.hitbox.getPointsCenter())

		copy.routine = self.routine.copy()
		copy.routineIndex = self.routineIndex
		copy.routineTime = self.routineTime
		copy.numberOfRoutines = self.numberOfRoutines

		return copy
