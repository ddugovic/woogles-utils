from api import *
from game import *
from utils import plural

# get play data from a game id

game_ids = []

for game in fetch_recent('BasicBot', 1):
    game_ids.append(game['game_id'])
    
with open("data/turns.csv", "w+", newline = "") as t:

    t.write("game_id,turn_number,nickname,rack,location,move,points,score,turn_type\n")

    for game_id in game_ids:
        plays = fetch_gcg(game_id)

        print("Parsing game %s..." % game_id)
        
        gcg = plays['gcg']

        turn_number = 0
        
        for line in gcg.splitlines():
            if not line.startswith("#"):
                turn_number += 1
                turn = parse_turn(line)

                turn.insert(0, game_id)
                turn.insert(1, str(turn_number))
                turn[2] = turn[2].strip(":")

                if(len(turn) != 9):
                    print(turn)
                    raise ValueError("Incorrect number of turn columns.")
                
                t.write(",".join(turn) + "\n")

        print("Parsed game %s (%d %s)..." % (game_id, turn_number, plural('turn', turn_number)))
