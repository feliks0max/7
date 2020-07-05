import discord
from discord.ext import commands
import random
import os
import requests
from bs4 import BeautifulSoup
import sqlite3
from config import settings
import wikipedia
import json
import requests
from discord.utils import get


bot = commands.Bot(command_prefix = settings['PREFIX'])
bot.remove_command( 'help' )



PREFIX = settings['PREFIX']
owner = settings['OWNER']
data_create = settings['data_create']

@bot.event
async def on_ready():



    print('Бот зашёл в сеть' )
    print('и он готов к работе')
    print(f'Создаель: {owner}.')
    print(f'Создан: {data_create}')
    print(f'Prefix: "{PREFIX}"')



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound ):
        await ctx.send(embed = discord.Embed(description = f'** {ctx.author.name}, данной команды не существует.**', color=0x0c0c0c))

@bot.event
async def on_message(message):
    #Чтение лс
    await bot.process_commands(message)
    if message.author != bot.user:
        if not message.guild: # Проверка что это ЛС
            chanel = chanel = bot.get_channel(719172738190803006)
            if message.content == None:
                text = 'Пустое сообщение'
            else:
                text = message.content

            if message.attachments == []:
                file = 'Файла нет'
                filename = 'Файла нет'
            else:
                file = message.attachments[0].url
                filename = message.attachments[0].filename

            embed = discord.Embed(title = message.author.name, description = f'''
    Текст сообщения: {text}
    Название файла: {filename}
    Ccылка на файл: {file}
    '''
    ,color=discord.Colour.green())
            embed.set_author(name=message.author, icon_url=message.author.avatar_url)

            await chanel.send(embed = embed)




# тестовая кмд
@bot.command(pass_context=True)  # разрешаем передавать агрументы
async def test(ctx, arg):  # создаем асинхронную фунцию бота
    await ctx.send(arg)  # отправляем обратно аргумент

# кмд привет
@bot.command()
async def hello(ctx):
    await ctx.send( "Приветствую!" )

#очистка чата
@bot.command()
@commands.has_permissions( administrator = True )
async def clear(ctx, amount=None):
    await ctx.channel.purge(limit=int(amount))
    await ctx.channel.send(':: Сообщения успешно удалены ::')

reason = 'reason'

# кикнуть чела
@bot.command()
@commands.has_permissions( administrator = True)
async def kick(ctx, member: discord.Member, *, reason = reason ):
    emb = discord.Embed( title = 'Кик!', description = f'Администратор: ``{ ctx.author.name }``, кикнул пользователя: { member.mention }!', colour = discord.Color.red())
    await member.kick( reason = reason )
    await ctx.send( embed = emb )



# забанить чела
@bot.command()
@commands.has_permissions( administrator = True)
async def ban(ctx, member: discord.Member, *, reason = None ):
    emb = discord.Embed( title = '**Бан**', description = f'** { member.mention } Был забанен за нарушения правил сервера**', colour = discord.Color.red())
    await ctx.channel.purge( limit = 1 )
    await member.ban( reason = reason)
    await ctx.send( embed = emb )


# список кмд
@bot.command()
async def help( ctx ):
    emb = discord.Embed( title = '**Выбирите категорию!**', description = 'Категории: ``moderation | funny | other``.    Пример: ``/help_moderation``!', colour = discord.Color.red())

    await ctx.channel.purge( limit = 1)

    await ctx.send( embed = emb )




# Измение статус
@bot.command()
@commands.is_owner()
async def inplay(ctx, *, arg):
    emb = discord.Embed( title = 'Изменения статуса!', description = 'Статус бота изменён!', colour = discord.Color.red())
    if not commands.NotOwner:
        await ctx.send(f"Отказано в доступе!")
    else:
        await bot.change_presence(activity=discord.Game(name=arg))
        await ctx.send( embed = emb )

@bot.command()
@commands.is_owner()
async def inwatch(ctx, *, arg):
    emb = discord.Embed( title = 'Изменения статуса!', description = 'Статус бота изменён!', colour = discord.Color.red())
    if not commands.NotOwner:
        await ctx.send(f"Отказано в доступе!")
    else:
        await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(name=arg, type=discord.ActivityType.watching))
        await ctx.send( embed = emb )

@bot.command()
@commands.is_owner()
async def inlisten(ctx, *, arg):
    emb = discord.Embed( title = 'Изменения статуса!', description = 'Статус бота изменён!', colour = discord.Color.red())
    if not commands.NotOwner:
        await ctx.send(f"Отказано в доступе!")
    else:
        await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(name=arg, type=discord.ActivityType.listening))
        await ctx.send( embed = emb )

@bot.command()
@commands.is_owner()
async def instream(ctx, *, arg):
    emb = discord.Embed( title = 'Изменения статуса!', description = 'Статус бота изменён!', colour = discord.Color.red())
    if not commands.NotOwner:
        await ctx.send(f"Отказано в доступе!")
    else:
        await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(name=arg, type=discord.ActivityType.streaming))
        await ctx.send( embed = emb )

# пргласить бота
@bot.command()
async def invite_bot(ctx):
    emb = discord.Embed( title = 'Ссылка на приглашения бота на свой севрер!', description = 'https://discord.com/oauth2/authorize?client_id=599587609240666123&scope=bot&permissions=2147483647 Перейди по этой ссылки и прегласи бота на севрер!',
    colour = discord.Color.blue())
    await ctx.send( embed = emb )


# эмодзи
@bot.command(aliases = ["емодзи", "емоджи", "эмоджи", "эмоция"])
async def emoji(ctx, emoji: discord.Emoji):
    await ctx.channel.purge( limit = 1)
    e = discord.Embed(description = f"[Эмодзи]({emoji.url}) сервера {emoji}")
    e.add_field(name = "Имя:", value = f"`{emoji.name}`")
    e.add_field(name = "Автор:", value = f"{(await ctx.guild.fetch_emoji(emoji.id)).user.mention}")
    e.add_field(name = "‎‎‎‎", value = "‎‎‎‎")
    e.add_field(name = "Время добавления:", value = f"`{emoji.created_at}`")
    e.add_field(name = "ID эмодзи:", value = f"`{emoji.id}`")
    e.add_field(name = "‎‎‎‎", value = "‎‎‎‎")
    e.set_thumbnail(url = f"{emoji.url}")
    await ctx.send(embed = e)


@bot.command()
async def say_hello( ctx, member: discord.Member ):
    await ctx.channel.purge( limit = 1 )
    emb = discord.Embed( title = '``Привет!``', description = f'Пользователь ``{ ctx.author.name }``, передал привет ``{ member.name }``! ', colour = discord.Color.blue())
    await member.send(f'Привет { member.name }, ты в курсе что { ctx.author.name } передал тебе привет?')
    await ctx.send( embed = emb )

@bot.command()
async def game(ctx):
    a = random.randint(1, 2)
    if a == 1:
        emb = discord.Embed(title = '__**Орёл и решка**__', color = discord.Colour.blue())
        emb.add_field(name = 'Что выпало:', value = '*Вам выпал* __**орёл**__')
        emb.set_thumbnail(url = 'https://i.gifer.com/ZXv0.gif')
        await ctx.send(embed = emb)
        emb.set_footer(text=f"Запросил: {ctx.author}", icon_url=ctx.author.avatar_url)
    else:
        emb = discord.Embed(title = '__**Орёл и решка**__', color = discord.Colour.red())
        emb.add_field(name = 'Что выпало:', value = '*Вам выпала* __**решка**__')
        emb.set_thumbnail(url = 'https://i.gifer.com/ZXv0.gif')
        await ctx.send(embed = emb)
        emb.set_footer(text=f"Запросил: {ctx.author}", icon_url=ctx.author.avatar_url)

@bot.command()
async def saper(ctx):
    embed = discord.Embed(description = '''
                     Держи :smile:
||0️⃣||||0️⃣||||0️⃣||||1️⃣||||1️⃣||||2️⃣||||1️⃣||||2️⃣||||1️⃣||||1️⃣||||
2️⃣||||2️⃣||||1️⃣||||1️⃣||||💥||||2️⃣||||💥||||3️⃣||||💥||||1️⃣||||
💥||||💥||||1️⃣||||1️⃣||||2️⃣||||3️⃣||||3️⃣||||💥||||2️⃣||||1️⃣||||
2️⃣||||2️⃣||||1️⃣||||0️⃣||||1️⃣||||💥||||2️⃣||||1️⃣||||1️⃣||||0️⃣||||
0️⃣||||0️⃣||||0️⃣||||1️⃣||||2️⃣||||2️⃣||||1️⃣||||0️⃣||||0️⃣||||0️⃣||||
1️⃣||||1️⃣||||0️⃣||||1️⃣||||💥||||1️⃣||||1️⃣||||2️⃣||||2️⃣||||1️⃣||||
💥||||1️⃣||||1️⃣||||2️⃣||||2️⃣||||1️⃣||||1️⃣||||💥||||💥||||1️⃣||||
1️⃣||||1️⃣||||1️⃣||||💥||||1️⃣||||1️⃣||||2️⃣||||3️⃣||||2️⃣||||1️⃣||||
1️⃣||||2️⃣||||2️⃣||||2️⃣||||2️⃣||||2️⃣||||💥||||1️⃣||||0️⃣||||0️⃣||||
💥||||2️⃣||||💥||||1️⃣||||1️⃣||||💥||||2️⃣||||2️⃣||||1️⃣||||1️⃣||||
1️⃣||||2️⃣||||1️⃣||||1️⃣||||1️⃣||||1️⃣||||1️⃣||||1️⃣||||💥||||1️⃣||
    ''', color = discord.Colour.orange())
    await ctx.send(embed=embed)

@bot.command(aliases=['коронавирус'])
async def cov(ctx):
    Corona = 'https://xn--80aesfpebagmfblc0a.xn--p1ai/#operational-data'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

    full_page = requests.get(Corona, headers=headers)
    soup = BeautifulSoup(full_page.content, 'html.parser')

    convert = soup.findAll("div", {"class": "cv-countdown__item-value"})
    hz = soup.find("div",{"class":"cv-banner__description"})

    heads = []
    for i in convert:
        heads.append(i.string)

    emb = discord.Embed(title=f"Данные по короновирусу. {hz.string}", color=708090)
    emb.set_author(name = bot.user.name, icon_url = bot.user.avatar_url)
    emb.add_field(name="Заболело: ", value=heads[1], inline=False)
    emb.add_field(name="Выздоровело: ", value=heads[3], inline=False)
    emb.add_field(name="Умерло: ", value=heads[4], inline=False)
    emb.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Biohazard_orange.svg/1200px-Biohazard_orange.svg.png')
    await ctx.send(embed=emb)

# HELP
@bot.command()
async def help_moderation( ctx ):
    await ctx.channel.purge( limit = 1 )
    emb = discord.Embed( title = '**Команды модерации!**', colour = discord.Color.red())

    emb.add_field( name = '`{}clear`'.format( PREFIX ), value = '**очистка чата (для адм)**')
    emb.add_field( name = '`{}kick`'.format( PREFIX ), value = '**Кикнуть пользователя (для адм)**')
    emb.add_field( name = '`{}ban`'.format( PREFIX ), value = '**Забанить пользователя (для адм)**')

    await ctx.send( embed = emb )

@bot.command()
async def help_funny( ctx ):
    await ctx.channel.purge( limit = 1 )
    emb = discord.Embed( title = '**Список "Фан" команд!**', colour = discord.Color.blue())

    emb.add_field( name = '`{}game`'.format( PREFIX ), value = '**Игра в орл и решку**')
    emb.add_field( name = '`{}saper`'.format( PREFIX ), value = '**Игра в сапера**')
    emb.add_field( name = '`{}hello`'.format( PREFIX ), value = '**Поздороваться с ботом**')
    emb.add_field( name = '`{}fake_kick`'.format( PREFIX ), value = '**Фэйк Кик!**')
    emb.add_field( name = '`{}fake_ban`'.format( PREFIX ), value = '**Фэйк Бан!**')
    emb.add_field( name = '`{}fake_mute`'.format( PREFIX ), value = '**Фэйк Мут!**')
    emb.add_field( name = '`{}hug(@пользователь)`'.format( PREFIX ), value = '**Обнять пользователя**')
    emb.add_field( name = '`{}kiss(@пользователь)`'.format( PREFIX ), value = '**Поцеловать пользователя!**')

    await ctx.send( embed = emb )

@bot.command()
async def help_other( ctx ):
    await ctx.channel.purge( limit = 1 )
    emb = discord.Embed( title = '**Список прочих команд:**', colour = discord.Color.red())

    emb.add_field( name = '`{}invite_bot`'.format( PREFIX ), value = '**Получить ссылку на бота для подключения на свой сервер!**')
    emb.add_field( name = '`{}emoji (сам эмодзи)`'.format( PREFIX ), value = '**Узнать информацию о эмодзи добавленый на этот сервер**')
    emb.add_field( name = '`{}say_hello`'.format( PREFIX ), value = '**При вводе этой комманды и упоменания человека которому хотите передать привет бот будет пистать ему привет ( в личные сообщения )!**')
    emb.add_field( name = '`{}cov`'.format( PREFIX ), value = '**Статистика короновируса в России**')
    emb.add_field( name = '`{}profile`'.format( PREFIX ), value = '**Информация о вашем аккаунте!**')
    emb.add_field( name = '`{}wiki`'.format( PREFIX ), value = '**Найти страницу на wikipedia!**')
    emb.add_field( name = '`{}cat`'.format( PREFIX ), value = '**Фотки котиков!**')
    emb.add_field( name = '`{}dog`'.format( PREFIX ), value = '**Фотки собак!**')

    await ctx.send( embed = emb )


@bot.command()
async def ping( ctx ):
    await ctx.send('Pong')

# Profile
@bot.command(pass_context=True)
async def profile(ctx):
    roles = ctx.author.roles
    role_list = ""
    for role in roles:
        role_list += f"<@&{role.id}> "
    emb = discord.Embed(title='Profile', colour = discord.Colour.purple())
    emb.set_thumbnail(url=ctx.author.avatar_url)
    emb.add_field(name='Никнэйм', value=ctx.author.mention)
    emb.add_field(name="Активность", value=ctx.author.activity)
    emb.add_field(name='Роли', value=role_list)
    if 'online' in ctx.author.desktop_status:
        emb.add_field(name="Устройство", value=":computer:Компьютер:computer:")
    elif 'online' in ctx.author.mobile_status:
        emb.add_field(name="Устройство", value=":iphone:Телефон:iphone:")
    elif 'online' in ctx.author.web_status:
        emb.add_field(name="Устройство", value=":globe_with_meridians:Браузер:globe_with_meridians:")
    emb.add_field(name="Статус", value=ctx.author.status)
    emb.add_field(name='Id', value=ctx.author.id)
    await ctx.channel.purge(limit=1)
    await ctx.send(embed = emb )

@bot.command()
async def fake_kick( ctx, member: discord.Member ):
    emb = discord.Embed( title = 'Кик!', description = f'Администратор: ``{ ctx.author.name }``, кикнул пользователя: { member.mention }!', colour = discord.Color.red())
    await ctx.send( embed = emb )

@bot.command()
async def fake_ban( ctx, member: discord.Member ):
    emb = discord.Embed( title = 'Ban!', description = f'Администратор: ``{ ctx.author.name }``, забанил пользователя: { member.mention }!', colour = discord.Color.red())
    await ctx.send( embed = emb )

@bot.command()
async def fake_mute( ctx, member: discord.Member ):
    emb = discord.Embed( title = 'Мут!', description = f'Администратор: ``{ ctx.author.name }``, выдал мут: { member.mention }!', colour = discord.Color.red())
    await ctx.send( embed = emb )

@bot.command()
async def official_server( ctx ):
    emb = discord.Embed( title = '**Официальный сервер бота!**', description = '**Ссылка на официальный сервер бота отправлена тебе в Личные сообщения!**')

    await ctx.send( embed = emb )
    await ctx.author.send( 'Ссылка на официальный сервер бота: https://discord.gg/Vrvypxj, по всем вопросам обращаться туда!' )

@bot.command()
async def wiki(ctx, *, text):
    wikipedia.set_lang("ru")
    new_page = wikipedia.page(text)
    summ = wikipedia.summary(text)
    emb = discord.Embed(
        title= new_page.title,
        description= summ,
        color = 0xc582ff)

    await ctx.send(embed=emb)





@bot.command()
@commands.is_owner()
async def game_help(ctx, *, arg):
    emb = discord.Embed(title = 'Успешно!', description = f'Мистер {owner}! Секретная кмд была выполнена!', colour = discord.Color.blue())

    if not commands.NotOwner:
        await ctx.send(f'Прости {ctx.author.name}, но ты не такой классный что бы использовать эту команду(')

    else:
        await bot.change_presence(activity=discord.Game(name="/help"))
        await ctx.send(embeb = emb)

@bot.command()
async def kiss(ctx, member: discord.Member):
    emb = discord.Embed(title = '💋Поцелуй!💋', description = f'**Пользователь: ``{ctx.author.name}``, поцеловал { member.mention }!💋**', colour = discord.Color.red())
    emb.set_thumbnail(url = 'https://d.radikal.ru/d43/2006/76/fb8f09103a8f.gif')
    await ctx.send( embed = emb )


@bot.command()
async def hug(ctx, member: discord.Member):
	emb = discord.Embed(title = '**Объятия!**', description = f'**Пользователь: {ctx.author.name}, обнял: {member.mention}!**', colour = discord.Color.blue())

	await ctx.send(embed = emb)
@bot.command()
async def dog( ctx ):
    response = requests.get('https://api.thedogapi.com/v1/images/search')
    json_data = json.loads(response.text)
    url = json_data[0]['url']

    embed = discord.Embed(color = 0xff9900)
    embed.set_image( url = url )

    await ctx.send( embed = embed )
@bot.command()
async def cat( ctx ):
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    json_data = json.loads(response.text)
    url = json_data[0]['url']

    embed = discord.Embed(color = 0xff9900)
    embed.set_image( url = url )

    await ctx.send( embed = embed )
@bot.command()
async def join(ctx):
  channel= ctx.message.author.voice.channel
  await channel.connect()
@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()
    await ctx.message.delete()
    
token = os.environ.get('BOT_TOKEN')

Bot.run(str(token))