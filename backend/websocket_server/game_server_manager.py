import os
import sys
import ssl
import asyncio
import datetime
import websockets
from websocket_server.utils import set_user_status, get_user_by_id
from db_test.models import Match, MatchUser, Goal, Map, Achivement
from backend.views_achievement import createAchievementIfNot, \
                                      getListeMatchDataForAchievement

# ssl context
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.load_verify_locations("/certs/cert.pem")

# List of game server
# List : [server running, port] ; if thread is False, the server is unused
game_servers = [
    [False, 8766],
    [False, 8767],
    [False, 8768],
    [False, 8769],
    [False, 8770]
]


def is_game_server_free():
    print("\nWS : ALL SERVER :", game_servers, file=sys.stderr)

    for i in range(len(game_servers)):
        if game_servers[i][0] == False:
            return True

    return False


async def start_game_websocket(port:int,
                               map_id : int,
                               power_up_enable : bool,
                               team_left:list[int],
                               team_right:list[int],
                               type:int):
    os.system("python3 pong_server/ws_game_server.py " + str(port) + "&")
    await asyncio.sleep(1)
    os.system("echo; echo WS : websocket now running on wss://localhost:" +
              str(port))
    ws = await websockets.connect("wss://localhost:" + str(port), ssl=ssl_context)
    msg = {"type":"info",
           "mapId" : map_id,
           "powerUp" : str(power_up_enable).lower(),
           "teamLeft" : team_left,
           "teamRight" : team_right,
           "gameType" : type}
    str_msg = str(msg).replace("'", '"')
    await ws.send(str_msg)
    await ws.close()
    print("\nWS : all info go to game server", file=sys.stderr)


async def start_local_game_websocket(my_id:int,
                                     port:int,
                                     map_id : int,
                                     power_up_enable : bool,
                                     team_left:list[int],
                                     team_right:list[int],
                                     type:int):
    os.system("python3 pong_server/ws_local_game_server.py " + str(port) + "&")
    await asyncio.sleep(1)
    os.system("echo; echo WS : websocket now running on wss://localhost:" +
              str(port))
    ws = await websockets.connect("wss://localhost:" + str(port), ssl=ssl_context)
    if type == 4:
        msg = {"type":"info",
               "my_id" : my_id,
               "mapId" : map_id,
               "powerUp" : str(power_up_enable).lower(),
               "teamLeft" : team_left,
               "teamRight" : team_right,
               "gameType" : type}
    else:
        msg = {"type":"info",
               "mapId" : map_id,
               "powerUp" : str(power_up_enable).lower(),
               "teamLeft" : team_left,
               "teamRight" : team_right,
               "gameType" : type}
    str_msg = str(msg).replace("'", '"')
    await ws.send(str_msg)
    await ws.close()
    print("\nWS : all info go to local game server", file=sys.stderr)


async def create_new_game(in_game_list : list,
                          map_id : int,
                          power_up_enable : bool,
                          team_left:list[int],
                          team_right:list[int],
                          type:int):
    print("\nWS : ALL SERVER :", game_servers, file=sys.stderr)

    for i in range(len(game_servers)):
        if game_servers[i][0] == False:
            game_servers[i][0] = True

            print("\nWS : START GAME ON SERVER :", i, file=sys.stderr)
            await start_game_websocket(game_servers[i][1],
                                       map_id, power_up_enable,
                                       team_left, team_right, type)

            print("\nWS : SERVER CREATED", file=sys.stderr)
            for id in team_left:
                if id >= 0:
                    in_game_list.append(id)
                    set_user_status(id, 2)
            print("\nWS : SET MID STATUS OK", file=sys.stderr)
            for id in team_right:
                if id >= 0:
                    in_game_list.append(id)
                    set_user_status(id, 2)
            print("\nWS : SET STATUS OK", file=sys.stderr)

            return i, game_servers[i][1]

    return None


async def create_new_local_game(my_id:int,
                                in_game_list : list,
                                map_id : int,
                                power_up_enable : bool,
                                team_left:list[int],
                                team_right:list[int],
                                type:int):
    print("\nWS : ALL SERVER :", game_servers, file=sys.stderr)

    for i in range(len(game_servers)):
        if game_servers[i][0] == False:
            game_servers[i][0] = True

            print("\nWS : START LOCAL GAME ON SERVER :", i, file=sys.stderr)
            await start_local_game_websocket(my_id, game_servers[i][1],
                                             map_id, power_up_enable,
                                             team_left, team_right, type)

            print("\nWS : SERVER CREATED", file=sys.stderr)
            in_game_list.append(my_id)
            set_user_status(my_id, 2)
            print("\nWS : SET STATUS OK", file=sys.stderr)

            return i, game_servers[i][1]

    return None


def modifyAchievement(user):
    listData = getListeMatchDataForAchievement(user)
    if (createAchievementIfNot(user)):
        try :
            achievement = Achivement.objects.all().filter(idUser=user.idUser)[0]
            achievement.winner = 0 if (listData[0] == 0) else (1 if (listData[0] < 21) else ((2 if (listData[0] < 42) else 3)))
            achievement.perfectShoot = 0 if (listData[1] == 0) else (1 if (listData[1] == 1) else ((2 if (listData[1] < 10) else 3)))
            achievement.digGrave =  0 if (listData[2] == 0) else 4
            achievement.unpredictable = 0 if (listData[3] < 10) else (1 if (listData[3] < 21) else ((2 if (listData[3] < 42) else 3)))
            achievement.faster = 0 if (listData[4] < 1000) else (1 if (listData[4] < 1920) else ((2 if (listData[4] < 4242) else 3)))
            achievement.waveComming = 0 if (listData[5] == 1) else (2 if (listData[5] == 2) else ((4 if (listData[5] < 8) else 8)))
            achievement.notPassed = 0 if (listData[6] == 0) else (1 if (listData[6] < 21) else ((2 if (listData[6] < 42) else 3)))
            achievement.party = 0 if (listData[7] == 0) else (1 if (listData[7] < 21) else ((2 if (listData[7] < 42) else 3)))
            achievement.molyBattle  = 0 if (listData[8] == 0) else (1 if (listData[8] < 21) else ((2 if (listData[8] < 42) else 3)))
            achievement.save()
        except :
            print("\nWS : Erreur while modifing achievement of  : ", user.username, file=sys.stderr)



async def end_game(data:dict,
                   in_game_list: list) -> bool:
    global game_servers

    print("\nWS : END GAME DETECTED", file=sys.stderr)

    # Get port info
    port = data.get("port", None)
    if port == None:
        print("\nWS : MISSING PORT :", data, file=sys.stderr)
        return None

    try:
        port = int(port)
    except:
        print("\nWS : PORT ISN'T AN INT:", data, file=sys.stderr)
        return None

    print("\nWS : PORT :", port, file=sys.stderr)

    for i in range(len(game_servers)):
        if game_servers[i][1] == port:
            game_servers[i][0] = False
            print("\nWS : SERVER ON PORT", port, "IS NOW FREE", file=sys.stderr)
            print("\nWS : ALL SERVER :", game_servers, file=sys.stderr)

    # Get users fielfs
    team_left = data.get("teamLeft", None)
    if team_left == None:
        print("\nWS : Missing info team_left was in game :", data,
              file=sys.stderr)

     # Get users fielfs
    team_right = data.get("teamRight", None)
    if team_right == None:
        print("\nWS : Missing info team_left was in game :", data,
              file=sys.stderr)

    # Set status of users and remove them from in game list
    my_id = data.get("my_id", None)
    if my_id == None:
        for id in team_left:
            if id >= 0:
                set_user_status(id, 1)
                if id in in_game_list:
                    in_game_list.remove(id)

        for id in team_right:
            if id >= 0:
                set_user_status(id, 1)
                if id in in_game_list:
                    in_game_list.remove(id)
    else:
        print("\nWS : My id :", my_id, file=sys.stderr)
        my_id = int(my_id)
        set_user_status(my_id, 1)
        in_game_list.remove(my_id)

    # Get stats info
    stats = data.get("stats", None)
    if stats == None:
        print("\nWS : MISSING STATS :", data, file=sys.stderr)
        return None

    # GAME STATS
    game_stats = stats[0]

    # TEAM LEFT STATS
    left_team_stats = stats[1]

    # TEAM RIGHT STATS
    right_team_stats = stats[2]

    # BALLS STATS
    balls_stats = stats[3]

    # Get type info
    game_type = data.get("gameType", None)
    if game_type == None:
        print("\nWS : MISSING TYPE :", data, file=sys.stderr)
        return None

    print("\nWS : ALL FIELDS GOOD", file=sys.stderr)

    # If the type is quick game, modify money of users
    if game_type == 0:
        print("\nWS : UPDATE MONEY", file=sys.stderr)
        # Get winner and loser
        if game_stats[0] > game_stats[1]:
            user_winner = get_user_by_id(team_left[left_team_stats[0][0]])
            user_loser = get_user_by_id(team_right[right_team_stats[0][0]])
        else:
            user_winner = get_user_by_id(team_right[right_team_stats[0][0]])
            user_loser = get_user_by_id(team_left[left_team_stats[0][0]])

        print("\nWS : Winner :", user_winner.username, "-", user_winner.money,
              file=sys.stderr)
        print("WS : Loser :", user_loser.username, "-", user_loser.money,
              file=sys.stderr)

        # Update money
        diff = user_winner.money - user_loser.money
        if diff >= 5:
            print("\nWS : +1 -1", file=sys.stderr)
            user_winner.money += 1
            user_loser.money -= 1
        elif diff <= -5:
            print("\nWS : +4 -3", file=sys.stderr)
            user_winner.money += 4
            user_loser.money -= 3
        else:
            print("\nWS : +2 -1", file=sys.stderr)
            user_winner.money += 2
            user_loser.money -= 1

        if user_loser.money < 0:
            user_loser.money = 0

        user_winner.save()
        user_loser.save()
        print("WS : DONE", file=sys.stderr)

    winner = None

    # If the type is tournament
    if game_type == 2:
        if game_stats[0] > game_stats[1]:
            print("\nWS : WINNER IS LEFT", file=sys.stderr)
            winner = (game_type, team_left[left_team_stats[0][0]])
        else:
            print("\nWS : WINNER IS RIGHT", file=sys.stderr)
            winner = (game_type, team_right[right_team_stats[0][0]])

    if game_type == 4:
        if game_stats[0] > game_stats[1]:
            print("\nWS : WINNER IS LEFT", file=sys.stderr)
            winner = (game_type, team_left[left_team_stats[0][0]],
                      game_stats[0], game_stats[1], my_id)
        else:
            print("\nWS : WINNER IS RIGHT", file=sys.stderr)
            winner = (game_type, team_right[right_team_stats[0][0]],
                      game_stats[0], game_stats[1], my_id)

    # PUT MATCH IN DB
    print("\nWS : PUT MATCH IN DB", file=sys.stderr)
    match_id = Match.objects.all().count()
    match_date = (datetime.datetime.now() +
                  datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M')
    match_time = int(game_stats[3]) + 1
    test_map = Map.objects.all().filter(idMap=game_stats[4])
    if len(test_map) != 1:
        print("\nWS : MAP NOT FOUND", file=sys.stderr)
        return
    map = test_map[0]

    power_up = False
    if game_stats[5] == "true":
        power_up = True

    match = Match.objects.create(idMatch=match_id, type=game_type,
                                 matchDate=match_date, matchDuration=match_time,
                                 idMap=map, powerUp=power_up,
                                 scoreLeft=game_stats[0], scoreRight=game_stats[1],
                                 nbMaxBallOnGame=game_stats[2])

    match.save()
    print("WS : DONE", file=sys.stderr)

    # PUT USERS MATCH IN DB
    for paddle_stats in left_team_stats:
        print("\nWS : PUT LEFT USER MATCH IN DB", file=sys.stderr)
        user_match_id = MatchUser.objects.all().count()
        if game_type == 4:
            user = get_user_by_id(my_id)
        else:
            user = get_user_by_id(team_left[paddle_stats[0]])

        match_user = MatchUser.objects.create(id=user_match_id, idMatch=match,
                                              idUser=user, nbGoal=paddle_stats[1],
                                              maxBallSpeed=paddle_stats[2],
                                              maxBallBounce=paddle_stats[3],
                                              nbCC=paddle_stats[4],
                                              nbPerfectShot=paddle_stats[5],
                                              idTeam=paddle_stats[6],
                                              idPaddle=paddle_stats[0])
        match_user.save()
        print("WS : DONE", file=sys.stderr)
        if game_type < 3:
            print("WS : MODIFY ACHIVEMENT", file=sys.stderr)
            modifyAchievement(user)

    for paddle_stats in right_team_stats:
        print("\nWS : PUT RIGHT USER MATCH IN DB", file=sys.stderr)
        user_match_id = MatchUser.objects.all().count()
        if game_type == 4:
            user = get_user_by_id(my_id)
        else:
            user = get_user_by_id(team_right[paddle_stats[0]])

        match_user = MatchUser.objects.create(id=user_match_id, idMatch=match,
                                              idUser=user, nbGoal=paddle_stats[1],
                                              maxBallSpeed=paddle_stats[2],
                                              maxBallBounce=paddle_stats[3],
                                              nbCC=paddle_stats[4],
                                              nbPerfectShot=paddle_stats[5],
                                              idTeam=paddle_stats[6],
                                              idPaddle=paddle_stats[0])
        match_user.save()
        print("WS : DONE", file=sys.stderr)
        if game_type < 3:
            print("WS : MODIFY ACHIVEMENT", file=sys.stderr)
            modifyAchievement(user)

    # PUT GOAL STATS IN DB
    for goal_stats in balls_stats:
        print("\nWS : PUT GOAL IN DB", file=sys.stderr)
        id_goal = Goal.objects.all().count()
        if game_type == 4:
            user = get_user_by_id(my_id)
        else:
            if goal_stats[1] == 0:
                user = get_user_by_id(team_left[goal_stats[0]])
            else:
                user = get_user_by_id(team_right[goal_stats[0]])

        perfect_shot = False
        if goal_stats[5] == "true":
            perfect_shot = True

        own_goal = False
        if goal_stats[4] == "true":
            own_goal = True

        goal = Goal.objects.create(id=id_goal, idUser=user, goalTime=goal_stats[6],
                                   idMatch=match, nbBounce=goal_stats[3],
                                   perfectedShot=perfect_shot,
                                   ballSpeed=goal_stats[2], ownGoal=own_goal,
                                   idTeam=goal_stats[1],
                                   idPaddle=goal_stats[0])
        goal.save()
        print("WS : DONE", file=sys.stderr)

    print("WS : ALL END GAME PUT IN DB", file=sys.stderr)
    return winner
