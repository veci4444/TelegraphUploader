# Part of < https://github.com/xditya/TelegraphUploader >
# (c) 2021 @xditya.

import os
import logging
from PIL import Image
from telethon import TelegramClient, events, Button
from telethon.tl.functions.users import GetFullUserRequest
from decouple import config
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telegraph import Telegraph, exceptions, upload_file

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

appid = apihash = bottoken = None
# start the bot
print("Starting...")
try:
    apiid = config("API_ID", cast=int)
    apihash = config("API_HASH")
    bottoken = config("BOT_TOKEN")
except:
    print("Environment vars are missing! Kindly recheck and try again!")
    print("Bot is quiting...")
    exit()

if (apiid != None and apihash!= None and bottoken != None):
    try:
        BotzHub = TelegramClient('bot', apiid, apihash).start(bot_token=bottoken)
    except Exception as e:
        print(f"ERROR!\n{str(e)}")
        print("Bot is quiting...")
        exit()
else:
    print("Environment vars are missing! Kindly recheck and try again!")
    print("Bot is quiting...")
    exit()

# join check
async def check_user(id):
    ok = True
    try:
        await BotzHub(GetParticipantRequest(channel='@frobid', user_id=id))
        ok = True
    except UserNotParticipantError:
        ok = False
    return ok

@BotzHub.on(events.NewMessage(incoming=True, pattern="/start", func=lambda e: e.is_private))
async def start(event):
    ok = await BotzHub(GetFullUserRequest(event.sender_id))
    if (await check_user(event.sender_id)) == False:
        return await event.reply(f"Sorry {ok.user.first_name} 😔️, **You must Join My Updates Channel To Use Me!** 😌️", buttons=[Button.url("🔰️ Join My Updates Channel 🔰️", url="https://t.me/NexaBotsUpdates")])
    await event.reply(f"Hi, {ok.user.first_name} 😉️!\nI am Telegraph Nexa Bot. Just Forward or Send me `Supported Media!` .\n\nFound Bugs? or Any Suggestions? 🤔️. Go here **@Nexa_bots**",
                     buttons=[
                         Button.inline("About 🤷‍♂️️", data="about"),
                         Button.inline("Help ❓", data="help"),
                         Button.inline("Credits ❤️", data="credits")
                     ])

@BotzHub.on(events.callbackquery.CallbackQuery(data="help"))
async def _(event):
    ok = await BotzHub(GetFullUserRequest(event.sender_id))
    await event.edit(f"Send or Forward me Supported Media and I will upload it to Telegraph! 🙂️\n\n **Supported Media Formates 🤔️,** \n\n❄️ `Images`\n❄️ `Small Videos`\n❄️ `Gifs`\n❄️ `Some Types Of Stickers`\n\nHosted with ❤️ by **@NexaBotsUpdates** .", buttons=[Button.inline("About 🤷‍♂️️", data="about"), Button.inline("Credits ❤️", data="credits"), Button.inline("Home 🏘️", data="home")])
                          
                          
@BotzHub.on(events.callbackquery.CallbackQuery(data="about"))
async def _(event):
    ok = await BotzHub(GetFullUserRequest(event.sender_id))
    await event.edit(f"Hi, {ok.user.first_name} 😉️!\nI am Telegraph Nexa Bot! 🙂️\n\n**Master : [I'm Not A Bot](https://t.me/Bruh_0x)** \n**Updates Channel : [Nexa Bots](https://t.me/NexaBotsUpdates)** \n**Support Group : [Nexa Bots Support](https://t.me/Nexa_bots)**\n\nWith ❤️ by **@NexaBotsUpdates** .", buttons=[Button.inline("Help ❓", data="help"), Button.inline("Credits ❤️", data="credits"), Button.inline("Home 🏘️", data="home")])


  
@BotzHub.on(events.callbackquery.CallbackQuery(data="credits"))
async def _(event):
    ok = await BotzHub(GetFullUserRequest(event.sender_id))
    await event.edit(f"Hi, 😉️ {ok.user.first_name}!\nI am Telegraph Nexa Bot! 🙂️\n\nCredits To **XDITYA**\n\nJoin **@NexaBotsUpdates**", buttons=[Button.inline("Help ❓", data="help"), Button.inline("About 🤷‍♂️️", data="about"), Button.inline("Home 🏘️", data="home")])                 

@BotzHub.on(events.callbackquery.CallbackQuery(data="home"))
async def _(event):
    ok = await BotzHub(GetFullUserRequest(event.sender_id))
    await event.edit(f"Hi, 😉️ {ok.user.first_name}!\nI am Telegraph Nexa Bot! 🙂️. Just Forward or Send me Supported Media!\n\nFound Bugs? or Any Suggestions? 🤔️. Go here **@Nexa_bots**\n\nWith ❤️ by **@NexaBotsUpdates**",
                     buttons=[
                         Button.inline("About 🤷‍♂️️", data="about"),
                         Button.inline("Help ❓", data="help"),
                         Button.inline("Credits ❤️", data="credits")
                     ])


@BotzHub.on(events.NewMessage(incoming=True, func=lambda e: e.is_private and e.media))
async def uploader(event):
    if (await check_user(event.sender_id)) is False:
        return
    TMP_DOWNLOAD_DIRECTORY = "./BotzHub/"
    if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TMP_DOWNLOAD_DIRECTORY)
    pic = event.media
    ok = await event.reply("`Downloading Your File... Please wait...`")
    downloaded_file_name = await BotzHub.download_media(pic, TMP_DOWNLOAD_DIRECTORY)
    if downloaded_file_name.endswith((".webp")):
        await ok.edit("`Oh no! It's a sticker...\nLemme convert it!!`")
        resize_image(downloaded_file_name)
    try:
        media_urls = upload_file(downloaded_file_name)
    except exceptions.TelegraphException as exc:
        await ok.edit("**Error : **" + str(exc))
        os.remove(downloaded_file_name)
        return
    else:
        os.remove(downloaded_file_name)
        await ok.edit("Your file is successfully uploaded to [Telegraph](https://telegra.ph{})\n\nJoin My Updates Channel **@NexaBotsUpdates** ❤️".format(media_urls[0]),
                    link_preview=True,
                    buttons=[
                        Button.url("🔗 Link To File 🔗", url=f"https://telegra.ph{media_urls[0]}")
                    ])

def resize_image(image):
    im = Image.open(image)
    tmp = im.save(image, "PNG")

print("Bot has started.")
print("Made By XDITYA . Do visit @NexaBotsUpdates..")
BotzHub.run_until_disconnected()
