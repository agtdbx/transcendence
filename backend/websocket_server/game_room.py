import sys
from websocket_server.game_server_manager import create_new_game, is_game_server_free

#game_rooms
# id : {'creator':<id>,
#       'power_up':<bool>,
#       'map_id':<int>,
#       'team_left':list[<id>],
#       'team_right':list[<id>]}
# If you add an ia, the id will be -1

async def create_game_room(my_id : int,
                          game_rooms : dict,
                          in_game_list: list,
                          connected_users : dict):
    # If the user is already in waitlist or in game, don't pu it in waitlist
    if my_id in in_game_list:
        print("\nWS : User", my_id, "already in waitlist or in game",
              file=sys.stderr)
        return

    room_id = len(game_rooms)
