############################################################################################
#                                       BALL DEFINE                                        #
############################################################################################
BALL_RADIUS = 10 # in pixel
BALL_START_SPEED = 480 # pixel per seconds
BALL_MIN_SPEED = 240 # pixel per seconds
BALL_MAX_SPEED = 1920 # pixel per seconds
BALL_PADDLE_ACCELERATION = 100 # pixel per seconds
BALL_WALL_ACCELERATION = 10 # pixel per seconds
BALL_HITBOX_PRECISION = 16 # nb number for make circle [4, 360]
BALL_MOVE_STEP = 2 # Number of pixel travel by ball between 2 collisions check
BALL_MOVE_STEP = BALL_RADIUS # Number of pixel travel by ball between 2 collisions check

BALL_FRICTION = False # boolean
BALL_MINIMUM_FRICTION = 100 # pixel per seconds
BALL_FRICTION_STRENGTH = 0.2 # float [0, 1]

# Ball state defines
STATE_RUN = 0
STATE_IN_GOAL_LEFT = 1
STATE_IN_GOAL_RIGHT = 2
STATE_IN_FOLLOW = 3


############################################################################################
#                                        MAP DEFINE                                        #
############################################################################################
AREA_SIZE = (1800, 900)
AREA_BORDER_SIZE = 10 # in pixel
SPACE_PART = AREA_SIZE[0] // 5
LEFT_TEAM_RECT = (0, 0, SPACE_PART, AREA_SIZE[1])
MIDDLE_RECT = (SPACE_PART, 0, AREA_SIZE[0] - SPACE_PART, AREA_SIZE[1])
RIGTH_TEAM_RECT = (AREA_SIZE[0] - SPACE_PART, 0, SPACE_PART, AREA_SIZE[1])

PERFECT_SHOOT_SIZE = BALL_RADIUS * 4 # in pixel

OBSTACLE_ROUTINE_TYPE_TRANSLATION = 0
OBSTACLE_ROUTINE_TYPE_ROTATION = 1
OBSTACLE_ROUTINE_TIME_INFINITE = -1

# {obstacle_type, obstacle_position, obstacle_color, obstacle_info, obstacle_routine}
OBSTACLE_TYPE_RECTANGLE = 0
OBSTACLE_TYPE_POLYGON = 1
OBSTACLE_TYPE_CIRCLE = 2
# obstacle_info RECTANGLE : [w, h]
# obstacle_info POLYGON : [(x, y), (x, y), ...]
# obstacle_info CIRCLE : [radius, precision]

IA_COOLDOWN_GET_GAME_STATE = 1 # In seconds

############################################################################################
#                                        TEAM DEFINE                                       #
############################################################################################
TEAM_MAX_PLAYER = 2
TEAM_WIN_SCORE = 1
TEAM_LEFT = 0
TEAM_RIGHT = 1

PADDLE_PLAYER = 0
PADDLE_IA = 1

############################################################################################
#                                       PADDLE DEFINE                                      #
############################################################################################
PADDLE_WIDTH = 14 # in pixel
PADDLE_HEIGHT = 140 # in pixel
PADDLE_SPEED = 800 # pixel per seconds
PADDLE_LAUNCH_COOLDOWN = 0.2 # In second

PADDLES_KEYS_STATE = [
	False, False, False, False, # Left Player 1
	False, False, False, False, # Left Player 2
	False, False, False, False, # Right Player 1
	False, False, False, False, # Right Player 2
]

# Key index defines
KEY_UP = 0
KEY_DOWN = 1
KEY_POWER_UP = 2
KEY_LAUNCH_BALL = 3


############################################################################################
#                                       POWER UP DEFINE                                    #
############################################################################################
# Power up object state
POWER_UP_HITBOX_RADIUS = 24 # in pixel
POWER_UP_HITBOX_PRECISION = 8 # number of point to make the circle hitbox
POWER_UP_VISIBLE = 0
POWER_UP_TAKE = -1
POWER_UP_SPAWN_COOLDOWN = 5 # in seconds
POWER_UP_USE_COOLDOWN = 0.5 # in seconds

# Power up list and effects define
POWER_UP_NONE = -1

POWER_UP_BALL_FAST = 0 # begin by hit paddle - 1 ball - end by hit wall
POWER_UP_BALL_FAST_FACTOR = 2.5 # multiply the speed
POWER_UP_BALL_FAST_TIME_STOP = 1 # in seconds

POWER_UP_BALL_WAVE = 1 # begin by hit paddle - 1 ball - end by hit wall
POWER_UP_BALL_WAVE_DEGREES = 45 # in degrees [0, 359]
POWER_UP_BALL_WAVE_SPEED_FACTOR = 20 # change the frequence of the wave. High = more but smaller waves

POWER_UP_BALL_INVISIBLE = 2 # begin by hit paddle - 1 ball - end by hit wall
POWER_UP_BALL_INVISIBLE_SPEED_FACTOR = 5 # in seconds

POWER_UP_BALL_NO_COLLISION = 3 # begin when ball isn't close of ennemy - all ball - end by hit paddle

POWER_UP_DUPLICATION_BALL = 4 # begin when ball isn't close of ennemy - all ball - never end
POWER_UP_DUPLICATION_BALL_SPEED_REDUCE_FACTOR = 2 # divise the speed
POWER_UP_DUPLICATION_BALL_DEGREES_DEVIATON = 30

POWER_UP_BALL_SLOW = 5 # any time - all ball - limited time effect
POWER_UP_BALL_SLOW_SPEED_FACTOR = 2 # divide the speed
POWER_UP_BALL_SLOW_TIME_EFFECT = 5 # in seconds

POWER_UP_BALL_STOP = 6 # any time - all ball - limited time effect
POWER_UP_BALL_STOP_TIMER_EFFECT = 3 # in seconds

POWER_UP_BALL_BIG = 7 # any time - all ball - limited time effect
POWER_UP_BALL_BIG_SIZE_FACTOR = 2 # multiply the size
POWER_UP_BALL_BIG_TIME_EFFECT = 10 # in seconds

POWER_UP_BALL_LITTLE = 8 # any time - all ball - limited time effect
POWER_UP_BALL_LITTLE_SIZE_FACTOR = 2 # divide the size
POWER_UP_BALL_LITTLE_TIME_EFFECT = 10 # in seconds

POWER_UP_PADDLE_FAST = 9 # any time - all team paddle - limited time effect
POWER_UP_PADDLE_FAST_SPEED_FACTOR = 2 # multiply the speed
POWER_UP_PADDLE_FAST_TIME_EFFECT = 10 # in seconds

POWER_UP_PADDLE_SLOW = 10 # any time - all ennemy team paddle - limited time effect
POWER_UP_PADDLE_SLOW_SPEED_FACTOR = 2 # divide the speed
POWER_UP_PADDLE_SLOW_TIME_EFFECT = 10 # in seconds

POWER_UP_PADDLE_BIG = 11 # any time - all team paddle - limited time effect
POWER_UP_PADDLE_BIG_SIZE_FACTOR = 2 # multiply the size
POWER_UP_PADDLE_BIG_TIME_EFFECT = 10 # in seconds

POWER_UP_PADDLE_LITTLE = 12 # any time - all ennemy team paddle - limited time effect
POWER_UP_PADDLE_LITTLE_SIZE_FACTOR = 2 # divide the size
POWER_UP_PADDLE_LITTLE_TIME_EFFECT = 10 # in seconds


############################################################################################
#                                    COMMUNICATION DEFINE                                  #
############################################################################################
TIME_SEND_UPDATE_INFO_TO_CLIENT = 0.01 # in seconds

#====================#
# MESSAGE DEFINITION #
#====================#
# [<message type>, <message content>]


#==================#
# CLIENT TO SERVER #
#==================#
CLIENT_MSG_TYPE_USER_EVENT = 0
# Content of user event :
# {id_paddle, id_key, key_action [True = press, False = release]}


#==================#
# SERVER TO CLIENT #
#==================#
SERVER_MSG_TYPE_CREATE_START_INFO = -1
# Content of obstacles :
# {
# 	obstables : [ {position:[x, y], points:[[x, y]], color:(r, g, b)} ]
# 	powerUp : True or False
# }

SERVER_MSG_TYPE_UPDATE_OBSTACLE = 0
# Content of obstacles :
# [
# 	{id, position, points:[[x, y]]}
# ]

SERVER_MSG_TYPE_UPDATE_PADDLES = 1
# Content of paddles :
# [
# 	{id_paddle, id_team, position:[x, y], modifierSize, powerUp, powerUpInCharge}
# ]

SERVER_MSG_TYPE_UPDATE_BALLS = 2
# Content of balls :
# [
# 	{position:[x, y], direction:[x, y], speed, radius, state, last_paddle_hit_info:[id, team], modifier_state}
# ]

SERVER_MSG_TYPE_DELETE_BALLS = 3
# Content of delete balls :
# [id_ball]

SERVER_MSG_TYPE_UPDATE_POWER_UP = 4
# Content of power up :
# {position:[x, y], state}

SERVER_MSG_TYPE_SCORE_UPDATE = 5
# Content of score :
# {leftTeam, rightTeam}
