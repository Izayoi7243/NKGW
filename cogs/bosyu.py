from discord.ext import commands
import discord
import asyncio
import random
import MySQLdb





class bosyu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.recruitid = 1
        self.players = []
        self.lucky = []
        self.count = 0
        self.already = {}
        self.srice = 0

    @commands.command()
    async def changeid(self, ctx, newid):
    #id変更コマンド
        conn = MySQLdb.connect(
        user='admin',
        passwd='OZmLQi6yXjvtmLvuKJWB',
        host='nakagawa.cgfmfgfg5hjd.ap-northeast-1.rds.amazonaws.com',
        db='nakagawa',
        charset="utf8"
        )
        c = conn.cursor()
        sql = 'delete from playerdata where id=%s'
        c.execute(sql, (ctx.author.id,))
        sql = 'insert into playerdata values (%s, %s)'
        c.execute(sql, (ctx.author.id, newid))
        await ctx.channel.send(f"UplayIDを:**{newid}**にしました")
        conn.commit()
        c.close()
        conn.close()
    
    @commands.command()
    async def resetall(self, ctx, usage="このコマンドは、何らかの事情で募集コマンドをやり直したいときに使ってください※管理者のみ使用可能"):
        if ctx.author.guild_permissions.administrator:
            self.already.clear()
            self.players.clear()
            self.lucky.clear()
        else:
            ctx.channel.send("このコマンドは管理者のみ使用可能です")

    @commands.command()
    async def resetplay(self, ctx, help="すでに参加したプレイヤーのプレイ数をリセット※管理者のみ使用可能"):
        if ctx.author.guild_permissions.administrator:
            self.already.clear()
        else:
            ctx.channel.send("このコマンドは管理者のみ使用可能です")

    
    @commands.command()
    async def start(self, ctx, srice: int, *args: str,help="使用方法\n```n!start <チームごとの人数> <一度参加したプレイヤーが何回休むか**省略した場合は0になります**>"):
        if ctx.author.guild_permissions.administrator:      
            if len(args) <= 1:
                print(f"count = {args[0]}")
                self.count = int(args[0]) 
            recruit = await ctx.channel.send("カスタムマッチの募集を始めます\n参加したい人は👍を押してください")
            nrecruitid = recruit.id
            self.recruitid = nrecruitid
            await recruit.add_reaction("👍")
            def check(reaction, user):
                return user.guild_permissions.administrator == reaction.message.author.guild_permissions.administrator and str(reaction.emoji) == '🔚'
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check)
            except asyncio.TimeoutError:
                return
            else:
                conn = MySQLdb.connect(
                user='admin',
                passwd='OZmLQi6yXjvtmLvuKJWB',
                host='nakagawa.cgfmfgfg5hjd.ap-northeast-1.rds.amazonaws.com',
                db='nakagawa',
                charset="utf8"
                )
                c = conn.cursor()
                await ctx.channel.send('募集を締め切り、チーム分けを行います')
                print(f"参加済み:{self.players}")
                random.shuffle(self.players)
                print(len(args))
                print(f"srice = {srice}")
                self.srice = int(srice)      
                blue = self.players[:self.srice]#:-5
                orange = self.players[self.srice:self.srice*2]#5:
                for ign in self.players[:10]:
                    sql = f"SELECT id from playerdata WHERE ign='{ign}';"
                    c.execute(sql)
                    did = c.fetchone()
                    self.already[did[0]] = +1
                print(blue)
                print(orange)
                embed=discord.Embed(title="Team", color=0xffffff)
                embed.add_field(name="Blue", value='\n'.join(blue), inline=False)
                embed.add_field(name="Orange", value='\n'.join(orange), inline=False)
                await ctx.channel.send(embed=embed)
                self.srice = 1
                self.players.clear()
        else:
            await ctx.channel.send("管理者のみ使用可能です")

    @commands.command()
    async def playerlist(self, ctx,help="抽選に参加しているプレイヤーのリスト※誰でも使用可能"):
        embed=discord.Embed(title="Players", color=0xffffff)
        embed.add_field(name="All", value='\n'.join(self.players), inline=False)
        try:
            await ctx.channel.send(embed=embed)
        except discord.ext.commands.errors.CommandInvokeError:
            await ctx.channel.send("Playerlist is Empty")

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
            conn = MySQLdb.connect(
            user='admin',
            passwd='OZmLQi6yXjvtmLvuKJWB',
            host='nakagawa.cgfmfgfg5hjd.ap-northeast-1.rds.amazonaws.com',
            db='nakagawa',
            charset="utf8"
            )
            c = conn.cursor()
            sql = f"SELECT ign from playerdata WHERE id='{user.id}';"
            c.execute(sql)
            ign = c.fetchall()[0][0]
            if ign in self.players:
                self.players.remove(ign)
            await user.send('参加を取り消しました')
            conn.commit()
            c.close()
            conn.close()
        else:
            print("Correct Reaciton:👍")
            userid = user.id
            if userid not in self.already:
                self.already[userid] = 0
                print(self.already)
            conn = MySQLdb.connect(
            user='admin',
            passwd='OZmLQi6yXjvtmLvuKJWB',
            host='nakagawa.cgfmfgfg5hjd.ap-northeast-1.rds.amazonaws.com',
            db='nakagawa',
            charset="utf8"
            )
            c = conn.cursor()
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
                conn.close()
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
                    conn.commit()
                    c.close()
                    conn.close()
                    await reactionuser.send(f"UplayIDを:**{msg.content}**で登録しました")


def setup(bot):
     bot.add_cog(bosyu(bot))