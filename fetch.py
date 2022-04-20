# Meg Risdal 2022-04-20
# https://www.kaggle.com/code/mrisdal/fetch-scrabble-data-from-woogles-io/notebook
from api import *

# get play data from a game id

game_ids = []

for game in fetch_recent('HastyBot', 1):
    game_ids.append(game['game_id'])
    
with open("data/turns.csv", "w+", newline = "") as t:

    t.write("game_id,turn_number,nickname,rack,location,move,points,score,turn_type\n")

    for game_id in game_ids:
        
        plays = fetch_gcg(game_id)

        gcg = plays['gcg']

        # print(gcg)

        # print(game_id)
        
        turn_number = 1
        
        for line in gcg.splitlines():
            if not line.startswith("#"):
                turn = line.strip(">").split(" ")

                if turn[2] == "-":
                    turn.insert(2, "")
                    turn.insert(6, "Pass")
                elif turn[2].startswith("-"):
                    turn.insert(2, "")
                    turn.insert(6, "Exchange")
                elif turn[2] == "(time)":
                    turn.insert(2, "")
                    turn.insert(6, "Timeout")
                elif turn[2].startswith("("):
                    turn.insert(2, "")
                    turn.insert(6, "Six-Zero Rule")
                elif turn[1].startswith("("):
                    turn.insert(1, "")
                    turn.insert(2, "")
                    turn.insert(6, "End")
                else:
                    turn.insert(6, "Play")

                turn.insert(0, game_id)
                turn.insert(1, str(turn_number))
                turn[2] = turn[2].strip(":")

                if(len(turn) != 9):
                    print(turn)
                    raise ValueError("Incorrect number of turn columns.")
                
                t.write(",".join(turn) + "\n")
                
                turn_number += 1
