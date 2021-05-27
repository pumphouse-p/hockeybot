import anyio
from semaphore import Bot, ChatContext

bot = Bot("+13322036573")

@bot.handler('')
async def echo(ctx: ChatContext) -> None:
    await ctx.message.reply(ctx.message.get_body() + " and shove it up your butt!")

async def main():
    async with bot:
        await bot.set_profile("Example bot")

        await bot.start()

anyio.run(main)