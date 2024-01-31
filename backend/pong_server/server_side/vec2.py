import math

class Vec2:
	def __init__(self, x, y) -> None:
		self.x = x
		self.y = y


	def __str__(self) -> str:
		return "<{x:+.2f},{y:+.2f}>".format(x=self.x, y=self.y)


	def add(self, vec) -> None:
		self.x += vec.x
		self.y += vec.y


	def subBy(self, vec) -> None:
		self.x -= vec.x
		self.y -= vec.y


	def multiply(self, nb) -> None:
		self.x *= nb
		self.y *= nb


	def divide(self, nb) -> None:
		if nb == 0:
			return
		self.x /= nb
		self.y /= nb


	def translate(self, x, y) -> None:
		self.x += x
		self.y += y


	def translateAlong(self, vec, dist) -> None:
		self.x += vec.x * dist
		self.y += vec.y * dist


	def rotateAround(self, x, y, sinTmp, cosTmp) -> None:
		# Move point to center
		self.x -= x
		self.y -= y

		# Apply rotation
		tmpX = self.x
		tmpY = self.y
		self.x = (tmpX * cosTmp) - (tmpY * sinTmp)
		self.y = (tmpX * sinTmp) + (tmpY * cosTmp)

		# Uncenter point
		self.x += x
		self.y += y


	def asTupple(self) -> tuple:
		return (self.x, self.y)


	def asTuppleCenter(self, x, y) -> tuple:
		return (self.x - x, self.y - y)


	def norm(self) -> float:
		return math.sqrt(self.x**2 + self.y**2)


	def normalize(self) -> None:
		norm = self.norm()
		if norm != 0:
			self.x /= norm
			self.y /= norm


	def rotate(self, angle) -> None:
		while angle < 0:
			angle += 360
		while angle > 359:
			angle -= 360

		rad = angle * (math.pi / 180)
		cosRad = math.cos(rad)
		sinRad = math.sin(rad)

		self.x = self.x * cosRad - self.y * sinRad
		self.y = self.x * sinRad + self.y * cosRad

		self.normalize()


	def dup(self):
		return Vec2(self.x, self.y)



def vec2Add(vec1, vec2) -> Vec2:
	return Vec2(vec1.x + vec2.x, vec1.y + vec2.y)


def vec2Sub(vec1, vec2) -> Vec2:
	return Vec2(vec1.x - vec2.x, vec1.y - vec2.y)


def vec2Dot(vec1, vec2) -> int:
	return (vec1.x * vec2.x) + (vec1.y * vec2.y)


def vec2Cross(vec1, vec2) -> int:
	return (vec1.x * vec2.y) - (vec1.y * vec2.x)


def getNormalOfSegment(vec1, vec2) -> Vec2:
	dx = vec2.x - vec1.x
	dy = vec2.y - vec1.y
	vec = Vec2(-dy, dx)
	vec.normalize()
	return vec


def reflectionAlongVec2(normal:Vec2, vec:Vec2) -> Vec2:
	if (vec2Dot(normal, vec) >= 0):
		normal.multiply(-1)

	divider = vec2Dot(vec, vec)
	if (divider == 0):
		return (vec)
	vecProjOnNormal = normal.dup()
	vecProjOnNormal.multiply(vec2Dot(normal, vec) / divider)

	vecProjOnNormal.multiply(2)
	reflectedVec = vec2Sub(vec, vecProjOnNormal)

	reflectedVec.normalize()

	return reflectedVec
