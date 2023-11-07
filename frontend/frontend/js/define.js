/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   define.js                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: lflandri <lflandri@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/11/07 13:27:34 by lflandri          #+#    #+#             */
/*   Updated: 2023/11/07 13:32:29 by lflandri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

WIN_WIDTH = 1280
WIN_HEIGHT = 700
WIN_CLEAR_COLOR = (0, 0, 0)

AREA_MARGIN = 50
AREA_RECT = (AREA_MARGIN, AREA_MARGIN, WIN_WIDTH - (AREA_MARGIN * 2), WIN_HEIGHT - (AREA_MARGIN * 2))
AREA_COLOR = (100, 100, 100)
AREA_BORDER_SIZE = 10
AREA_BORDER_COLOR = (200, 200, 200)
AREA_BORDER_RECT = (AREA_RECT[0] - AREA_BORDER_SIZE,
					AREA_RECT[1] - AREA_BORDER_SIZE,
					AREA_RECT[2] + (AREA_BORDER_SIZE * 2),
					AREA_RECT[3] + (AREA_BORDER_SIZE * 2))

BALL_RADIUS = 10
BALL_COLOR = (255, 255, 255)
BALL_TRAIL_OPACITY = 0.5
BALL_TRAIL_LENGTH = 30
BALL_MAX_SPEED = 500
BALL_MINIMUM_FRICTION = 100
BALL_FRICTION_STRENGTH = 0.1

DRAW_HITBOX = False
DRAW_HITBOX_NORMALS = False
HITBOX_BALL_COLOR = (255, 0, 0)
HITBOX_WALL_COLOR = (0, 255, 0)
HITBOX_PADDLE_COLOR = (0, 0, 255)

