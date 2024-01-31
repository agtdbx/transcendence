from define import *

import server_side.paddle as paddle
import random

class Team:
	def __init__(self, numberOfPlayers:int, team:int) -> None:
		if numberOfPlayers < 1:
			numberOfPlayers = 1
		elif numberOfPlayers > TEAM_MAX_PLAYER:
			numberOfPlayers = TEAM_MAX_PLAYER

		self.team = team

		if self.team == TEAM_LEFT:
			xPos = AREA_BORDER_SIZE * 2
		else:
			xPos = AREA_SIZE[0] - AREA_BORDER_SIZE * 2

		self.paddles = []
		if numberOfPlayers == 1:
			self.paddles.append(paddle.Paddle(xPos, AREA_SIZE[1] // 2 + random.randint(-50, 50), 0, self.team))
		else:
			self.paddles.append(paddle.Paddle(xPos, AREA_SIZE[1] // 3 + random.randint(-50, 50), 0, self.team))
			self.paddles.append(paddle.Paddle(xPos, AREA_SIZE[1] // 3 * 2 + random.randint(-50, 50), 1, self.team))

		self.score = 0
		# list of power up who try to use : [power up id, paddle id, power up used (bool)]
		self.powerUpTryUse = []


	def tick(self, delta:float, paddlesKeyState:list, updateTime:bool) -> None:
		# Check power up try to used
		for powerUp in self.powerUpTryUse:
			# if a power up is user, remove it to the player
			if powerUp[2]:
				if powerUp[0] == POWER_UP_BALL_FAST:
					self.paddles[powerUp[1]].powerUpInCharge.append(POWER_UP_BALL_FAST)
				elif powerUp[0] == POWER_UP_BALL_WAVE:
					self.paddles[powerUp[1]].powerUpInCharge.append(POWER_UP_BALL_WAVE)
				elif powerUp[0] == POWER_UP_BALL_INVISIBLE and self.paddles[powerUp[1]].waitUsePowerUp == 0:
					self.paddles[powerUp[1]].powerUpInCharge.append(POWER_UP_BALL_INVISIBLE)

				self.paddles[powerUp[1]].waitUsePowerUp = POWER_UP_USE_COOLDOWN
				self.paddles[powerUp[1]].powerUp = POWER_UP_NONE

		self.powerUpTryUse.clear()


		# Check input
		for i in range(len(self.paddles)):
			if updateTime:
				self.paddles[i].updateTimes(delta)

			keyId = i
			if self.team == TEAM_RIGHT:
				keyId += TEAM_MAX_PLAYER

			if paddlesKeyState[keyId * 4 + KEY_UP]:
				self.paddles[i].move("up", delta)
			if paddlesKeyState[keyId * 4 + KEY_DOWN]:
				self.paddles[i].move("down", delta)
			if paddlesKeyState[keyId * 4 + KEY_POWER_UP]:
				powerUp = self.paddles[i].powerUp
				if powerUp != POWER_UP_NONE:
					self.powerUpTryUse.append([powerUp, i, False])


	def applyPowerUpToPaddles(self, powerUp):
		for p in self.paddles:
			p.addPowerUpEffect(powerUp)
