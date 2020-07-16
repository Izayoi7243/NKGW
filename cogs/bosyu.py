from discord.ext import commands
import discord
import asyncio
import random
import MySQLdb





class bosyu(commands.Cog):
    def __init__(self, bot):
        self.conn = MySQLdb.connect(
        user='admin',
        passwd='OZmLQi6yXjvtmLvuKJWB',
        host='nakagawa.cgfmfgfg5hjd.ap-northeast-1.rds.amazonaws.com',
        db='nakagawa',
        charset="utf8",
        autocommit=True
        )
        self.bot = bot
        self.recruitid = 1
        self.players = []
        self.lucky = []
        self.count = 0
        self.already = {}
        self.srice = 0

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
        c = self.conn.cursor()
        sql = f'select ign from playerdata where id = {ctx.author.id}'#名前を取得
        c.execute(sql)
        await ctx.send(f"あなたのUplayIDは **{c.fetchone()[0]}** です")
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
            await ctx.send("IDが登録されていません\nregisterコマンドで設定してください\n例```n!register id```")



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
        else:
            ctx.channel.send("このコマンドは管理者のみ使用可能です")

    @commands.command()
    async def resetplay(self, ctx):
        if ctx.author.guild_permissions.administrator:
            self.already.clear()
        else:
            ctx.channel.send("このコマンドは管理者のみ使用可能です")

    
    @commands.command()
    async def start(self, ctx, srice: int, count=0):
        if ctx.author.guild_permissions.administrator:      
            if count == 0:
                self.count = 0
            else:
                self.count = count
            print(f"COUNT IS {count} class count is {self.count}")
            recruit = await ctx.channel.send("カスタムマッチの募集を始めます\n参加したい人は👍を押してください\n参加をキャンセルする場合は❌を推してください")
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
                    print(f"srice = {srice}")
                    self.srice = int(srice)      
                    blue = self.players[:self.srice]#シャッフルしたリストの中からself.sriceというチームごとの人数が入った変数を使ってスライス
                    orange = self.players[self.srice:self.srice*2]
                    for ign in self.players[:10]:#当選したプレイヤー10人の名前をスライスでfor
                        sql = f"SELECT id from playerdata WHERE ign='{ign}';"#当選したプレイヤーの名前からidを入手
                        c.execute(sql)#sqlを実行
                        did = c.fetchone()#idを代入
                        self.already[did[0]] = +1#辞書"already"に当選したプレイヤーのid+プレイ回数+1を追加（何回休み家のシステムのため）
                    print(blue)#ブルーチーム
                    print(orange)#オレンジチーム
                    embed=discord.Embed(title="Team", color=0xffffff)
                    embed.add_field(name="Blue", value='\n'.join(blue), inline=False)#Blueチームにjoinで改行しながらリストblueを入れる
                    embed.add_field(name="Orange", value='\n'.join(orange), inline=False)#orangeチームにjoinで改行しながらリストorangeを入れる
                    await ctx.channel.send(embed=embed)#チーム分けを送信
                    self.srice = 0#チーム分けの人数をリセット
                    self.players.clear()#抽選参加プレイヤーをクリア
                    c.close()
                elif str(reaction) == '🔚':#つけられたリアクションが🔚の場合
                    ctx.channel.send("募集をキャンセルします")
        else:
            await ctx.channel.send("管理者のみ使用可能です")

    @commands.command()
    async def playerlist(self, ctx):
        embed=discord.Embed(title="Players", color=0xffffff)
        embed.add_field(name="All", value='\n'.join(self.players), inline=False)
        try:
            await ctx.channel.send(embed=embed)
        except discord.ext.commands.errors.CommandInvokeError:
            await ctx.channel.send("Playerlist is Empty")

    @start.error#スタートコマンドのエラーハンドリング
    async def start_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):#引数が足りないエラー
            await ctx.send("チームごとの人数を指定してください\n**例**\n```n!start 5```")
        if isinstance(error, commands.errors.CommandInvokeError):#埋め込みに入れる要素がないときのエラー
            await ctx.send("参加プレイヤーが足りません")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
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
            c = self.conn.cursor()
            sql = f"SELECT ign from playerdata WHERE id='{user.id}';"
            c.execute(sql)
            ign = c.fetchall()[0][0]
            if ign in self.players:
                self.players.remove(ign)
            await user.send('参加を取り消しました')
            await reaction.remove(user)
            c.close()
        else:
            print("Correct Reaciton:👍")
            userid = user.id
            if userid not in self.already:
                self.already[userid] = 0
                print(self.already)
            c = self.conn.cursor()
            sql = f"SELECT COUNT(1) FROM playerdata WHERE id = {int(userid)}"
            c.execute(sql)
            if c.fetchone()[0]:
                print(f"COUNT IS {self.count}!!!!!!!!!!!!!!")
                if 1 <= self.already[userid] <= self.count:
                    await user.send(f"一度参加したため参加できません\nあと**{self.count}マッチ後**に参加できます※参加できるまで配信が続くかはわかりません")#参加した回数1
                    return
                sql = f"SELECT ign from playerdata WHERE id='{user.id}';"
                c.execute(sql)
                ign = c.fetchall()[0][0]
                if ign in self.players:
                    print("You already joined")
                    return
                print("YET")
                print(ign)
                await user.send("参加を受け付けました")
                self.players.append(ign)
                c.close()
            else:
                print(f"Sent message to {userid}")
                reactionuser = self.bot.get_user(userid)
                await reactionuser.create_dm()
                dmid = reactionuser.dm_channel.id
                await reaction.remove(user)
                await reactionuser.send("**UplayID**が未登録です。\n**UplayID**を送信してください\nまた**__IDを送信したあとに募集のメッセージにもう一度リアクションをつけてください__**")
                await reactionuser.create_dm()
                def check(m):
                    return userid == m.author.id and dmid == m.channel.id
                try:
                    msg = await self.bot.wait_for('message', check=check, timeout = 60)
                except asyncio.TimeoutError:
                    await reactionuser.send('タイムアウトしました')
                else:
                    sql = 'insert into playerdata values (%s, %s)'
                    c.execute(sql, (msg.author.id, msg.content))#(msg.author.id, msg.content)
                    sql = 'select * from playerdata;'
                    c.execute(sql)
                    print(c.fetchall())
                    c.close()
                    await reactionuser.send(f"UplayIDを:**{msg.content}**で登録しました")


def setup(bot):
     bot.add_cog(bosyu(bot))