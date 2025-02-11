from discord.ext import commands
import discord
import os
from os.path import join, dirname
import random
import secrets
from dotenv import load_dotenv
import numpy as np
from PIL import Image
import asyncio

# サーバーごとのデフォルト設定を保持する辞書
server_settings = {}

def first_time_action():
    global server_settings
    if not server_settings:
        # 初期設定（例: 全サーバーにデフォルトの設定を追加）
        server_settings = {}

first_time_action()

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True  # メンバー管理の権限
intents.message_content = True  # メッセージの内容を取得する権限

IMAGE_DIR = './images'
YAJU_DIR = './yaju'

bot = commands.Bot(
    command_prefix="!",
    case_insensitive=True,
    intents=intents
)

@bot.event
async def on_ready():
    print(f'ログインしました: {bot.user}')

@bot.command(aliases=["dman"])
async def deeman(ctx, bad:str="deeman"):
    await ctx.send("deemanはカス")

@bot.command(aliases=["frtk"])
async def frtkshop(ctx, bad:str="frtkshop"):
    await ctx.send("ふらつきショップはカス")

@bot.command()
async def alser(ctx, bad:str="alser"):
    await ctx.send("Alserはカス")

@bot.command()
async def dmeigen(ctx):
    emoji = discord.utils.get(ctx.guild.emojis, name="hiroyuki_narita")
    responses = ["共用の…強要！", "アルターエゴ楽しすぎる", "末代まで祟ってやる", "生きててごめんなさい…", "今キンタマに篭城してます", "ピュピュピュピュピュピュ ピュ〜〜〜〜〜〜〜〜", "おじさんを、持参！", "イクーーーーッ！！！", "おやふら","おまんこ壊れちゃう〜(><)","いちごパンツで抜くと濃いのでる","ボルテ19以上3時間触るよりアーケア1時間やるほうが疲れる", "初めまして、ドけんた食堂です\n\n今日はたこ焼きを食べていきたいと思います\n\nドピュビュルル(たこ焼きを食べる音)\n\nビュボボ…(たこ焼きを食べる音)\n\nドガーンガシャガシャ(たこ焼きを食べる音)\n\nウィーンピポピポドドドドドドガッシャンガッシャン(たこ焼きを食べる音)\n\n……\n\n粋スギィ！(満面の笑み)","おふろ",str(emoji) + "<お前を殺す。","デカいウンコの恐竜、デカウンコザウルス"]
    response = random.choice(responses)
    await ctx.send(response)

@bot.command()
async def debug(ctx, directory: str, query: str):
    # 指定されたディレクトリの存在を確認
    if not os.path.exists(directory) or not os.path.isdir(directory):
        await ctx.send("指定されたディレクトリが存在しません。")
        return
    
    # 指定ディレクトリ内のファイルを検索
    matched_files = [f for f in os.listdir(directory) if query.lower() in f.lower()]
    
    if not matched_files:
        await ctx.send("該当する画像が見つかりませんでした。")
        return
    
    for file in matched_files:
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):  # ファイルであることを確認
            await ctx.send(f"ファイル名: {file}", file=discord.File(file_path))

@bot.command()
async def setDefaultGuessc(ctx, DefaultDivision: float):
    """サーバーごとにDefaultGを設定"""
    server_id = str(ctx.guild.id)
    
    # サーバーがまだ設定されていない場合、初期設定を追加
    if server_id not in server_settings:
        server_settings[server_id] = {'DefaultG': 6, 'DefaultM': 6}
    
    # 入力値を検証
    if DefaultDivision < 1 or DefaultDivision > 20:
        await ctx.send("エラー: 分割数は1以上20以下の値を指定してください。")
        return
    
    # サーバーごとの設定を更新
    server_settings[server_id]['DefaultG'] = DefaultDivision
    await ctx.send(f"サーバーのデフォルト分割数を {DefaultDivision} に設定しました。")

@bot.command()
async def setDefaultMosaic(ctx, DefaultMosaic: int):
    """サーバーごとにDefaultMを設定"""
    server_id = str(ctx.guild.id)
    
    # サーバーがまだ設定されていない場合、初期設定を追加
    if server_id not in server_settings:
        server_settings[server_id] = {'DefaultG': 6, 'DefaultM': 6}
    
    # 入力値を検証
    if DefaultMosaic < 5 or DefaultMosaic > 500:
        await ctx.send("エラー: 分割数は5以上500以下の値を指定してください。")
        return
    
    # サーバーごとの設定を更新
    server_settings[server_id]['DefaultM'] = DefaultMosaic
    await ctx.send(f"サーバーのデフォルトモザイク分割数を {DefaultMosaic} に設定しました。")

@bot.command(aliases=["p"])
async def potential(ctx: commands.context, const: float, score: float) -> None:

    FRAG = 0

    if (score < 0) or (const < 0):
        await  ctx.send("Error:譜面定数、スコアは正の値を入力してください。")
        FRAG = -1
    if const > score:
        a = const
        const = score
        score = a
    while score<1000000:
        score *= 10
    if score>=10000000:
        potential = const + 2.0
    elif score>=9800000:
        potential = const + 1.0 + (score - 9800000)/200000
    else:
        potential = const + (score - 9500000)/300000
    if FRAG == 0:
        if potential < 0:
            await  ctx.send("0")
        else:
            await ctx.send(potential)


@bot.command(aliases=["s"])
async def skip(ctx):
    global skip_flag
    skip_flag = True
    await ctx.send("出題をスキップしました！")


def is_acronym(input_str, answer_str):
    """入力が正解の頭文字を取った省略形であるか確認"""
    acronym = ''.join(word[0] for word in answer_str.split() if word)
    return input_str.lower() == acronym.lower()

# モザイク処理の追加
@bot.command(aliases=["m"])
async def mosaic(ctx, block_size: int = None ,yaju: str='null'):
    server_id = str(ctx.guild.id)
    
    # サーバーのデフォルト設定を参照
    if server_id not in server_settings:
        server_settings[server_id] = {'DefaultG': 6, 'DefaultM': 6}
    DefaultM = server_settings[server_id]['DefaultM']
    # block_sizeが指定されていなければデフォルト値を使用
    if block_size is None:
        if DefaultM is not None:
            block_size = DefaultM
        else:
            block_size = 80  # デフォルトの値をここに設定（もしデフォルト値がない場合）
    try:
        if block_size < 5 or block_size > 500:
            await ctx.send("分割数は5以上500以下の数にしてください。")
            return

        # 画像の選択
        image_files = [f for f in os.listdir(IMAGE_DIR) if f.endswith(('png', 'jpg', 'jpeg', 'gif'))]
        if not image_files:
            await ctx.send("画像が見つかりません。")
            return

        random_image = secrets.choice(image_files)
        image_path = os.path.join(IMAGE_DIR, random_image)

        if(yaju=='yaju'):
            image_files = [f for f in os.listdir(YAJU_DIR) if f.endswith(('png', 'jpg', 'jpeg', 'gif'))]
            if not image_files:
                await ctx.send("画像が見つかりません。")
                return
            random_image = secrets.choice(image_files)
            image_path = os.path.join(YAJU_DIR, random_image)

        # 画像の読み込み
        img = Image.open(image_path)
        img_width, img_height = img.size
        img_array = np.array(img)

        # モザイク処理
        for y in range(0, img_height, block_size):
            for x in range(0, img_width, block_size):
                block = img_array[y:y + block_size, x:x + block_size]
                avg_color = np.mean(block, axis=(0, 1)).astype(int)
                img_array[y:y + block_size, x:x + block_size] = avg_color

        # モザイク画像を保存
        mosaic_img = Image.fromarray(img_array)
        temp_image_path = 'temp_image.png'
        mosaic_img.save(temp_image_path)

        # モザイク画像を送信
        sent_message = await ctx.send(file=discord.File(temp_image_path))
        
        # ファイル削除前に送信したメッセージに関連するファイルパスを保持
        os.remove(temp_image_path)

        def check(m):
            return m.channel == ctx.channel and m.reference is not None and m.reference.message_id == sent_message.id

        start_time = asyncio.get_event_loop().time()
        FRAG = 1

        while asyncio.get_event_loop().time() - start_time < 30:
            try:
                response = await asyncio.wait_for(bot.wait_for('message', check=check), timeout=30.0)
                if (response.content.lower() == os.path.splitext(random_image)[0].lower()) or (len(response.content) >= 3 and response.content.lower() in os.path.splitext(random_image)[0].lower()) or (len(response.content) >= 3 and is_acronym(response.content, os.path.splitext(random_image)[0])):
                    await response.reply("正解です！")
                    FRAG = 0
                    break
                elif (response.content.lower() == ("!s" or "!skip")):
                    break
                else:
                    await response.reply("残念！もう一度お試しください。")
            except asyncio.TimeoutError:
                continue

        if FRAG:
            await ctx.send("時間切れです！")
        await ctx.send(f"正解は `{os.path.splitext(random_image)[0]}` でした！")
        await ctx.send(file=discord.File(image_path))

    except Exception as e:
        await ctx.send(f"エラーが発生しました: {e}")




@bot.command(aliases=["g"])
async def guessc(ctx, n: float = 6):
    server_id = str(ctx.guild.id)
    
    # サーバーのデフォルト設定を参照
    if server_id not in server_settings:
        server_settings[server_id] = {'DefaultG': 6, 'DefaultM': 6}
    DefaultG = server_settings[server_id]['DefaultG']
    # block_sizeが指定されていなければデフォルト値を使用
    if n is None:
        if DefaultG is not None:
            n = DefaultG
        else:
            n = 6  # デフォルトの値をここに設定（もしデフォルト値がない場合）
    try:
        # nが1以上の数であることを確認
        if n < 1 or n > 20:
            await ctx.send("分割数は1以上20以下の数にしてください。")
            return

        # 画像の選択
        image_files = [f for f in os.listdir(IMAGE_DIR) if f.endswith(('png', 'jpg', 'jpeg', 'gif'))]
        if not image_files:
            await ctx.send("画像が見つかりません。")
            return

        random_image = secrets.choice(image_files)
        image_path = os.path.join(IMAGE_DIR, random_image)

        # 画像の分割処理
        img = Image.open(image_path)
        img_width, img_height = img.size
        tile_width = int(img_width // n)
        tile_height = int(img_height // n)

        tiles = []
        for i in range(int(n)):
            for j in range(int(n)):
                left = j * tile_width
                upper = i * tile_height
                right = left + tile_width
                lower = upper + tile_height
                tiles.append(img.crop((left, upper, right, lower)))

        # ランダムなタイルを選択
        selected_tile = secrets.choice(tiles)

        # 一時ファイルとして保存
        temp_path = 'temp_image.png'
        selected_tile.save(temp_path)

        sent_message = await ctx.send(file=discord.File(temp_path))
        os.remove(temp_path)

        def check(m):
            return m.channel == ctx.channel and m.reference is not None and m.reference.message_id == sent_message.id

        start_time = asyncio.get_event_loop().time()
        FRAG = 1

        while asyncio.get_event_loop().time() - start_time < 30:
            try:
                response = await asyncio.wait_for(bot.wait_for('message', check=check), timeout=30.0)
                if (response.content.lower() == os.path.splitext(random_image)[0].lower()) or (len(response.content) >= 3 and response.content.lower() in os.path.splitext(random_image)[0].lower()) or (len(response.content) >= 3 and is_acronym(response.content, os.path.splitext(random_image)[0])):
                    await response.reply("正解です！")
                    FRAG = 0
                    break
                elif (response.content.lower() == ("!s" or "!skip")):
                    break
                else:
                    await response.reply("残念！もう一度お試しください。")
            except asyncio.TimeoutError:
                continue

        if FRAG:
            await ctx.send("時間切れです！")
        await ctx.send(f"正解は `{os.path.splitext(random_image)[0]}` でした！")
        await ctx.send(file=discord.File(image_path))

    except Exception as e:
        await ctx.send(f"エラーが発生しました: {e}")


bot.run(TOKEN)
