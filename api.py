import requests
import json
from utils import plural

HEADERS = {
    'authority': 'woogles.io',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'accept': 'application/json, text/plain, */*',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://woogles.io',
    'accept-language': 'en-US,en;q=0.9'
}

GCG_URL = 'https://woogles.io/twirp/game_service.GameMetadataService/GetGCG'
RECENT_URL = 'https://woogles.io/twirp/game_service.GameMetadataService/GetRecentGames'

def fetch_gcg(game_id):
    params = '{"gameId":"%s"}'

    print("Downloading game %s..." % game_id)
    game_response = requests.post(GCG_URL, headers = HEADERS, data = (params % game_id))

    return json.loads(game_response.text)

def fetch_recent(username, num):
    params = '{"username":"%s","numGames":%d,"offset":%d}'

    result = list()


    print("Downloading %d %s..." % (num, plural('game', num)))
    step = 20
    for offset in range(0, num, step):
        size = min(step, num - offset)
        games_response = requests.post(RECENT_URL, headers = HEADERS, data = (params % (username, size, offset)))

        games = json.loads(games_response.text)

        if game_count := len(games['game_info']):
            result.extend(games['game_info'])
        else:
            break

    with open('data/woogles.json', 'w') as output_file:
        json.dump(result, output_file)
        count = offset + game_count
        print("Finished downloading game metadata (%d %s)." % (count, plural('game', count)))

    return result
