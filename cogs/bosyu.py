from discord.ext import commands
import discord
import asyncio
import random
import MySQLdb
import os




class bosyu(commands.Cog):
    def __init__(self, bot):
        self.conn = MySQLdb.connect(
        user=os.environ['user'],
        passwd=os.environ['password'],
        host=os.environ['host'],
        db=os.environ['db'],
        charset="utf8",
        autocommit=True
        )
        self.bluesrice = 0
        self.redsrice = 0
        self.bot = bot
        self.recruitid = 1
        self.players = []
        self.lucky = []
        self.count = 0
        self.already = {}
        self.recruitm = None
        print(
            os.environ['user'],
            os.environ['password'],
            os.environ['host'],
            os.environ['db'],
        )

    @commands.command()
    async def register(self, ctx, newid):
        c = self.conn.cursor()
        sql = f"SELECT COUNT(1) FROM playerdata WHERE id = {ctx.author.id}"
        c.execute(sql)
        if c.fetchone()[0]:
            await ctx.send("すでに登録されています")
        else:
            sql = 'insert into playerdata values (%s, %s)'
            c.execute(sql, (ctx.author.id, newid))#(msg.author.id, msg.content)
            await ctx.send(f"UplayIDを:**{newid}**で登録しました")


    @commands.command()
    async def checkid(self, ctx):#自分の登録されている名前を確認
        if ctx.message.mentions:
            target = ctx.message.mentions[0]
            print("*mention*")
        else:   
            target = ctx.author
        c = self.conn.cursor()
        sql = f'select ign from playerdata where id = {target.id}'#名前を取得
        c.execute(sql)
        ign = c.fetchone()[0]
        print(f"{target.name} is {ign}")
        await ctx.send(f"{target.name}のUplayIDは **{ign}** です")
        c.close()


    @commands.command()
    async def changeid(self, ctx, newid):
    #id変更コマンド
        c = self.conn.cursor()
        sql = f"update playerdata set ign = '{newid}' where id= {ctx.author.id};"
        c.execute(sql)
        await ctx.channel.send(f"UplayIDを:**{newid}**にしました")
        c.close()

    @register.error
    async def register_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("IDを入力してください\n例```n!register id```")

    @checkid.error
    async def checkid_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("IDが登録されていません\nregisterコマンドで登録することができます\n例```n!register id```")

    @changeid.error
    async def changeid_eror(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):#引数が足りないエラー
            await ctx.send("設定するIDを入力してください\n例```n!changeid id```")
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("IDが登録されていません\nregisterコマンドで設定してください\n例```n!register id```")
    
    @commands.command()
    async def resetall(self, ctx):
        if ctx.author.guild_permissions.administrator:
            self.already.clear()
            self.players.clear()
            self.lucky.clear()
            await ctx.send("参加プレイヤーと当選プレイヤーをリセットしました")
        else:
            ctx.channel.send("このコマンドは管理者のみ使用可能です")

    # @commands.command()
    # async def resetplay(self, ctx):
    #     if ctx.author.guild_permissions.administrator:
    #         self.already.clear()
    #     else:
    #         ctx.channel.send("このコマンドは管理者のみ使用可能です")
    
    @commands.command()
    async def start(self, ctx, bluesrice: int, orangesrice: int, count=0):
        if ctx.author.guild_permissions.administrator:   
            if count == 0:
                self.count = 0
            else:
                self.count = count
            self.players.clear()#抽選参加プレイヤーをクリア
            self.lucky.clear()#当選者のリセット
            self.bluesrice = bluesrice
            self.orangesrice = orangesrice
            print(f"COUNT IS {count} class count is {self.count}")
            recruit = await ctx.channel.send("カスタムマッチの募集を始めます\n参加したい人は👍を押してください\n参加をキャンセルする場合は❌を推してください\n現在の参加プレイヤー数:**0**")
            self.recruitm = recruit
            nrecruitid = recruit.id
            self.recruitid = nrecruitid
            await recruit.add_reaction("👍")
            await recruit.add_reaction("❌")
            def check(reaction, user):
                return user.guild_permissions.administrator == reaction.message.author.guild_permissions.administrator and str(reaction.emoji) == '✅' or user.guild_permissions.administrator == reaction.message.author.guild_permissions.administrator and str(reaction.emoji) == '🔚'
                #もしつけられたリアクションが✅か🔚だったというcheck関数
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check)
                #つけられたリアクションが✅か🔚なら
            except asyncio.TimeoutError:
                #タイムアウトした場合の処理
                return
            else:
                #それ以外の場合(つけられたリアクションが✅か🔚の場合)
                if str(reaction) == '✅':#つけられたリアクションが✅ならチーム分け
                    c = self.conn.cursor()
                    await ctx.channel.send('募集を締め切り、チーム分けを行います')#チーム分けをするというメッセージ
                    print(f"参加済み:{self.players}")
                    random.shuffle(self.players)#参加しているプレイヤーが入っているリストをシャッフル
                    for i in self.players[:orangesrice + bluesrice]:#チームごとの人数*2
                        sql = f"SELECT ign from playerdata WHERE id='{i}';"#当選したプレイヤーの名前からidを入手
                        c.execute(sql)#sqlを実行
                        did = c.fetchone()[0]#ignを代入
                        self.lucky.append(did)
                    blue = self.lucky[:bluesrice]#シャッフルしたリストの中からself.sriceというチームごとの人数が入った変数を使ってスライス
                    orange = self.lucky[bluesrice:]
                    # for playerid in self.players[:bluesrice+orangesrice]:#当選したプレイヤー10人の名前をスライスでfor入
                    #     self.already[playerid] = +1#辞書"already"に当選したプレイヤーのid+プレイ回数+1を追加（何回休み家のシステムのため）
                    print(blue)#ブルーチーム
                    print(orange)#オレンジチーム
                    bjoin = '\n'.join(blue)
                    ojoin = '\n'.join(orange)
                    print(bjoin)
                    print(ojoin)
                    embed=discord.Embed(title="Team", color=0xffffff)
                    embed.add_field(name="Blue", value=f"```\n{bjoin}```", inline=False)#Blueチームにjoinで改行しながらリストblueを入れる
                    embed.add_field(name="Orange", value=f"```\n{ojoin}```", inline=False)#orangeチームにjoinで改行しながらリストorangeを入れる
                    await ctx.channel.send(embed=embed)#チーム分けを送信
                    c.close()
                elif str(reaction) == '🔚':#つけられたリアクションが🔚の場合
                    await ctx.channel.send("募集をキャンセルします")
        else:
            await ctx.channel.send("管理者のみ使用可能です")
    
    @commands.command()
    async def changeplayer(self, ctx, before: str, after: str):
        if ctx.author.guild_permissions.administrator:
            locate = self.lucky.index(before)
            self.lucky[locate] = after
            blue = self.lucky[:self.bluesrice]#シャッフルしたリストの中からself.sriceというチームごとの人数が入った変数を使ってスライス
            orange = self.lucky[self.bluesrice:self.orangesrice*2]
            embed=discord.Embed(title="Team", color=0xffffff)
            embed.add_field(name="Blue", value='\n'.join(blue), inline=False)#Blueチームにjoinで改行しながらリストblueを入れる
            embed.add_field(name="Orange", value='\n'.join(orange), inline=False)#orangeチームにjoinで改行しながらリストorangeを入れる
            await ctx.channel.send(embed=embed)#チーム分けを送信
        else:
            await ctx.send("管理者のみ使用可能です")

    @commands.command()
    async def getmember(self, ctx, ign: str):
        c = self.conn.cursor()
        sql = f'select id from playerdata where ign = "{ign}"'
        c.execute(sql)
        id = c.fetchone()
        nguild = ctx.message.guild
        member = nguild.get_member(int(id[0]))
        # await ctx.send(member.name)
        await ctx.send(member)
        
    @getmember.error#スタートコマンドのエラーハンドリング
    async def getmember_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):#引数が足りないエラー
            await ctx.send("UPLAYIDを指定してください")
        if isinstance(error, commands.errors.CommandInvokeError):#埋め込みに入れる要素がないときのエラー
            await ctx.send("該当するメンバーがいません")

    @commands.command()
    async def playerlist(self, ctx, guildid = 722059814154534932):
        playerlist = []
        embed=discord.Embed(title="Players", color=0xffffff)
        for player in  self.players:
            c = self.conn.cursor()
            sql = f'select ign from playerdata where id = "{player}"'
            c.execute(sql)
            ign = c.fetchone()
            joinuser = self.get_user(player)
            res = f"```{joinuser.name}:{ign[0]}```"
            playerlist.append(res)
        a = '\n'.join(playerlist)
        embed.add_field(name="All", value=f"```{a}```", inline=False)
        await ctx.channel.send(embed=embed)

    @start.error#スタートコマンドのエラーハンドリング
    async def start_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):#引数が足りないエラー
            await ctx.send("チームごとの人数を指定してください\n**例**\n```n!start 5```")
        if isinstance(error, commands.errors.CommandInvokeError):#埋め込みに入れる要素がないときのエラー
            await ctx.send("参加プレイヤーが足りません")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        guild = reaction.message.guild
        if user.id == 731483416163516486:
            print("It's bot")
            return
        elif str(reaction.emoji) != '👍' and str(reaction.emoji) != '❌':
            print("Not this reaction")
            return
        elif self.recruitid != reaction.message.id:
            print(f"messageid:{self.recruitid} != reactionid:{reaction.message.id}")
            print("not this massage")
            return
        elif str(reaction.emoji) == '❌':   
            print("Cancel:❌")
            if user.id in self.players:
                self.players.remove(user.id)
                #recruitmessage = await reaction.message.channel.fetch_message(self.recruitid)
                await self.recruitm.edit(content=f"カスタムマッチの募集を始めます\n参加したい人は👍を押してください\n参加をキャンセルする場合は❌を押してください\n現在の参加プレイヤー数:**{len(self.players)}**")
                try:
                    await user.send('参加を取り消しました')
                except discord.errors.Forbidden:
                    print(f"Failed sent to cancel message Name:{user.name}")
            else:
                await user.send("参加していないためキャンセルできませんでした")
            for mreaction in reaction.message.reactions:
                await mreaction.remove(user)
        else:
            print("Correct Reaciton:👍")
            userid = user.id
            if userid not in self.already:
                self.already[userid] = 0
            c = self.conn.cursor()
            sql = f"SELECT COUNT(1) FROM playerdata WHERE id = {int(userid)}"
            c.execute(sql)
            if c.fetchone()[0]:
                # if 1 <= self.already[userid] <= self.count:
                #     await user.send(f"一度参加したため参加できません\nあと**{self.count}マッチ後**に参加できます※参加できるまで配信が続くかはわかりません")#参加した回数1
                #     return
                if userid in self.players:
                    print("You already joined")
                    return
                self.players.append(userid)
                player = guild.get_member(userid)
                print(f"Add player:{userid} NAME:{player.name}")
                await self.recruitm.edit(content=f"カスタムマッチの募集を始めます\n参加したい人は👍を押してください\n参加をキャンセルする場合は❌を推してください\n現在の参加プレイヤー数:**{len(self.players)}**")
                print(self.players)
                c.close()
            else:
                await user.create_dm()
                dmid = user.dm_channel.id
                await reaction.remove(user)
                try:
                    await user.send("**UplayID**が未登録です。\n**UplayID**を送信してください\nまた**__IDを送信したあとに募集のメッセージにもう一度リアクションをつけてください__**")
                except discord.errors.Forbidden:
                    print(f"Failed Send DM to {user.id}Name:{user.name}")
                print(f"Sent message to {userid}")
                await user.create_dm()
                def check(m):
                    return userid == m.author.id and dmid == m.channel.id
                try:
                    msg = await self.bot.wait_for('message', check=check, timeout = 60)
                except asyncio.TimeoutError:
                    await user.send('タイムアウトしました\nbotがメッセージ送信されてから60秒以内にIDを送ってください')
                else:
                    sql = 'insert into playerdata values (%s, %s)'
                    c.execute(sql, (msg.author.id, msg.content))#(msg.author.id, msg.content)
                    c.close()
                    print(f"Register player Name:{msg.content}")
                    await user.send(f"UplayIDを:**{msg.content}**で登録しました")


def setup(bot):
     bot.add_cog(bosyu(bot))
    
