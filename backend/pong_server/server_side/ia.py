from define import *
from server_side.vec2 import *
import server_side.obstacle as obstacle
import server_side.paddle as paddle
import server_side.team as team
import server_side.ball as ball

########################################################
#                        DEFINE                        #
########################################################
IA_STATE_WAIT = 0
IA_STATE_GO_TO_Y_POS = 1

IA_POSITION_PRECISION = 1 # In pixels
IA_EMULATE_MAX_TIME = 5 # In seconds

########################################################
#                         CLASS                        #
########################################################
class Ia:
	def __init__(self, teamId:int, paddleId:int):
		self.teamId = teamId
		self.paddleId = paddleId
		self.globalId = paddleId
		if self.teamId == TEAM_RIGHT:
			self.globalId += TEAM_MAX_PLAYER

		# Copy of game environement
		self.paddles = []
		self.walls = []
		self.balls = []
		# {state, hitbox, paddleWhoGet:[id, team]}
		self.powerUp = {"state" : None, "hitbox" : None, "paddleWhoGet" : None}

		# [Up, Down, Power Up, Launch ball]
		self.iaPaddle = None
		self.keyToEmulate = [False, False, False, False]
		self.state = IA_STATE_WAIT
		self.stateInfo = None


	def updateGameEnvironement(self,
							walls:list[obstacle.Obstacle],
							paddlesLeft:list[paddle.Paddle],
							paddlesRight:list[paddle.Paddle],
							balls:list[ball.Ball],
							powerUp:dict):
		# Copy the game environement
		self.copyGameEnvironement(walls, paddlesLeft, paddlesRight, balls, powerUp)

		# Determine the paddle of the ia
		if self.teamId == TEAM_LEFT:
			self.iaPaddle = self.paddles[self.paddleId]
		else:
			self.iaPaddle = self.paddles[self.paddleId + len(paddlesLeft)]

		if self.balls[0].state == STATE_IN_FOLLOW:
			self.balls[0].state == STATE_RUN

		tmpPaddle = self.iaPaddle.copy()

		# Simulate the game until one ball is in goal
		self.emulateBallsToGoal()

		# Choose where ia should be placed, and it action to do
		self.chooseNextActionToDo()

		self.iaPaddle = tmpPaddle


	def tick(self, delta:float):
		"""
		Tick method of the Ia.
		In this method, the Ia will emulate the game to know what to do.
		To make is plan, the Ia will change paddleKeyState to move paddle according to it's plan
		"""
		# Ia movement
		if self.state == IA_STATE_GO_TO_Y_POS and self.stateInfo != None:
			if abs(self.iaPaddle.pos.y - self.stateInfo) <= IA_POSITION_PRECISION:
				self.state = IA_STATE_WAIT
				self.keyToEmulate[KEY_UP] = False
				self.keyToEmulate[KEY_DOWN] = False
				self.stateInfo = None
			elif self.iaPaddle.pos.y > self.stateInfo:
				self.keyToEmulate[KEY_UP] = True
				self.keyToEmulate[KEY_DOWN] = False
				self.iaPaddle.move("up", delta)
			elif self.iaPaddle.pos.y < self.stateInfo:
				self.keyToEmulate[KEY_DOWN] = True
				self.keyToEmulate[KEY_UP] = False
				self.iaPaddle.move("down", delta)
			else:
				self.state = IA_STATE_WAIT
				self.keyToEmulate[KEY_UP] = False
				self.keyToEmulate[KEY_DOWN] = False
				self.stateInfo = None
		else:
			self.keyToEmulate[KEY_UP] = False
			self.keyToEmulate[KEY_DOWN] = False

		# Ia use power up when it possible
		if self.iaPaddle.powerUp != POWER_UP_NONE:
			self.keyToEmulate[KEY_POWER_UP] = True
		else:
			self.keyToEmulate[KEY_POWER_UP] = False

		# Ia launch ball when it's possible
		if self.balls[0].state == STATE_IN_FOLLOW and self.balls[0].lastPaddleHitId == self.paddleId and self.balls[0].lastPaddleTeam == self.teamId:
			self.keyToEmulate[KEY_LAUNCH_BALL] = True
		else:
			self.keyToEmulate[KEY_LAUNCH_BALL] = False


	def copyGameEnvironement(self,
							walls:list[obstacle.Obstacle],
							paddlesLeft:list[paddle.Paddle],
							paddlesRight:list[paddle.Paddle],
							balls:list[ball.Ball],
							powerUp:dict):
		self.walls.clear()
		for w in walls:
			self.walls.append(w.copy())

		self.paddles.clear()
		for p in paddlesLeft:
			self.paddles.append(p.copy())
		for p in paddlesRight:
			self.paddles.append(p.copy())

		self.balls.clear()
		for b in balls:
			self.balls.append(b.copy())

		self.powerUp["state"] = powerUp["state"]
		self.powerUp["hitbox"] = powerUp["hitbox"]
		self.powerUp["paddleWhoGet"] = powerUp["paddleWhoGet"]


	def emulateBallsToGoal(self):
		delta = 0.015 # ~ 60 fps

		simulateTimeLimit = IA_EMULATE_MAX_TIME

		stopSimulateIfLastPaddleTouchIsIaOne = []
		for i in range(len(self.balls)):
			b = self.balls[i]
			if b.lastPaddleHitId == self.paddleId and b.lastPaddleTeam == self.teamId:
				stopSimulateIfLastPaddleTouchIsIaOne.append(False)
			else:
				stopSimulateIfLastPaddleTouchIsIaOne.append(True)

		self.emulateState = self.state
		self.emulateStateInfo = self.stateInfo

		while simulateTimeLimit > 0:
			# Update walls routine
			for w in self.walls:
				w.updateRoutine(delta)

			for p in self.paddles:
				p.updateTimes(delta)

			self.emulateTick(delta)

			for i in range(len(self.balls)):
				b = self.balls[i]
				b.updatePosition(delta, self.paddles, [], self.walls, self.powerUp)
				b.updateTime(delta)

				if not stopSimulateIfLastPaddleTouchIsIaOne[i] and (b.lastPaddleHitId != self.paddleId or b.lastPaddleTeam != self.teamId):
					stopSimulateIfLastPaddleTouchIsIaOne[i] = True
				elif stopSimulateIfLastPaddleTouchIsIaOne[i] and b.lastPaddleHitId == self.paddleId and b.lastPaddleTeam == self.teamId:
					break

				if b.state == STATE_IN_GOAL_LEFT:
					if self.teamId == TEAM_LEFT:
						self.stateInfo = b.pos.y
					break
				if b.state == STATE_IN_GOAL_RIGHT:
					if self.teamId == TEAM_RIGHT:
						self.stateInfo = b.pos.y
					break

			simulateTimeLimit -= delta


	def emulateTick(self, delta:float):
		"""
		Tick method of the Ia.
		In this method, the Ia will emulate the game to know what to do.
		To make is plan, the Ia will change paddleKeyState to move paddle according to it's plan
		"""
		# Ia movement
		if self.emulateState == IA_STATE_GO_TO_Y_POS:
			if abs(self.iaPaddle.pos.y - self.emulateStateInfo) <= IA_POSITION_PRECISION:
				self.emulateState = IA_STATE_WAIT
				self.emulateStateInfo = None
			elif self.iaPaddle.pos.y > self.emulateStateInfo:
				self.iaPaddle.move("up", delta)
			elif self.iaPaddle.pos.y < self.emulateStateInfo:
				self.iaPaddle.move("down", delta)
			else:
				self.emulateState = IA_STATE_WAIT
				self.emulateStateInfo = None


	def chooseNextActionToDo(self):
		if self.stateInfo != None:
			self.state = IA_STATE_GO_TO_Y_POS
