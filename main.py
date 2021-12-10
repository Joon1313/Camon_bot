import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import discord
from discord.ext import commands
import re
import pymysql
import time
import os
load_dotenv()

# camon_db = pymysql.connect(
#     user=os.environ.get('USER'),
#     passwd=os.environ.get('PASSWD'),
#     host=os.environ.get('HOST'),
#     db=os.environ.get('DB'),
#     charset=os.environ.get('CHARSET')
# )
# cursor = camon_db.cursor(pymysql.cursors.DictCursor)
app = commands.Bot(command_prefix='.')

def created_log(name, command):
    if str(name) == '깜언#1577':
        return
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    data = (name, date, command)
    sql = "INSERT INTO `log` (name, created,command) VALUES (%s, %s, %s);"
    # cursor.execute(sql, data)
    # camon_db.commit()

@app.event
async def on_ready():
    await app.change_presence(status=discord.Status.online, activity=None)

@app.command()
async def 검색(ctx, *, name):
    url = f"https://lostark.game.onstove.com/Profile/Character/{name}"
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser')
    # 아이템 레벨
    try:
        level = soup.select_one(
            '#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info2 > div.level-info2__expedition > span:nth-child(2)').get_text()
    except:
        await ctx.send('캐릭터를 찾을수 없습니다')
        return
    # 길드
    guild = soup.select_one(
        '#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.game-info > div.game-info__guild > span:nth-child(2)').get_text()
    # 영지 레벨
    expedition_level = soup.select_one(
        '#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info > div.level-info__expedition > span:nth-child(2)').get_text()
    # 전투 레벨
    battle_level = soup.select_one(
        '#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info > div.level-info__item > span:nth-child(2)').get_text()
    # 클래스
    class_name = soup.select_one(
        '#lostark-wrapper > div > main > div > div.profile-character-info > img')
    # 공격력
    attack = soup.select_one(
        '#profile-ability > div.profile-ability-basic > ul > li:nth-child(1) > span:nth-child(2)').get_text()
    # 치명
    stat_1 = soup.select_one(
        '#profile-ability > div.profile-ability-battle > ul > li:nth-child(1) > span:nth-child(2)').get_text()
    # 특화
    stat_2 = soup.select_one(
        '#profile-ability > div.profile-ability-battle > ul > li:nth-child(2) > span:nth-child(2)').get_text()
    # 제압
    stat_3 = soup.select_one(
        '#profile-ability > div.profile-ability-battle > ul > li:nth-child(3) > span:nth-child(2)').get_text()
    # 신속
    stat_4 = soup.select_one(
        '#profile-ability > div.profile-ability-battle > ul > li:nth-child(4) > span:nth-child(2)').get_text()
    # 인내
    stat_5 = soup.select_one(
        '#profile-ability > div.profile-ability-battle > ul > li:nth-child(5) > span:nth-child(2)').get_text()
    # 숙련
    stat_6 = soup.select_one(
        '#profile-ability > div.profile-ability-battle > ul > li:nth-child(6) > span:nth-child(2)').get_text()

    skill = soup.select('#profile-ability > div.profile-ability-engrave > div > div.swiper-wrapper li')

    embed = discord.Embed(title=f"***[{name}] 캐릭터 정보***", description="`.검색 캐릭터명`", color=0xAAFFFF)
    embed.add_field(name='아이템 레벨', value=f"`{level[3:]}`", inline=True)
    embed.add_field(name='클래스', value=f"`{class_name['alt']}`", inline=True)
    embed.add_field(name='길드명', value=f"`{guild}`", inline=True)
    embed.add_field(name='전투 레벨', value=f"`{battle_level}`", inline=True)
    embed.add_field(name='원정대 레벨', value=f"`{expedition_level}`", inline=True)
    embed.add_field(name='공격력', value=f'`{attack}`', inline=True)
    embed.add_field(name='\u200B', value=f"> ***[전투 특성]***", inline=False)
    embed.add_field(name='치명', value=f"`{stat_1}`", inline=True)
    embed.add_field(name='특화', value=f"`{stat_2}`", inline=True)
    embed.add_field(name='제압', value=f"`{stat_3}`", inline=True)
    embed.add_field(name='신속', value=f"`{stat_4}`", inline=True)
    embed.add_field(name='인내', value=f"`{stat_5}`", inline=True)
    embed.add_field(name='숙련', value=f"`{stat_6}`", inline=True)
    skill_name = []
    for i in skill:
        skill_name.append(f"`{i.select_one('span').get_text()}`\n")
    skill_name = "".join(skill_name)
    embed.add_field(name="> ***[각인 효과]***\n", value=skill_name, inline=False)
    embed.set_thumbnail(url="https://i.imgur.com/X5ECwa0.png")
    embed.set_footer(text="명령어) .도움말", icon_url="https://i.imgur.com/X5ECwa0.png")
    created_log(name=ctx.author, command='검색')
    await ctx.send(embed=embed)

@app.command()
async def 오페별(ctx, *, name):
    answer = []
    answer2 = []
    url = f"https://lostark.game.onstove.com/Profile/Character/{name}"
    url2 = "https://lostark.game.onstove.com/Profile/GetCollection"
    res = requests.get(url).text
    soup = BeautifulSoup(res, 'html.parser')
    # 아이템 레벨
    try:
        level = soup.select_one(
            '#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info2 > div.level-info2__expedition > span:nth-child(2)').get_text()
    except:
        await ctx.send('캐릭터를 찾을수 없습니다')
        return

    pcid = r"var _pcId = '(.+?)';"
    pcid = re.search(pcid, res, re.S).group(1)
    memberno = r"var _memberNo = '(.+?)';"
    memberno = re.search(memberno, res, re.S).group(1)
    worldno = r"var _worldNo = '(.+?)';"
    worldno = re.search(worldno, res, re.S).group(1)
    data = {
        'pcid': pcid,
        'memberno': memberno,
        'worldno': worldno,
    }
    res2 = requests.post(url2, data=data).text
    soup = BeautifulSoup(res2, 'html.parser')
    star_list = soup.select(
        '#lui-tab1-2 > div > div.collection-list > ul > li')
    status = soup.select_one(
        '#lui-tab1-2 > div > div.collection-list > div > p').get_text()
    for i in star_list:
        if "획득" in i.get_text():
            answer.append(f"`{i.get_text()[1:12]}`\n")
        else:
             answer2.append(f"`{i.get_text()[1:12]}`\n")
    answer = "".join(answer)
    answer2 = "".join(answer2)
    if answer == "":
        answer = '획득한 오르페우스 별이 없습니다.'
    if answer2 == "":
        answer2 = '오르페우스 별을 모두 획득하였습니다.'
    embed = discord.Embed(title=f"[{name}] 오르페우스의 별 획득 현황", description=f"{status}", color=0xAAFFFF)
    embed.add_field(name='> 획득', value=answer, inline=True)
    embed.add_field(name='> 미획득', value=answer2, inline=True)
    embed.set_thumbnail(url="https://i.imgur.com/X5ECwa0.png")
    embed.set_footer(text="명령어) .도움말", icon_url="https://i.imgur.com/X5ECwa0.png")
    created_log(name=ctx.author, command='오페별')
    await ctx.send(embed=embed)

@app.command()
async def 거심(ctx, *, name):
    answer = []
    answer2 = []
    url = f"https://lostark.game.onstove.com/Profile/Character/{name}"
    url2 = "https://lostark.game.onstove.com/Profile/GetCollection"
    res = requests.get(url).text
    soup = BeautifulSoup(res, 'html.parser')
    # 아이템 레벨
    try:
        level = soup.select_one(
            '#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info2 > div.level-info2__expedition > span:nth-child(2)').get_text()
    except:
        await ctx.send('캐릭터를 찾을수 없습니다')
        return

    pcid = r"var _pcId = '(.+?)';"
    pcid = re.search(pcid, res, re.S).group(1)
    memberno = r"var _memberNo = '(.+?)';"
    memberno = re.search(memberno, res, re.S).group(1)
    worldno = r"var _worldNo = '(.+?)';"
    worldno = re.search(worldno, res, re.S).group(1)
    data = {
        'pcid': pcid,
        'memberno': memberno,
        'worldno': worldno,
    }
    res2 = requests.post(url2, data=data).text
    soup = BeautifulSoup(res2, 'html.parser')
    Heart_list = soup.select(
        '#lui-tab1-3 > div > div.collection-list > ul > li')
    status = soup.select_one(
        '#lui-tab1-3 > div > div.collection-list > div > p').get_text()
    num_del = r'[0-9]+'
    for i in Heart_list:
        if "획득" in i.get_text():
            answer.append(f"`{re.sub(num_del, '', i.get_text())}`\n")
        else:
            answer2.append(f"`{re.sub(num_del, '', i.get_text())}`\n")
    answer = "".join(answer)
    answer2 = "".join(answer2)
    if answer == "":
        answer = '획득한 거인의 심장이 없습니다.'
    if answer2 == "":
        answer2 = '거인의 심장을 모두 획득하였습니다.'
    embed = discord.Embed(title=f"[{name}] 거인의 심장 획득 현황", description=f"{status}", color=0xAAFFFF)
    embed.add_field(name='> 획득', value=answer, inline=True)
    embed.add_field(name='> 미획득', value=answer2, inline=True)
    embed.set_thumbnail(url="https://i.imgur.com/X5ECwa0.png")
    embed.set_footer(text="명령어) .도움말", icon_url="https://i.imgur.com/X5ECwa0.png")
    created_log(name=ctx.author, command='거심')
    await ctx.send(embed=embed)

@app.command()
async def 모코코(ctx, *, name):
    i = 0
    answer = []
    url = f"https://lostark.game.onstove.com/Profile/Character/{name}"
    url2 = "https://lostark.game.onstove.com/Profile/GetCollection"
    res = requests.get(url).text
    soup = BeautifulSoup(res, 'html.parser')
    try:
        level = soup.select_one(
            '#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info2 > div.level-info2__expedition > span:nth-child(2)').get_text()
    except:
        await ctx.send('캐릭터를 찾을수 없습니다')
        return

    pcid = r"var _pcId = '(.+?)';"
    pcid = re.search(pcid, res, re.S).group(1)
    memberno = r"var _memberNo = '(.+?)';"
    memberno = re.search(memberno, res, re.S).group(1)
    worldno = r"var _worldNo = '(.+?)';"
    worldno = re.search(worldno, res, re.S).group(1)
    data = {
        'pcid': pcid,
        'memberno': memberno,
        'worldno': worldno,
    }
    res2 = requests.post(url2, data=data).text
    soup = BeautifulSoup(res2, 'html.parser')
    mococo_list = soup.select(
        '#lui-tab1-5 > div > div.collection-list > ul > li')
    status = soup.select_one(
        '#lui-tab1-5 > div > div.collection-list > div > p').get_text()
    # num_del = r'[0-9]+'
    for v in range(0,len(mococo_list)):
            text = ' '.join(mococo_list[v].get_text().split())
            if v < 9:
                text = text[1:]
            else:
                text = text[2:]
            answer.append(f"`{text}`\n")
    answer = "".join(answer)
    embed = discord.Embed(title=f"[{name}] 모코코 획득 현황", description=f"{status}", color=0xAAFFFF)
    embed.add_field(name='> 지역별 모코코 획득 개수', value=answer, inline=True)
    embed.set_thumbnail(url="https://i.imgur.com/X5ECwa0.png")
    embed.set_footer(text="명령어) .도움말", icon_url="https://i.imgur.com/X5ECwa0.png")
    created_log(name=ctx.author, command='모코코')
    await ctx.send(embed=embed)

@app.command()
async def 미술품(ctx, *, name):
    i = 0
    answer = []
    answer2 = []
    url = f"https://lostark.game.onstove.com/Profile/Character/{name}"
    url2 = "https://lostark.game.onstove.com/Profile/GetCollection"
    res = requests.get(url).text
    soup = BeautifulSoup(res, 'html.parser')
    try:
        level = soup.select_one(
            '#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info2 > div.level-info2__expedition > span:nth-child(2)').get_text()
    except:
        await ctx.send('캐릭터를 찾을수 없습니다')
        return

    pcid = r"var _pcId = '(.+?)';"
    pcid = re.search(pcid, res, re.S).group(1)
    memberno = r"var _memberNo = '(.+?)';"
    memberno = re.search(memberno, res, re.S).group(1)
    worldno = r"var _worldNo = '(.+?)';"
    worldno = re.search(worldno, res, re.S).group(1)
    data = {
        'pcid': pcid,
        'memberno': memberno,
        'worldno': worldno,
    }
    res2 = requests.post(url2, data=data).text
    soup = BeautifulSoup(res2, 'html.parser')
    list = soup.select(
        '#lui-tab1-4 > div > div.collection-list > ul > li')
    status = soup.select_one(
        '#lui-tab1-4 > div > div.collection-list > div > p').get_text()
    for v in range(0,len(list)):
            text = ' '.join(list[v].get_text().split())
            if v < 9:
                text = text[1:]
            else:
                text = text[2:]
            if "획득" in text:
                answer.append(f"`{text}`\n")
            else:
                answer2.append(f"`{text}`\n")
    answer = "".join(answer)
    answer2 = "".join(answer2)
    if answer == "":
        answer = '획득한 위대한 미술품이 없습니다.'
    if answer2 == "":
        answer2 = '위대한 미술품을 모두 획득하였습니다.'
    embed = discord.Embed(title=f"[{name}] 위대한 미술품 획득 현황", description=f"{status}", color=0xAAFFFF)
    embed.add_field(name='> 획득', value=answer, inline=True)
    embed.add_field(name='> 미획득', value=answer2, inline=True)
    embed.set_thumbnail(url="https://i.imgur.com/X5ECwa0.png")
    embed.set_footer(text="명령어) .도움말", icon_url="https://i.imgur.com/X5ECwa0.png")
    created_log(name=ctx.author, command='모코코')
    await ctx.send(embed=embed)

@app.command()
async def 모험물(ctx, *, name):
    i = 0
    answer = []
    answer2 = []
    url = f"https://lostark.game.onstove.com/Profile/Character/{name}"
    url2 = "https://lostark.game.onstove.com/Profile/GetCollection"
    res = requests.get(url).text
    soup = BeautifulSoup(res, 'html.parser')
    try:
        level = soup.select_one(
            '#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info2 > div.level-info2__expedition > span:nth-child(2)').get_text()
    except:
        await ctx.send('캐릭터를 찾을수 없습니다')
        return

    pcid = r"var _pcId = '(.+?)';"
    pcid = re.search(pcid, res, re.S).group(1)
    memberno = r"var _memberNo = '(.+?)';"
    memberno = re.search(memberno, res, re.S).group(1)
    worldno = r"var _worldNo = '(.+?)';"
    worldno = re.search(worldno, res, re.S).group(1)
    data = {
        'pcid': pcid,
        'memberno': memberno,
        'worldno': worldno,
    }
    res2 = requests.post(url2, data=data).text
    soup = BeautifulSoup(res2, 'html.parser')
    list = soup.select(
        '#lui-tab1-6 > div > div.collection-list > ul > li')
    status = soup.select_one(
        '#lui-tab1-6 > div > div.collection-list > div > p').get_text()
    for v in range(0,len(list)):
            text = ' '.join(list[v].get_text().split())
            if v < 9:
                text = text[1:]
            else:
                text = text[2:]
            if "획득" in text:
                answer.append(f"`{text}`\n")
            else:
                answer2.append(f"`{text}`\n")
    answer = "".join(answer)
    answer2 = "".join(answer2)
    if answer == "":
        answer = '획득한 항해 모험물이 없습니다.'
    if answer2 == "":
        answer2 = '항해 모험물을 모두 획득하였습니다.'
    embed = discord.Embed(title=f"[{name}] 항해 모험물 획득 현황", description=f"{status}", color=0xAAFFFF)
    embed.add_field(name='> 획득', value=answer, inline=True)
    embed.add_field(name='> 미획득', value=answer2, inline=True)
    embed.set_thumbnail(url="https://i.imgur.com/X5ECwa0.png")
    embed.set_footer(text="명령어) .도움말", icon_url="https://i.imgur.com/X5ECwa0.png")
    created_log(name=ctx.author, command='모험물')
    await ctx.send(embed=embed)

@app.command()
async def 이그네아(ctx, *, name):
    i = 0
    answer = []
    answer2 = []
    url = f"https://lostark.game.onstove.com/Profile/Character/{name}"
    url2 = "https://lostark.game.onstove.com/Profile/GetCollection"
    res = requests.get(url).text
    soup = BeautifulSoup(res, 'html.parser')
    try:
        level = soup.select_one(
            '#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info2 > div.level-info2__expedition > span:nth-child(2)').get_text()
    except:
        await ctx.send('캐릭터를 찾을수 없습니다')
        return

    pcid = r"var _pcId = '(.+?)';"
    pcid = re.search(pcid, res, re.S).group(1)
    memberno = r"var _memberNo = '(.+?)';"
    memberno = re.search(memberno, res, re.S).group(1)
    worldno = r"var _worldNo = '(.+?)';"
    worldno = re.search(worldno, res, re.S).group(1)
    data = {
        'pcid': pcid,
        'memberno': memberno,
        'worldno': worldno,
    }
    res2 = requests.post(url2, data=data).text
    soup = BeautifulSoup(res2, 'html.parser')
    list = soup.select(
        '#lui-tab1-7 > div > div.collection-list > ul > li')
    status = soup.select_one(
        '#lui-tab1-7 > div > div.collection-list > div > p').get_text()
    for v in range(0,len(list)):
            text = ' '.join(list[v].get_text().split())
            if v < 9:
                text = text[1:]
            else:
                text = text[2:]
            if "획득" in text:
                answer.append(f"`{text}`\n")
            else:
                answer2.append(f"`{text}`\n")
    answer = "".join(answer)
    answer2 = "".join(answer2)
    if answer == "":
        answer = '획득한 이그네아의 징표가 없습니다.'
    if answer2 == "":
        answer2 = '이그네아의 징표를 모두 획득하였습니다.'
    embed = discord.Embed(title=f"[{name}] 이그네아의 징표 획득 현황", description=f"{status}", color=0xAAFFFF)
    embed.add_field(name='> 획득', value=answer, inline=True)
    embed.add_field(name='> 미획득', value=answer2, inline=True)
    embed.set_thumbnail(url="https://i.imgur.com/X5ECwa0.png")
    embed.set_footer(text="명령어) .도움말", icon_url="https://i.imgur.com/X5ECwa0.png")
    created_log(name=ctx.author, command='이그네아')
    await ctx.send(embed=embed)

@app.command()
async def 세계수(ctx, *, name):
    i = 0
    answer = []
    answer2 = []
    url = f"https://lostark.game.onstove.com/Profile/Character/{name}"
    url2 = "https://lostark.game.onstove.com/Profile/GetCollection"
    res = requests.get(url).text
    soup = BeautifulSoup(res, 'html.parser')
    try:
        level = soup.select_one(
            '#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info2 > div.level-info2__expedition > span:nth-child(2)').get_text()
    except:
        await ctx.send('캐릭터를 찾을수 없습니다')
        return

    pcid = r"var _pcId = '(.+?)';"
    pcid = re.search(pcid, res, re.S).group(1)
    memberno = r"var _memberNo = '(.+?)';"
    memberno = re.search(memberno, res, re.S).group(1)
    worldno = r"var _worldNo = '(.+?)';"
    worldno = re.search(worldno, res, re.S).group(1)
    data = {
        'pcid': pcid,
        'memberno': memberno,
        'worldno': worldno,
    }
    res2 = requests.post(url2, data=data).text
    soup = BeautifulSoup(res2, 'html.parser')
    list = soup.select(
        '#lui-tab1-8 > div > div.collection-list > ul > li')
    status = soup.select_one(
        '#lui-tab1-8 > div > div.collection-list > div > p').get_text()
    for v in range(0,len(list)):
            text = ' '.join(list[v].get_text().split())
            if v < 9:
                text = text[1:]
            else:
                text = text[2:]
            if "획득" in text:
                answer.append(f"`{text}`\n")
            else:
                answer2.append(f"`{text}`\n")
    answer = "".join(answer)
    answer2 = "".join(answer2)
    if answer == "":
        answer = '`획득한 세계수의 잎이 없습니다.`'
    if answer2 == "":
        answer2 = '`세계수의 잎을 모두 획득하였습니다.`'
    embed = discord.Embed(title=f"[{name}] 세계수의 잎 획득 현황", description=f"{status}", color=0xAAFFFF)
    embed.add_field(name='> 획득', value=answer, inline=True)
    embed.add_field(name='> 미획득', value=answer2, inline=True)
    embed.set_thumbnail(url="https://i.imgur.com/X5ECwa0.png")
    embed.set_footer(text="명령어) .도움말", icon_url="https://i.imgur.com/X5ECwa0.png")
    created_log(name=ctx.author, command='세계수')
    await ctx.send(embed=embed)

@app.command()
async def 섬마(ctx, *, name):
    i = 0
    answer = []
    answer2 = []
    url = f"https://lostark.game.onstove.com/Profile/Character/{name}"
    url2 = "https://lostark.game.onstove.com/Profile/GetCollection"
    res = requests.get(url).text
    soup = BeautifulSoup(res, 'html.parser')
    try:
        level = soup.select_one(
            '#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info2 > div.level-info2__expedition > span:nth-child(2)').get_text()
    except:
        await ctx.send('캐릭터를 찾을수 없습니다')
        return

    pcid = r"var _pcId = '(.+?)';"
    pcid = re.search(pcid, res, re.S).group(1)
    memberno = r"var _memberNo = '(.+?)';"
    memberno = re.search(memberno, res, re.S).group(1)
    worldno = r"var _worldNo = '(.+?)';"
    worldno = re.search(worldno, res, re.S).group(1)
    data = {
        'pcid': pcid,
        'memberno': memberno,
        'worldno': worldno,
    }
    res2 = requests.post(url2, data=data).text
    soup = BeautifulSoup(res2, 'html.parser')
    list = soup.select(
        '#lui-tab1-1 > div > div.collection-list > ul > li')
    status = soup.select_one(
        '#lui-tab1-1 > div > div.collection-list > div > p').get_text()
    for v in range(0,len(list)):
            text = ' '.join(list[v].get_text().split())
            if v < 9:
                text = text[1:]
            else:
                text = text[2:]
            text = text.replace("의 마음", "")
            if "획득" in text:
                answer.append(f"`{text}`\n")
            else:
                answer2.append(f"`{text}`\n")
    answer = "".join(answer)
    answer2 = "".join(answer2)
    if answer == "":
        answer = '`획득한 섬의 마음이 없습니다.`'
    if answer2 == "":
        answer2 = '`섬의 마음을 모두 획득하였습니다.`'
    embed = discord.Embed(title=f"[{name}] 섬의 마음 획득 현황", description=f"`{status}`", color=0xAAFFFF)
    embed.add_field(name='> 획득', value=answer, inline=True)
    embed.add_field(name='> 미획득', value=answer2, inline=True)
    embed.set_thumbnail(url="https://i.imgur.com/X5ECwa0.png")
    embed.set_footer(text="명령어) .도움말", icon_url="https://i.imgur.com/X5ECwa0.png")
    created_log(name=ctx.author, command='섬마')
    await ctx.send(embed=embed)

@app.command()
async def 도움말(ctx):
    embed = discord.Embed(title="안녕하세요! 깜언 봇 입니다!", description="하단에서 모든 명령어를 보실수 있습니다\n> 문의 <@553252395325325343>", color=0x62c1cc)
    embed.add_field(name='캐릭터 검색', value='`.검색 캐릭터명`', inline=True)
    embed.add_field(name='수집형 포인트', value='`미구현`', inline=True)
    embed.add_field(name='오르페우스 별 검색', value='`.오페별 캐릭터명`', inline=False)
    embed.add_field(name='섬의 마음 검색', value='`.섬마 캐릭터명`', inline=True)
    embed.add_field(name='거인의 심장 검색', value='`.거심 캐릭터명`', inline=True)
    embed.add_field(name='위대한 미술품 검색', value='`.미술품 캐릭터명`', inline=True)
    embed.add_field(name='모코코 씨앗 검색', value='`.모코코 캐릭터명`', inline=True)
    embed.add_field(name='항해 모험물 검색', value='`.모험물 캐릭터명`', inline=True)
    embed.add_field(name='이그네아 징표 검색', value='`.이그네아 캐릭터명`', inline=True)
    embed.add_field(name='세계수의 잎 검색', value='`.세계수 캐릭터명`', inline=True)
    embed.set_thumbnail(url="https://i.imgur.com/X5ECwa0.png")
    embed.set_footer(text="명령어) .도움말", icon_url="https://i.imgur.com/X5ECwa0.png")
    created_log(name=ctx.author, command='도움말')
    await ctx.send(embed=embed)

app.run(os.environ.get('TOKEN'))
