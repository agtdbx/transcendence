from define import *
from server_side.tcp_server import runGameServer


map_to_load = 2
paddles_left = [PADDLE_PLAYER]
paddles_right = [PADDLE_IA]
powerUpEnable=True

runGameServer(map_to_load=map_to_load, paddles_left=paddles_left, paddles_right=paddles_right, powerUpEnable=powerUpEnable)
