from api import *
from game import *
from sys import argv
from utils import plural
    
def fetch(username, num):
    print("Downloading %d %s..." % (num, plural('game', num)), end=' ')
    count, games = fetch_recent(username, num)
    print("done (%d %s downloaded)." % (count, plural('game', count)))

    # get play data from a game id
    with open("data/turns.csv", "w+", newline = "") as t:
    
        t.write("game_id,turn_number,nickname,rack,location,move,points,score,turn_type\n")
    
        for game in games:
            game_id = game['game_id']
            players = game['players']
            player1, player2 = players[0], players[1]
            if bool(player2['first']):
                player1, player2 = player2, player1

            print("Downloading game %s..." % game_id)
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
    username = argv[1] if len(argv) > 1 else 'HastyBot'
    num = argv[2] if len(argv) > 2 else '1'
    fetch(username, int(num))
