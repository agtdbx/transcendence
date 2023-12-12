// import math

class Vec2 {
	def constructor ( x, y) -> None:
		this.x = x
		this.y = y


	def __str__(this) -> str:
		return "<{x:+.2f},{y:+.2f}>".format(x=this.x, y=this.y)


	def add( vec) -> None:
		this.x += vec.x
		this.y += vec.y


	def subBy( vec) -> None:
		this.x -= vec.x
		this.y -= vec.y


	def multiply( nb) -> None:
		this.x *= nb
		this.y *= nb


	def divide( nb) -> None:
		if nb == 0:
			return
		this.x /= nb
		this.y /= nb


	def translate( x, y) -> None:
		this.x += x
		this.y += y


	def translateAlong( vec, dist) -> None:
		this.x += vec.x * dist
		this.y += vec.y * dist


	def rotateAround( x, y, sinTmp, cosTmp) -> None:
		// Move point to center
		this.x -= x
		this.y -= y

		// Apply rotation
		tmpX = this.x
		tmpY = this.y
		this.x = (tmpX * cosTmp) - (tmpY * sinTmp)
		this.y = (tmpX * sinTmp) + (tmpY * cosTmp)

		// Uncenter point
		this.x += x
		this.y += y


	def asTupple(this) -> tuple:
		return (this.x, this.y)


	def asTuppleCenter( x, y) -> tuple:
		return (this.x - x, this.y - y)


	def norm(this) -> float:
		return math.sqrt(this.x**2 + this.y**2)


	def normalize(this) -> None:
		norm = this.norm()
		if norm != 0:
			this.x /= norm
			this.y /= norm


	def rotate( angle) -> None:
		while angle < 0:
			angle += 360
		while angle > 359:
			angle -= 360

		rad = angle * (math.pi / 180)
		cosRad = math.cos(rad)
		sinRad = math.sin(rad)

		this.x = this.x * cosRad - this.y * sinRad
		this.y = this.x * sinRad + this.y * cosRad

		this.normalize()


	def dup(this):
		return Vec2(this.x, this.y)



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

}