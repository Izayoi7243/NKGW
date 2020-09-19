from discord.ext import tasks, commands
import discord
import random

class randommap(commands.Cog):
    def __init__(self, bot):
        print("Map is loaded")


    @commands.command()
    async def randommap(self, ctx, maptype):
        eslmapsdic = {
            'クラブハウス':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/1vCw5eD2XzxZlv6Au1gtui/a173a37999379b65dad7b37a77c24498/r6-maps-clubhouse.jpg',
            'カフェ・ドストエフスキー':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/2nIuPSHvbM57TK90VSwBEm/70144ada56cf1ba72103aeb4ece9ed1a/r6-maps-kafe.jpg',
            '領事館':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/6PR2sBla9E6TNurVUfJ0mc/860cab16eb1d4cd27ea356a1c3fe9591/r6-maps-consulate.jpg',
            '国境':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/4hqsrL3cokFqedkfjiEaGf/b91bc482243b56531f999912de6d0bcb/r6-maps-border.jpg',
            '海岸線':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/5GfAQ3pXCJnDqiqaDH3Zic/2a491e0c4c184c28a88792d85279e551/r6-maps-coastline.jpg',
            'テーマパーク':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/2immPCOZj6tTHMM9zeBg5B/cf09c9c75bc2e70dd38ebf0a12bdb9a2/r6-maps-themepark.jpg',
            'ヴィラ':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/Io6dxNeHbCbJoF9WLJf9s/ebf89b009affba37df84dcf1934c74e0/r6-maps-villa.jpg'
        }
        rankmapdic = {
            '銀行':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/6ilgtuzucX7hEu2MvjhRtp/04d41f0066cc9d0ca26d1fea27577ce4/r6-maps-bank_352520.jpg',
            '国境':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/4hqsrL3cokFqedkfjiEaGf/b91bc482243b56531f999912de6d0bcb/r6-maps-border.jpg',
            '山荘':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/Km3ZJUM7ZMVbGsi6gad5Y/c48162371342d9f15386c77a3766315b/r6-maps-chalet.jpg',
            'クラブハウス':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/1vCw5eD2XzxZlv6Au1gtui/a173a37999379b65dad7b37a77c24498/r6-maps-clubhouse.jpg',
            '海岸線':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/5GfAQ3pXCJnDqiqaDH3Zic/2a491e0c4c184c28a88792d85279e551/r6-maps-coastline.jpg',
            '領事館':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/6PR2sBla9E6TNurVUfJ0mc/860cab16eb1d4cd27ea356a1c3fe9591/r6-maps-consulate.jpg',
            'カフェ・ドストエフスキー':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/2nIuPSHvbM57TK90VSwBEm/70144ada56cf1ba72103aeb4ece9ed1a/r6-maps-kafe.jpg',
            '運河':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/4VHR8uZRGkHqvtZxtmibtc/da988c2cab37f1cb186535fc9ba40bea/r6-maps-kanal.jpg',
            'オレゴン':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/Z9a0gU7iR0vfcbXtoJUOW/42ad6aabbd189fbcd74c497627f1624e/r6-maps-oregon.jpg',
            'アウトバック':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/1vqGVW6pqBZlLKp4h86NnB/e40a67fd2d88aa6434d96e2e0f2965e3/r6-maps-outback.jpg',
            'テーマパーク':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/2immPCOZj6tTHMM9zeBg5B/cf09c9c75bc2e70dd38ebf0a12bdb9a2/r6-maps-themepark.jpg',
            'ヴィラ':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/Io6dxNeHbCbJoF9WLJf9s/ebf89b009affba37df84dcf1934c74e0/r6-maps-villa.jpg'
        }
        allmapdic = {
            '銀行':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/6ilgtuzucX7hEu2MvjhRtp/04d41f0066cc9d0ca26d1fea27577ce4/r6-maps-bank_352520.jpg',
            '国境':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/4hqsrL3cokFqedkfjiEaGf/b91bc482243b56531f999912de6d0bcb/r6-maps-border.jpg',
            '山荘':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/Km3ZJUM7ZMVbGsi6gad5Y/c48162371342d9f15386c77a3766315b/r6-maps-chalet.jpg',
            'クラブハウス':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/1vCw5eD2XzxZlv6Au1gtui/a173a37999379b65dad7b37a77c24498/r6-maps-clubhouse.jpg',
            '海岸線':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/5GfAQ3pXCJnDqiqaDH3Zic/2a491e0c4c184c28a88792d85279e551/r6-maps-coastline.jpg',
            '領事館':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/6PR2sBla9E6TNurVUfJ0mc/860cab16eb1d4cd27ea356a1c3fe9591/r6-maps-consulate.jpg',
            'ファベーラ':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/5x991vPOlYbFlynxn9tmn8/df3368e4b798324b6572d592e8ab8cf4/r6-maps-favela.jpg',
            '要塞':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/1MrLwvq61aSSvvUj3dDiZg/18e267c79b8015a1af509a2e5694b18b/r6-maps-fortress.jpg',
            'ヘレフォード基地':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/1QHhMYSliWgWXFLxZj19hz/44197c1d98498d8a77618076a19ce538/r6-maps-hereford.jpg',
            '民家':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/28OaEZAY3stNFr0wSvW9MB/a4f22d216af3054380fccb7e172d8f5f/r6-maps-house.jpg',
            'カフェ・ドストエフスキー':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/2nIuPSHvbM57TK90VSwBEm/70144ada56cf1ba72103aeb4ece9ed1a/r6-maps-kafe.jpg',
            '運河':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/4VHR8uZRGkHqvtZxtmibtc/da988c2cab37f1cb186535fc9ba40bea/r6-maps-kanal.jpg',
            'オレゴン':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/Z9a0gU7iR0vfcbXtoJUOW/42ad6aabbd189fbcd74c497627f1624e/r6-maps-oregon.jpg',
            'アウトバック':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/1vqGVW6pqBZlLKp4h86NnB/e40a67fd2d88aa6434d96e2e0f2965e3/r6-maps-outback.jpg',
            '大統領専用機':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/3YSN2V0HWsddcQq82Iqihn/d3e03012e8909be26f8274b7f9b3bf19/r6-maps-plane.jpg',
            '高層ビル':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/7vblsbhmSPLsI3pQJ5Dqx9/669192088ad875a24f6f8c24a6ba2247/r6-maps-skyscraper.jpg',
            'テーマパーク':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/2immPCOZj6tTHMM9zeBg5B/cf09c9c75bc2e70dd38ebf0a12bdb9a2/r6-maps-themepark.jpg',
            'タワー':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/6ZMBunxANmzTNr42wwzggb/3a19c506f9e3f910e34da21095686fa9/r6-maps-tower.jpg',
            'ヴィラ':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/Io6dxNeHbCbJoF9WLJf9s/ebf89b009affba37df84dcf1934c74e0/r6-maps-villa.jpg',
            'ヨット':'https://staticctf.akamaized.net/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/smDP6lSSaB6Daa7bLZxHZ/d6cc60d76e553e91503a474ff0bc148b/r6-maps-yacht.jpg'
        }
        if maptype == 'esl':
            mappool = eslmapsdic
        elif maptype == 'rank':
            mappool = rankmapdic
        elif maptype == 'all':
            mappool = allmapdic
        elif maptype in allmapdic.keys():
            embed=discord.Embed(title=maptype)
            embed.set_image(url=allmapdic[maptype])
            await ctx.send(embed=embed)
            return
        else:
            await ctx.send(f"マッププール**{maptype}**はありません")
            return
        randommapname, mapurl = random.choice(list(mappool.items()))
        embed=discord.Embed(title=randommapname)
        embed.set_image(url=mapurl)
        await ctx.send(embed=embed)

def setup(bot):
     bot.add_cog(randommap(bot))