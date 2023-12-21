// import math

export class Vec2 {
	constructor ( x, y)
	{
		this.x = x
		this.y = y
	}


	print()
	{
		console.log("<{" + this.x + ":+.2f},{" + this.y + ":+.2f}>");
	}


	add( vec){
		this.x += vec.x
		this.y += vec.y
	}


	subBy( vec){
		this.x -= vec.x
		this.y -= vec.y
	}


	multiply( nb){
		this.x *= nb
		this.y *= nb
	}


	divide( nb){
		if (nb == 0)
			return
		this.x /= nb
		this.y /= nb
	}


	translate( x, y)
	{
		this.x += x
		this.y += y
	}


	translateAlong( vec, dist)
	{
		this.x += vec.x * dist
		this.y += vec.y * dist
	}


	rotateAround( x, y, sinTmp, cosTmp)
	{
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
	}


	asTupple()
	{
		return (this.x, this.y)
	}


	asTuppleCenter( x, y)
	{
		return (this.x - x, this.y - y)
	}


	norm()
	{
		return math.sqrt(this.x**2 + this.y**2)
	}


	normalize()
	{
		norm = this.norm()
		if (norm != 0){
			this.x /= norm
			this.y /= norm
		}
	}


	rotate( angle)
	{
		while (angle < 0)
			angle += 360
		while (angle > 359)
			angle -= 360

		rad = angle * (math.pi / 180)
		cosRad = math.cos(rad)
		sinRad = math.sin(rad)

		this.x = this.x * cosRad - this.y * sinRad
		this.y = this.x * sinRad + this.y * cosRad

		this.normalize()
	}


	dup()
	{
		return new Vec2(this.x, this.y)
	}

}

function vec2Add(vec1, vec2)
{
	return new Vec2(vec1.x + vec2.x, vec1.y + vec2.y)
}


function vec2Sub(vec1, vec2)
{
	return new Vec2(vec1.x - vec2.x, vec1.y - vec2.y)
}


function vec2Dot(vec1, vec2)
{
	return (vec1.x * vec2.x) + (vec1.y * vec2.y)
}


function vec2Cross(vec1, vec2)
{
	return (vec1.x * vec2.y) - (vec1.y * vec2.x)
}


function getNormalOfSegment(vec1, vec2)
{
	dx = vec2.x - vec1.x
	dy = vec2.y - vec1.y
	vec = Vec2(-dy, dx)
	vec.normalize()
	return vec
}

function reflectionAlongVec2(normal, vec)
{
	if (vec2Dot(normal, vec) >= 0)
		normal.multiply(-1)

	divider = vec2Dot(vec, vec)
	if (divider == 0)
		return (vec)
	vecProjOnNormal = normal.dup()
	vecProjOnNormal.multiply(vec2Dot(normal, vec) / divider)

	vecProjOnNormal.multiply(2)
	reflectedVec = vec2Sub(vec, vecProjOnNormal)

	reflectedVec.normalize()

	return reflectedVec
}

