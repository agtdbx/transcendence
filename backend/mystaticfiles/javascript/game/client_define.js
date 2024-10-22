// import pygame as pg

import * as d from "./define.js"

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                      WINDOW DEFINE                                       //
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
export const WIN_WIDTH = 1800 // in pixel
export const WIN_HEIGHT = 900 // in pixel
export const WIN_CLEAR_COLOR = (0, 0, 0) // (r, g, b), channel int [0, 255]


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                      BALL DEFINE                                       //
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
export const BALL_COLOR = (255, 255, 255) // (r, g, b), channel int [0, 255]
export const BALL_TRAIL_OPACITY = 0.5 // float [0, 1]
export const BALL_TRAIL_LENGTH = 30 // number of cicles in trail


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                        MAP DEFINE                                        //
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
export var AREA_RECT = [(WIN_WIDTH - d.AREA_SIZE[0]) / 2, (WIN_HEIGHT - d.AREA_SIZE[1]) / 2, d.AREA_SIZE[0], d.AREA_SIZE[1]]
export const AREA_COLOR = (100, 100, 100) // (r, g, b), channel int [0, 255]

export const AREA_LEFT_TEAM_RECT = (AREA_RECT[0], AREA_RECT[1], d.SPACE_PART, d.AREA_SIZE[1])
export const AREA_MIDDLE_RECT = (AREA_RECT[0] + d.SPACE_PART, AREA_RECT[1], d.AREA_SIZE[0] - d.SPACE_PART, d.AREA_SIZE[1])
export const AREA_RIGTH_TEAM_RECT = (AREA_RECT[0] + d.AREA_SIZE[0] - d.SPACE_PART, AREA_RECT[1], d.SPACE_PART, d.AREA_SIZE[1])
export const AREA_TEAM_COLOR = (90, 90, 90) // (r, g, b), channel int [0, 255]


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                       PADDLE DEFINE                                      //
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
export const PADDLE_COLOR = (200, 200, 200) // (r, g, b), channell int [0, 255]


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                       DEBUG DEFINE                                       //
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
export const DRAW_HITBOX = false // boolean
export const DRAW_HITBOX_NORMALS = false // boolean
export const HITBOX_BALL_COLOR = (255, 0, 0) // (r, g, b), channel int [0, 255]
export const HITBOX_WALL_COLOR = (0, 255, 0) // (r, g, b), channel int [0, 255]
export const HITBOX_PADDLE_COLOR = (0, 0, 255) // (r, g, b), channel int [0, 255]


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                       POWER UP DEFINE                                    //
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Power up object state
export const POWER_UP_HITBOX_COLOR = (200, 100, 100) // (r, g, b), channell int [0, 255]

// Power up list and effects define
export const POWER_UP_BALL_FAST_COLOR = "#FF00FF" // in seconds
export const POWER_UP_BALL_WAVE_COLOR = "#00FFFF" // in seconds
export const POWER_UP_BALL_INVISIBLE_COLOR = "#FFFF00" // in seconds


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                      CLIENT DEFINE                                       //
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// PLAYERS KEYS QWERTY
export const PLAYER_KEYS = [
	["KeyQ", "KeyA", "KeyS", "Space"], // L1 player
	["KeyQ", "KeyA", "KeyS", "Space"], // L2 player
	["KeyQ", "KeyA", "KeyS", "Space"], // R1 player
	["KeyQ", "KeyA", "KeyS", "Space"], // R2 player
]

// // PLAYERS KEYS AZERTY
// PLAYER_KEYS = [
// ["KeyA", "KeyQ", "KeyW", "Space"], // L1 player
// ["KeyZ", "KeyS", "KeyX", "Space"], // L2 player
// ["KeyO", "KeyK", "Comma", "Space"], // R1 player
// ["KeyI", "KeyJ", "KeyN", "Space"], // R2 player
// ]
