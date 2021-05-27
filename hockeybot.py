"""
Signal bot that returns data from the NHL Stats API.
"""
import requests
import os
import anyio
from datetime import datetime
from pytz import timezone

from semaphore import Bot, ChatContext

from nhlapi.team import get_next_game, get_last_game, get_roster

BASEURL = "https://statsapi.web.nhl.com/api/v1/"
TOR_ID = "10"

async def handle_msg(ctx: ChatContext) -> None:
    raw_msg = ctx.message.get_body()
    parsed_msg = raw_msg.split(' ')
    response = ''
    if len(parsed_msg) > 1:
        if parsed_msg[1] == 'help':
            await _handle_help(ctx)
        elif parsed_msg[1] == 'team':
            if parsed_msg[3] == 'nextgame':
                response = await get_next_game(team='foo')
            elif parsed_msg[3] == 'lastgame':
                response = await get_last_game(team='foo')
            elif parsed_msg[3] == 'roster':
                response = await get_roster(team='foo')
        

        await ctx.message.reply(response)
        # await ctx.message.reply(str(parsed_msg))

    else:
        s = 'I am HockeyBot, and I am here to service all your hockey needs.\n'
        s += 'To get help, just ask you knucklehead. Send me a message that reads "/hbot help".'
        await ctx.message.reply(s)

async def _handle_help(ctx: ChatContext) -> None:
    s = "Here are the available commands that you send to me:\n"
    s += "/hbot help : Print this message"
    s += "/hbot team : Print a list of all team names and their abbrevations"
    s += "/hbot team <TEAM> nextgame : Get the next game for <TEAM>"
    await ctx.message.reply(s)

async def foo_get_next_game(ctx: ChatContext) -> None:
    url = '{}/teams/{}?expand=team.schedule.next'.format(BASEURL, TOR_ID)
    response = requests.get(url)
    response_json = response.json()
    away_team = response_json['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['teams']['away']['team']['name']
    home_team = response_json['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['teams']['home']['team']['name']
    game_date = response_json['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['gameDate']
    game_datetime = datetime.strptime(game_date, "%Y-%m-%dT%H:%M:%SZ")
    game_datetime = game_datetime.astimezone(timezone('America/New_York'))
    date = game_datetime.strftime("%a %b %-d at %-I:%m %p")
    message = 'The {} visit the {} on {}'.format(
        away_team,
        home_team,
        date
    )
    await ctx.message.reply(body=message)

async def hbot(ctx: ChatContext) -> None:
    await handle_msg(ctx)

async def main():
    # Connect the bot to the phone number found in the environment
    async with Bot(os.environ["SIGNAL_PHONE_NUMBER"]) as bot:
        bot.register_handler("/hbot", hbot)

        # Set the profile name
        await bot.set_profile("Hockeybot")
        # Run the bot until the user hits Ctrl-c.
        await bot.start()

if __name__ == '__main__':
    anyio.run(main)