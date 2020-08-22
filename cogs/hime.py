from discord.ext import tasks, commands
import discord
import asyncio
import random
import MySQLdb
import os




class hime(commands.Cog):
    def __init__(self, bot):
        self.conn = MySQLdb.connect(
        user='admin',
        passwd='OZmLQi6yXjvtmLvuKJWB',
        host='nakagawa.cgfmfgfg5hjd.ap-northeast-1.rds.amazonaws.com',
        db='nakagawa',
        charset="utf8",
        autocommit=True
        )
        self.connecter.start()
        self.bluesrice = 0
        self.redsrice = 0
        self.bot = bot
        self.recruitid = 1
        self.blue_warrior = []
        self.blue_lucky_warrior = []
        self.orange_warrior = []
        self.orange_lucky_warrior= []
        self.count = 0
        self.already = {}
        self.recruitm = None
        self.blue_teamname = None
        self.orange_teamname = None
        self.tsugumiemoji = self.bot.get_emoji(746675506111578152)
        self.reinaemoji = self.bot.get_emoji(746675764556201984)

    @tasks.loop(hours=4.0)
    async def connecter(self):
        self.conn.close()
        self.conn = MySQLdb.connect(
        user='admin',
        passwd='OZmLQi6yXjvtmLvuKJWB',
        host='nakagawa.cgfmfgfg5hjd.ap-northeast-1.rds.amazonaws.com',
        db='nakagawa',
        charset="utf8",
        autocommit=True
        )

    @commands.command()
    async def emoji(self,ctx):
        await ctx.send(self.tsugumiemoji)
    
    @commands.command()
    async def hime(self, ctx, bluesrice: int, orangesrice: int, teamname_b = "つぐみ軍", teamname_o = "れいな郡"):
        if ctx.author.guild_permissions.administrator or ctx.message.guild.get_role(741998241989525575) in ctx.message.author.roles:
            self.blue_warrior.clear()#抽選参加プレイヤーをクリア
            self.orange_warrior.clear()#当選者のリセット
            self.bluesrice = bluesrice
            self.orange_lucky_warrior.clear()
            self.blue_lucky_warrior.clear()
            self.orangesrice = orangesrice
            self.blue_teamname = teamname_b
            self.orange_teamname = teamname_o
            #print(f"COUNT IS {count} class count is {self.count}")
            recruit = await ctx.channel.send("カスタムマッチの募集を始めます\n参加したい人は👍を押してください\n参加をキャンセルする場合は❌を推してください\n現在の参加プレイヤー数:**0**")
            self.recruitm = recruit
            nrecruitid = recruit.id
            self.recruitid = nrecruitid
            await recruit.add_reaction("🇹")
            await recruit.add_reaction("🇷")
            await recruit.add_reaction("❌")
            def check(reaction, user):
                return user.guild_permissions.administrator == True and reaction.message.id == self.recruitid and str(reaction.emoji) == '✅' or user.guild_permissions.administrator == True and reaction.message.id == self.recruitid and str(reaction.emoji) == '🔚' or user.guild.get_role(741998241989525575) in reaction.message.author.guild.roles and reaction.message.id == self.recruitid and str(reaction.emoji) == '✅' or user.guild.get_role(741998241989525575) in reaction.message.author.guild.roles and reaction.message.id == self.recruitid  and str(reaction.emoji) == '🔚'  
                #もしつけられたリアクションが✅か🔚だったというcheck関数
            try:
                reaction, member = await self.bot.wait_for('reaction_add', check=check)
                #つけられたリアクションが✅か🔚なら
            except asyncio.TimeoutError:
                #タイムアウトした場合の処理
                return
            else:
                #それ以外の場合(つけられたリアクションが✅か🔚の場合)
                if str(reaction) == '✅':#つけられたリアクションが✅ならチーム分け
                    c = self.conn.cursor()
                    await ctx.channel.send('募集を締め切り、チーム分けを行います')#チーム分けをするというメッセージ
                    print(bluesrice, orangesrice)
                    print(f"ブルー抽選ID:{self.blue_warrior}")
                    print(f"オレンジ抽選ID:{self.orange_warrior}")
                    random.shuffle(self.blue_warrior)#参加しているプレイヤーが入っているリストをシャッフル
                    random.shuffle(self.orange_warrior)
                    #プレイヤーの中に先生とれいなさんを入れる処理
                    #つぐみ
                    self.blue_warrior.insert(0, 268024006970441735)
                    print(self.blue_warrior)
                    #れいな
                    self.orange_warrior.insert(0, 292271311705866241)
                    print(self.orange_warrior)
                    for i in self.blue_warrior[:bluesrice]:#チームごとの人数+
                        print(f"For{i}")
                        sql = f"SELECT ign from playerdata WHERE id='{i}';"#当選したプレイヤーの名前からidを入手
                        c.execute(sql)#sqlを実行
                        did = c.fetchone()[0]#ignを代入
                        self.blue_lucky_warrior.append(did) 
                    blue = self.blue_lucky_warrior#シャッフルしたリストの中からself.sriceというチームごとの人数が入った変数を使ってスライス
                    for i in self.orange_warrior[:orangesrice]:
                        print(f"Foro{i}")
                        sql = f"SELECT ign from playerdata WHERE id='{i}';"#当選したプレイヤーの名前からidを入手
                        c.execute(sql)#sqlを実行
                        did = c.fetchone()[0]#ignを代入
                        self.orange_lucky_warrior.append(did)
                    orange = self.orange_lucky_warrior
                    # for playerid in self.players[:bluesrice+orangesrice]:#当選したプレイヤー10人の名前をスライスでfor入
                    #     self.already[playerid] = +1#辞書"already"に当選したプレイヤーのid+プレイ回数+1を追加（何回休み家のシステムのため）
                    print(f"Blue:{blue}")#ブルーチーム
                    print(f"Orange:{orange}")#オレンジチーム
                    bjoin = '\n'.join(blue)
                    ojoin = '\n'.join(orange)
                    print(bjoin)
                    print(ojoin)
                    embed=discord.Embed(title="Team", color=0xffffff)
                    embed.add_field(name=teamname_b, value=f"```\n{bjoin}```", inline=False)#Blueチームにjoinで改行しながらリストblueを入れる
                    embed.add_field(name=teamname_o, value=f"```\n{ojoin}```", inline=False)#orangeチームにjoinで改行しながらリストorangeを入れる
                    await ctx.channel.send(embed=embed)#チーム分けを送信
                    c.close()
                elif str(reaction) == '🔚':#つけられたリアクションが🔚の場合
                    await ctx.channel.send("募集をキャンセルします")
        else:
            await ctx.channel.send("管理者のみ使用可能です")


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        guild = reaction.message.guild
        if user.id == 731483416163516486:
            #print("It's bot")
            return
        # elif str(reaction.emoji) != '👍' and str(reaction.emoji) != '❌':
        #     #print("Not this reaction")
        #     return
        elif self.recruitid != reaction.message.id:
            #print(f"messageid:{self.recruitid} != reactionid:{reaction.message.id}")
            #print("not this massage")
            return
        elif str(reaction.emoji) == '❌':   
            #print("Cancel:❌")
            if user.id in self.orange_warrior:
                self.orange_warrior.remove(user.id)
                await self.recruitm.edit(content=f"カスタムマッチの募集を始めます\n参加したい人は👍を押してください\n参加をキャンセルする場合は❌を押してください\n現在の{self.blue_teamname}参加プレイヤー数:**{len(self.blue_warrior)}**\n現在の{self.orange_teamname}参加プレイヤー数:**{len(self.orange_warrior)}**")
            elif user.id in self.blue_warrior:
                self.blue_warrior.remove(user.id)
                #recruitmessage = await reaction.message.channel.fetch_message(self.recruitid)
                await self.recruitm.edit(content=f"カスタムマッチの募集を始めます\n参加したい人は👍を押してください\n参加をキャンセルする場合は❌を押してください\n現在の{self.blue_teamname}参加プレイヤー数:**{len(self.blue_warrior)}**\n現在の{self.orange_teamname}参加プレイヤー数:**{len(self.orange_warrior)}**")
                try:
                    await user.send('参加を取り消しました')
                except discord.errors.Forbidden:
                    print(f"Failed to send cancel message Name:{user.name}")
            else:
                await user.send("参加していないためキャンセルできませんでした")
            for mreaction in reaction.message.reactions:
                await mreaction.remove(user)
        elif str(reaction.emoji) == str("🇹") or str(reaction.emoji) == str("🇷"):
            print("Add a warrior")
            userid = user.id
            if userid not in self.already:
                self.already[userid] = 0
            c = self.conn.cursor()
            sql = f"SELECT COUNT(1) FROM playerdata WHERE id = {int(userid)}"
            c.execute(sql)
            if c.fetchone()[0]:
                print("FETCH")
                if str(reaction.emoji) == str("🇹"):
                    self.blue_warrior.append(userid)
                    await self.recruitm.edit(content=f"カスタムマッチの募集を始めます\n参加したい人は👍を押してください\n参加をキャンセルする場合は❌を押してください\n現在の{self.blue_teamname}参加プレイヤー数:**{len(self.blue_warrior)}**\n現在の{self.orange_teamname}参加プレイヤー数:**{len(self.orange_warrior)}**")
                    player = guild.get_member(userid)
                    print(f"Add player:{userid} NAME:{player.name}")
                elif str(reaction.emoji) == str("🇷"):
                    self.orange_warrior.append(userid)
                    await self.recruitm.edit(content=f"カスタムマッチの募集を始めます\n参加したい人は👍を押してください\n参加をキャンセルする場合は❌を押してください\n現在の{self.blue_teamname}参加プレイヤー数:**{len(self.blue_warrior)}**\n現在の{self.orange_teamname}参加プレイヤー数:**{len(self.orange_warrior)}**")
                    player = guild.get_member(userid)
                    print(f"Add player:{userid} NAME:{player.name}")
                if userid in self.blue_warrior or userid in self.orange_warrior:
                    print("You already joined")
                    return
                c.close()
            else:
                await user.create_dm()
                dmid = user.dm_channel.id
                await reaction.remove(user)
                try:
                    await user.send("**UplayID**が未登録です。\n**UplayID**を送信してください\nまた**__IDを送信したあとに募集のメッセージにもう一度リアクションをつけてください__**")
                except discord.errors.Forbidden:
                    print(f"Failed to send message {user.id}Name:{user.name}")
                print(f"Send to message {userid}")
                await user.create_dm()
                def check(m):
                    return userid == m.author.id and dmid == m.channel.id
                try:
                    msg = await self.bot.wait_for('message', check=check, timeout = 60)
                except asyncio.TimeoutError:
                    await user.send('タイムアウトしました\nbotがメッセージ送信されてから60秒以内にIDを送ってください')
                else:
                    sql = f'select id from playerdata where id = {userid}'
                    c.execute(sql)
                    uplayids = c.fetchall()
                    print(uplayids)
                    if len(uplayids) > 0:
                        await user.send("既に登録されています")
                        return
                    else:
                        sql = 'insert into playerdata values (%s, %s)'
                        c.execute(sql, (msg.author.id, msg.content))#(msg.author.id, msg.content)
                        c.close()
                        print(f"Register player Name:{msg.content}")
                        await user.send(f"UplayIDを:**{msg.content}**で登録しました")


def setup(bot):
     bot.add_cog(hime(bot))