# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aderouba <aderouba@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/10/19 17:13:10 by aderouba          #+#    #+#              #
#    Updated: 2023/10/20 14:10:20 by aderouba         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NOC			= \e[0m
BOLD		= \e[1m
UNDERLINE	= \e[4m
BLACK		= \e[1;30m
RED			= \e[1m\e[38;5;196m
GREEN		= \e[1m\e[38;5;76m
YELLOW		= \e[1m\e[38;5;220m
BLUE		= \e[1m\e[38;5;33m
VIOLET		= \e[1;35m
CYAN		= \e[1;36m
WHITE		= \e[1;37m


all:
	@echo "$(GREEN)Start server !$(NOC)"
	@docker volume ls | grep db_data || docker volume create db_data
	@docker compose up -d

clean:
	@echo "$(BLUE)Server stop$(NOC)"
	@docker compose down

fclean: clean
	@echo "$(BLUE)Remove own image$(NOC)"
	@docker image rm transcendence-backend 2>/dev/null || echo "$(RED)Backend image not exist$(NOC)"
	@docker image rm transcendence-frontend 2>/dev/null || echo "$(RED)Front image not exist$(NOC)"

vclean: fclean
	@docker volume rm $$(docker volume ls -q) 2>/dev/null || echo "$(RED)No volume to delete$(NOC)"

fullclean: vclean
	@echo "$(BLUE)Remove premake image$(NOC)"
	@docker image rm $$(docker image ls -aq) 2>/dev/null || echo "$(RED)Premake image aren't install$(NOC)"

re : fclean all

.PHONY: all clean fclean re
