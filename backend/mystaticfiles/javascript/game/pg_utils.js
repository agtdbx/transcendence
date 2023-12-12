// import pygame as pg

function drawText(surface, text, pos, color=(0, 0, 0), size=24, font=None, align="left")
{
	//TODO convert function for transition

	font = pg.font.SysFont(font, size)
	img = font.render(text, true, color)

	if (align == "top-left")
		placement = pos
	else if (align == "mid-left")
		placement = (pos[0], pos[1] - img.get_height() / 2)
	else if (align == "bot-left")
		placement = (pos[0], pos[1] - img.get_height())

	else if (align == "top-center")
		placement = (pos[0] - img.get_width() / 2, pos[1])
	else if (align == "mid-center")
		placement = (pos[0] - img.get_width() / 2, pos[1] - img.get_height() / 2)
	else if (align == "bot-center")
		placement = (pos[0] - img.get_width() / 2, pos[1] - img.get_height())

	else if (align == "top-right")
		placement = (pos[0] - img.get_width(), pos[1])
	else if (align == "mid-right")
		placement = (pos[0] - img.get_width(), pos[1] - img.get_height() / 2)
	else if (align == "bot-right")
		placement = (pos[0] - img.get_width(), pos[1] - img.get_height())

	surface.blit(img, placement)
}
