from api import *
from game import *
from utils import plural
    
def fetch(username, num):
    # get play data from a game id
    
    games = {}
    
    for game in fetch_recent(username, num):
        games[game['game_id']] = game
        
    with open("data/turns.csv", "w+", newline = "") as t:
    
        t.write("game_id,turn_number,nickname,rack,location,move,points,score,turn_type\n")
    
        for game_id in games:
            players = games[game_id]['players']
            player1, player2 = players[0], players[1]
            if bool(player2['first']):
                player1, player2 = player2, player1

            plays = fetch_gcg(game_id)

            print("Parsing game %s (%s - %s)..." % (game_id, player1['nickname'], player2['nickname']), end = ' ')
    
            gcg = plays['gcg']
    
            turn_number = 0
            
            for line in gcg.splitlines():
                if not line.startswith("#"):
                    turn_number += 1
                    turn = parse_turn(line, game_id, turn_number)
                    
                    t.write(",".join(turn) + "\n")
    
            print("%d %s." % (turn_number, plural('turn', turn_number)))


if __name__ == '__main__':
    fetch('BasicBot', 1)
