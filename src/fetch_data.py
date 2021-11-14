from datetime import datetime
import pytz
import requests
import json
import argparse


def get_game_archive_list(player):
    try:
        url = f"https://api.chess.com/pub/player/{player}/games/archives"
        response = requests.get(url)
        data = response.text
        archives_list = json.loads(data)['archives']
    except:
        raise ValueError(f'Could not get games archive for player {player}')
    return archives_list


def read_games_from_archives(url) -> list:
    try:
        response = requests.get(url)
        data = response.text
        return json.loads(data)['games']
    except:
        raise ValueError(f"Can't read archive url {url}")


def game_id_from_url(url):
    ''' Urls look like 'https://www.chess.com/live/game/6071303142'''
    return url.split('/')[-1]


def get_metadata(player):
    tz_str = 'UTC'  # Match game data that are in UTC
    tz = pytz.timezone(tz_str)

    metadata = {
        'player_name': player,
        'aggregation_tz': tz_str,
        'aggregation_timestamp': datetime.now(tz).strftime("%H:%M:%S")}
    return metadata


def main(player):
    games_dict = {'data': {}}
    games_dict['metadata'] = get_metadata(player)

    archive_urls = get_game_archive_list(player)
    for url in archive_urls:
        archive_games = read_games_from_archives(url)
        for game in archive_games:
            game_id = game_id_from_url(game['url'])
            games_dict['data'][game_id] = game

    with open('data/raw_data.json', 'w') as fp:
        json.dump(games_dict, fp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    main(player=args.player)
