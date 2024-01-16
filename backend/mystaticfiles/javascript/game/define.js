////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                       BALL DEFINE                                        //
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
export const BALL_RADIUS = 10 // in pixel
export const BALL_START_SPEED = 480 // pixel per seconds 
export const BALL_MIN_SPEED = 240 // pixel per seconds
export const BALL_MAX_SPEED = 1920 // pixel per seconds
export const BALL_PADDLE_ACCELERATION = 100 // pixel per seconds
export const BALL_WALL_ACCELERATION = 10 // pixel per seconds
export const BALL_HITBOX_PRECISION = 16 // nb number for make circle [4, 360]
export const BALL_MOVE_STEP = BALL_RADIUS // Number of pixel travel by ball between 2 collisions check

export const BALL_FRICTION = false // boolean
export const BALL_MINIMUM_FRICTION = 100 // pixel per seconds
export const BALL_FRICTION_STRENGTH = 0.2 // float [0, 1]

// Ball state defines
export const STATE_RUN = 0
export const STATE_IN_GOAL_LEFT = 1
export const STATE_IN_GOAL_RIGHT = 2
export const STATE_IN_FOLLOW = 3


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                        MAP DEFINE                                        //
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
export const AREA_SIZE = [1800, 900]
export const AREA_BORDER_SIZE = 10 // in pixel
export const SPACE_PART = AREA_SIZE[0] // 5
export const LEFT_TEAM_RECT = (0, 0, SPACE_PART, AREA_SIZE[1])
export const MIDDLE_RECT = (SPACE_PART, 0, AREA_SIZE[0] - SPACE_PART, AREA_SIZE[1])
export const RIGTH_TEAM_RECT = (AREA_SIZE[0] - SPACE_PART, 0, SPACE_PART, AREA_SIZE[1])

export const PERFECT_SHOOT_SIZE = BALL_RADIUS * 4 // in pixel

export const OBSTACLE_ROUTINE_TYPE_TRANSLATION = 0
export const OBSTACLE_ROUTINE_TYPE_ROTATION = 1
export const OBSTACLE_ROUTINE_TIME_INFINITE = -1

// {obstacle_type, obstacle_position, obstacle_color, obstacle_info, obstacle_routine}
export const OBSTACLE_TYPE_RECTANGLE = 0
export const OBSTACLE_TYPE_POLYGON = 1
export const OBSTACLE_TYPE_CIRCLE = 2
// obstacle_info RECTANGLE : [w, h]
// obstacle_info POLYGON : [(x, y), (x, y), ...]
// obstacle_info CIRCLE : [radius, precision]

export const IA_COOLDOWN_GET_GAME_STATE = 1 // In seconds

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                        TEAM DEFINE                                       //
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
export const TEAM_MAX_PLAYER = 2
export const TEAM_WIN_SCORE = 11
export const TEAM_LEFT = 0
export const TEAM_RIGHT = 1

export const PADDLE_PLAYER = 0
export const PADDLE_IA = 1

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                       PADDLE DEFINE                                      //
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
export const PADDLE_WIDTH = 14 // in pixel
export const PADDLE_HEIGHT = 140 // in pixel
export const PADDLE_SPEED = 800 // pixel per seconds
export const PADDLE_LAUNCH_COOLDOWN = 0.2 // In second

export const PADDLES_KEYS_STATE = [
	false, false, false, false, // Left Player 1
	false, false, false, false, // Left Player 2
	false, false, false, false, // Right Player 1
	false, false, false, false, // Right Player 2
]

// Key index defines
export const KEY_UP = 0
export const KEY_DOWN = 1
export const KEY_POWER_UP = 2
export const KEY_LAUNCH_BALL = 3


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                       POWER UP DEFINE                                    //
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Power up object state
export const POWER_UP_HITBOX_RADIUS = 24 // in pixel
export const POWER_UP_HITBOX_PRECISION = 8 // number of point to make the circle hitbox
export const POWER_UP_VISIBLE = 0
export const POWER_UP_TAKE = -1
export const POWER_UP_SPAWN_COOLDOWN = 5 // in seconds
export const POWER_UP_USE_COOLDOWN = 0.5 // in seconds

// Power up list and effects define
export const POWER_UP_NONE = -1

export const POWER_UP_BALL_FAST = 0 // begin by hit paddle - 1 ball - end by hit wall
export const POWER_UP_BALL_FAST_FACTOR = 2.5 // multiply the speed
export const POWER_UP_BALL_FAST_TIME_STOP = 1 // in seconds

export const POWER_UP_BALL_WAVE = 1 // begin by hit paddle - 1 ball - end by hit wall
export const POWER_UP_BALL_WAVE_DEGREES = 45 // in degrees [0, 359]
export const POWER_UP_BALL_WAVE_SPEED_FACTOR = 20 // change the frequence of the wave. High = more but smaller waves

export const POWER_UP_BALL_INVISIBLE = 2 // begin by hit paddle - 1 ball - end by hit wall
export const POWER_UP_BALL_INVISIBLE_SPEED_FACTOR = 5 // in seconds

export const POWER_UP_BALL_NO_COLLISION = 3 // begin when ball isn't close of ennemy - all ball - end by hit paddle

export const POWER_UP_DUPLICATION_BALL = 4 // begin when ball isn't close of ennemy - all ball - never end
export const POWER_UP_DUPLICATION_BALL_SPEED_REDUCE_FACTOR = 2 // divise the speed
export const POWER_UP_DUPLICATION_BALL_DEGREES_DEVIATON = 30

export const POWER_UP_BALL_SLOW = 5 // any time - all ball - limited time effect
export const POWER_UP_BALL_SLOW_SPEED_FACTOR = 2 // divide the speed
export const POWER_UP_BALL_SLOW_TIME_EFFECT = 5 // in seconds

export const POWER_UP_BALL_STOP = 6 // any time - all ball - limited time effect
export const POWER_UP_BALL_STOP_TIMER_EFFECT = 3 // in seconds

export const POWER_UP_BALL_BIG = 7 // any time - all ball - limited time effect
export const POWER_UP_BALL_BIG_SIZE_FACTOR = 2 // multiply the size
export const POWER_UP_BALL_BIG_TIME_EFFECT = 10 // in seconds

export const POWER_UP_BALL_LITTLE = 8 // any time - all ball - limited time effect
export const POWER_UP_BALL_LITTLE_SIZE_FACTOR = 2 // divide the size
export const POWER_UP_BALL_LITTLE_TIME_EFFECT = 10 // in seconds

export const POWER_UP_PADDLE_FAST = 9 // any time - all team paddle - limited time effect
export const POWER_UP_PADDLE_FAST_SPEED_FACTOR = 2 // multiply the speed
export const POWER_UP_PADDLE_FAST_TIME_EFFECT = 10 // in seconds

export const POWER_UP_PADDLE_SLOW = 10 // any time - all ennemy team paddle - limited time effect
export const POWER_UP_PADDLE_SLOW_SPEED_FACTOR = 2 // divide the speed
export const POWER_UP_PADDLE_SLOW_TIME_EFFECT = 10 // in seconds

export const POWER_UP_PADDLE_BIG = 11 // any time - all team paddle - limited time effect
export const POWER_UP_PADDLE_BIG_SIZE_FACTOR = 2 // multiply the size
export const POWER_UP_PADDLE_BIG_TIME_EFFECT = 10 // in seconds

export const POWER_UP_PADDLE_LITTLE = 12 // any time - all ennemy team paddle - limited time effect
export const POWER_UP_PADDLE_LITTLE_SIZE_FACTOR = 2 // divide the size
export const POWER_UP_PADDLE_LITTLE_TIME_EFFECT = 10 // in seconds


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                    COMMUNICATION DEFINE                                  //
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
export const TIME_SEND_UPDATE_INFO_TO_CLIENT = 0.01 // in seconds

//====================//
// MESSAGE DEFINITION //
//====================//
// [<message type>, <message content>]


//==================//
// CLIENT TO SERVER //
//==================//
export const CLIENT_MSG_TYPE_USER_EVENT = 0
// Content of user event :
// {id_paddle, id_key, key_action [True = press, false = release]}


//==================//
// SERVER TO CLIENT //
//==================//
export const SERVER_MSG_TYPE_CREATE_START_INFO = -1
// Content of obstacles :
// {
// 	obstables : [ {position:[x, y], points:[[x, y]], color:(r, g, b)} ]
// 	powerUp : True or false
// }

export const SERVER_MSG_TYPE_UPDATE_OBSTACLE = 0
// Content of obstacles :
// [
// 	{id, position, points:[[x, y]]}
// ]

export const SERVER_MSG_TYPE_UPDATE_PADDLES = 1
// Content of paddles :
// [
// 	{id_paddle, id_team, position:[x, y], modifierSize, powerUp, powerUpInCharge}
// ]

export const SERVER_MSG_TYPE_UPDATE_BALLS = 2
// Content of balls :
// [
// 	{position:[x, y], direction:[x, y], speed, radius, state, last_paddle_hit_info:[id, team], modifier_state}
// ]

export const SERVER_MSG_TYPE_DELETE_BALLS = 3
// Content of delete balls :
// [id_ball]

export const SERVER_MSG_TYPE_UPDATE_POWER_UP = 4
// Content of power up :
// {position:[x, y], state}
// Content of delete balls :
// [id_ball]

export const SERVER_MSG_TYPE_SCORE_UPDATE = 5
// Content of power up :
// {leftTeam, rightTeam}
