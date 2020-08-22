from discord.ext import commands
import traceback

INITIAL_EXTENSIONS = [
    'cogs.normal',
    'cogs.hime'
]

class MyBot(commands.Bot):
    def __init__(self, command_prefix):
        # スーパークラスのコンストラクタに値を渡して実行。
        super().__init__(command_prefix)

        for cog in INITIAL_EXTENSIONS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    async def on_ready(self):
        print(f"{self.user.name} is Ready.")

if __name__ == '__main__':
    bot = MyBot(command_prefix='n!')
    bot.load_extension('dispander')
    bot.run('NzMxNDgzNDE2MTYzNTE2NDg2.XwmtBA.BXh3o1iA2RyTICJbc7s9g2phMc4') # Botのトークン
