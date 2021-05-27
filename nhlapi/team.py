"""
Handles the team related commands.
"""
from datetime import datetime
from pytz import timezone

import nhlapi.utils 

async def get_next_game(team):
    endpoint = '/teams/{}?expand=team.schedule.next'.format('10')
    r = nhlapi.utils.get(endpoint=endpoint)
    away_team = r['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['teams']['away']['team']['name']
    home_team = r['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['teams']['home']['team']['name']
    game_date = r['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['gameDate']
    game_datetime = datetime.strptime(game_date, "%Y-%m-%dT%H:%M:%SZ")
    game_datetime = game_datetime.astimezone(timezone('America/New_York'))
    date = game_datetime.strftime("%a %b %-d at %-I:%m %p")
    message = "{} @ {} - {}".format(
        away_team,
        home_team,
        date
    )

    return message

async def get_last_game(team):
    endpoint = '/teams/{}?expand=team.schedule.previous'.format('10')
    r = get(endpoint=endpoint)
    away = r['teams'][0]['previousGameSchedule']['dates'][0]['games'][0]['teams']['away']
    home = r['teams'][0]['previousGameSchedule']['dates'][0]['games'][0]['teams']['home']
    message = '{} {}\n{} {}\n{}'.format(
        away['team']['name'],
        away['score'],
        home['team']['name'],
        home['score'],

    )

    return message


async def get_roster(team):
    endpoint = '/teams/{}?expand=team.roster'.format('10')
    r = get(endpoint=endpoint)
    players = [person for person in r['teams'][0]['roster']['roster']]
    players = sorted(players, key=lambda k: k['position']['code'])
    message = ''
    for player in players:
        message += '{} / {} / {}\n'.format(
            player['position']['code'],
            player['person']['fullName'],
            player['jerseyNumber']
        )

    return message
