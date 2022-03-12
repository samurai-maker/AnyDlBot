import os
import logging
import asyncio
from urllib.parse import urlparse
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from youtube_dl import YoutubeDL
from opencc import OpenCC
from config import Config

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)
CHANNEL_FORWARD_TO = -1001668382627

Jebot = Client(
   "YT Downloader",
   api_id=Config.APP_ID,
   api_hash=Config.API_HASH,
   bot_token=Config.TG_BOT_TOKEN,
)

BotzHub = Client('BotzHub', apiid, apihash).start(bot_token=bottoken)


YTDL_REGEX = (r"^((?:https?:)?\/\/)"
              r"?((?:www|m)\.)"
              r"?((?:youtube\.com|youtu\.be|xvideos\.com|pornhub\.com"
              r"|xhamster\.com|xnxx\.com))"
              r"(\/)([-a-zA-Z0-9()@:%_\+.~#?&//=]*)([\w\-]+)(\S+)?$")
s2tw = OpenCC('s2tw.json').convert


@Jebot.on_message(filters.command("start"))
async def start(client, message):
   if message.chat.type == 'private':
       await Jebot.send_message(
               chat_id=message.chat.id,
               text="""<b>
വെൽക്കം എയർ കമ്പി 🛩,
എല്ലായാത്രക്കാരും നിയമങ്ങൾ അനുസരിച്ച് യാത്ര ചെയ്യുക
ലിങ്ക് എനിക്ക് അയച്ചു തന്നാൽ ഞാൻ ഡൌൺലോഡ് ചെയ്തു തരാം </b>\n\n
<i>
1.യുട്യൂബ്\n
2.എക്സ്.എൻ.എക്സ്.എക്സ്\n
3.എക്സ് വീഡിയോസ്\n
4.പോൺഹബ്\n
5.എക്സ്ഹസ്റ്റർ
</i>\n\n
<i>നിയമങ്ങൾ:</i>
<b> 1.പതിനെട്ടു തികയാത്ത ആരും എന്റെ മേലെ കൈ വെക്കരുത്❌</b>\n
<b> 2.ചൈൽഡ് പോൺ കർശനമായി നിരോധിച്ചിരിക്കുന്നു❌</b>
""",   
                            reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "വടക്കിനിപ്പുര", url="https://t.me/vadakinipura")
                                    ]]
                            ),      
            disable_web_page_preview=True,        
            parse_mode="html")
# join check
async def get_user_join(id):
    ok = True
    try:
        await BotzHub(GetParticipantRequest(channel=channel, participant=id))
        ok = True
    except UserNotParticipantError:
        ok = False
    return ok


@BotzHub.on(events.ChatAction())
async def _(event):
    if on_join is False:
        return
    if event.user_joined or event.user_added:
        user = await event.get_user()
        chat = await event.get_chat()
        title = chat.title if chat.title else "this chat"
        pp = await BotzHub.get_participants(chat)
        count = len(pp)
        mention = f"[{get_display_name(user)}](tg://user?id={user.id})"
        name = user.first_name
        last = user.last_name
        if last:
            fullname = f"{name} {last}"
        else:
            fullname = name
        uu = user.username
        if uu:
            username = f"@{uu}"
        else:
            username = mention
        x = await get_user_join(user.id)
        if x is True:
            msg = welcome_msg.format(mention=mention, title=title, fullname=fullname, username=username, name=name, last=last, channel=f"@{channel}")
            butt = [Button.url("Channel", url=f"https://t.me/{channel}")]
        else:
            msg = welcome_not_joined.format(mention=mention, title=title, fullname=fullname, username=username, name=name, last=last, channel=f"@{channel}")
            butt = [Button.url("Channel", url=f"https://t.me/{channel}"), Button.inline("അഴിച്ചു വിട് 🐣", data=f"unmute_{user.id}")]
            await BotzHub.edit_permissions(event.chat.id, user.id, until_date=None, send_messages=False)
        
        await event.reply(msg, buttons=butt)


@BotzHub.on(events.NewMessage(incoming=True))
async def mute_on_msg(event):
    if event.is_private:
        return
    if on_new_msg is False:
        return
    x = await get_user_join(event.sender_id)
    temp = await BotzHub(GetFullUserRequest(event.sender_id))
    if x is False:
        if temp.user.bot:
            return
        nm = temp.user.first_name
        try:
            await BotzHub.edit_permissions(event.chat.id, event.sender_id, until_date=None, send_messages=False)
        except Exception as e:
            print(str(e))
            return
        await event.reply(f"പൂയ് {nm}, നീ നമ്മുടെ ചാനൽ സബ്സ്ക്രൈബ് ചെയ്തട്ടില്ല 🔕. അതില് ജോയിൻ അയേച്ചും വാ 🔔 , എന്നിട്ട് താഴെ അഴിച്ചു വിട് ബട്ടൺ അമർത്തി നോക്ക്.. ഇന്നാ നമ്മുടെ ചാനൽ ലിങ്ക് 🔗 @{channel} ", buttons=[[Button.url("Channel", url=f"https://t.me/{channel}")], [Button.inline("അഴിച്ചു വിട് 🐣", data=f"unmute_{event.sender_id}")]])


@BotzHub.on(events.callbackquery.CallbackQuery(data=re.compile(b"unmute_(.*)")))
async def _(event):
    uid = int(event.data_match.group(1).decode("UTF-8"))
    if uid == event.sender_id:
        x = await get_user_join(uid)
        nm = (await BotzHub(GetFullUserRequest(uid))).user.first_name
        if x is False:
            await event.answer(f"എടാ നീ ചാനലിൽ ചേർന്നില്ലെടാ! 🥺 @{channel} ", cache_time=0, alert=True)
        elif x is True:
            try:
                await BotzHub.edit_permissions(event.chat.id, uid, until_date=None, send_messages=True)
            except Exception as e:
                print(str(e))
                return
            msg = f"Welcome to {(await event.get_chat()).title}, {nm}!\nGood to see you here!"
            butt = [Button.url("Channel", url=f"https://t.me/{channel}")]
            await event.edit(msg, buttons=butt)
    else:
        await event.answer("എടാ നീ  പറഞ്ഞോ നീ നുമ്മടെ സബ്സ്ക്രൈബ്ർ അല്ലെ 🌚", cache_time=0, alert=True)



# https://docs.pyrogram.org/start/examples/bot_keyboards
# Reply with inline keyboard
@Jebot.on_message( filters.text
                   & ~filters.edited
                   & filters.regex(YTDL_REGEX))
async def ytdl_with_button(_, message: Message):
    await message.reply_text(
        "**ഏതേലും ഒന്ന് കൊടുക്കടെ**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "സംഗീതം 🎧",
                        callback_data="ytdl_audio"
                    ),
                    InlineKeyboardButton(
                        "വീഡിയോ 🎟",
                        callback_data="ytdl_video"
                    )
                ]
            ]
        ),
        quote=True
    )


@Jebot.on_callback_query(filters.regex("^ytdl_audio$"))
async def callback_query_ytdl_audio(_, callback_query):
    try:
        url = callback_query.message.reply_to_message.text
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': '%(title)s - %(extractor)s-%(id)s.%(ext)s',
            'writethumbnail': True
        }
        with YoutubeDL(ydl_opts) as ydl:
            message = callback_query.message
            await message.reply_chat_action("typing")
            info_dict = ydl.extract_info(url, download=False)
            # download
            await callback_query.edit_message_text("**Downloading audio...**")
            ydl.process_info(info_dict)
            # upload
            audio_file = ydl.prepare_filename(info_dict)
            task = asyncio.create_task(send_audio(message, info_dict,
                                                  audio_file))
            while not task.done():
                await asyncio.sleep(3)
                await message.reply_chat_action("upload_document")
            await message.reply_chat_action("cancel")
            await message.delete()
    except Exception as e:
        await message.reply_text(e)
    await callback_query.message.reply_to_message.delete()
    await callback_query.message.delete()


async def send_audio(message: Message, info_dict, audio_file):
    basename = audio_file.rsplit(".", 1)[-2]
    # .webm -> .weba
    if info_dict['ext'] == 'webm':
        audio_file_weba = basename + ".weba"
        os.rename(audio_file, audio_file_weba)
        audio_file = audio_file_weba
    # thumbnail
    thumbnail_url = info_dict['thumbnail']
    thumbnail_file = basename + "." + \
        get_file_extension_from_url(thumbnail_url)
    # info (s2tw)
    webpage_url = info_dict['webpage_url']
    title = '@vadakinipura '+s2tw(info_dict['title'])
    caption = f"<b><a href=\"{webpage_url}\">{title}</a></b>"
    duration = int(float(info_dict['duration']))
    performer = s2tw(info_dict['uploader'])
    await message.reply_audio(audio_file, caption=caption, duration=duration,
                              performer=performer, title=title,
                              parse_mode='HTML', thumb=thumbnail_file)
    os.remove(audio_file)
    os.remove(thumbnail_file)


@Jebot.on_callback_query(filters.regex("^ytdl_video$"))
async def callback_query_ytdl_video(_, callback_query):
    try:
        # url = callback_query.message.text
        url = callback_query.message.reply_to_message.text
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': '%(title)s - %(extractor)s-%(id)s.%(ext)s',
            'writethumbnail': True
        }
        with YoutubeDL(ydl_opts) as ydl:
            message = callback_query.message
            await message.reply_chat_action("typing")
            info_dict = ydl.extract_info(url, download=False)
            # download
            await callback_query.edit_message_text("**Downloading video...**")
            ydl.process_info(info_dict)
            # upload
            video_file = ydl.prepare_filename(info_dict)
            task = asyncio.create_task(send_video(message, info_dict,
                                                  video_file))
            while not task.done():
                await asyncio.sleep(3)
                await message.reply_chat_action("upload_document")
            await message.reply_chat_action("cancel")
            await message.delete()
    except Exception as e:
        await message.reply_text(e)
    await callback_query.message.reply_to_message.delete()
    await callback_query.message.delete()


async def send_video(message: Message, info_dict, video_file):
    basename = video_file.rsplit(".", 1)[-2]
    # thumbnail
    thumbnail_url = info_dict['thumbnail']
    thumbnail_file = basename + "." + \
        get_file_extension_from_url(thumbnail_url)
    # info (s2tw)
    webpage_url = info_dict['webpage_url']
    title = '@vadakinipura '+s2tw(info_dict['title'])
    caption = f"<b><a href=\"{webpage_url}\">{title}</a></b>"
    duration = int(float(info_dict['duration']))
    width, height = get_resolution(info_dict)
    await message.reply_video(
        video_file, caption=caption, duration=duration,
        width=width, height=height, parse_mode='HTML',
        thumb=thumbnail_file,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Save ✅",
                        callback_data="forward_video"
                    )
                ]
            ]
        ))
    os.remove(video_file)
    os.remove(thumbnail_file)


def get_file_extension_from_url(url):
    url_path = urlparse(url).path
    basename = os.path.basename(url_path)
    return basename.split(".")[-1]


def get_resolution(info_dict):
    if {"width", "height"} <= info_dict.keys():
        width = int(info_dict['width'])
        height = int(info_dict['height'])
    # https://support.google.com/youtube/answer/6375112
    elif info_dict['height'] == 1080:
        width = 1920
        height = 1080
    elif info_dict['height'] == 720:
        width = 1280
        height = 720
    elif info_dict['height'] == 480:
        width = 854
        height = 480
    elif info_dict['height'] == 360:
        width = 640
        height = 360
    elif info_dict['height'] == 240:
        width = 426
        height = 240
    return (width, height)


@Jebot.on_callback_query(filters.regex("^forward_video$"))
async def callback_query_forward_video(_, callback_query):
    m_edited = await callback_query.message.edit_reply_markup(None)
    m_cp = await m_edited.copy(CHANNEL_FORWARD_TO,
                               disable_notification=True)
    await callback_query.answer("Saved!")
    await m_edited.reply(m_cp.link, quote=True)

@Jebot.on_callback_query()
async def button(bot, update):
      cb_data = update.data
      if "help" in cb_data:
        await update.message.delete()
        await help(bot, update.message)
      elif "about" in cb_data:
        await update.message.delete()
        await about(bot, update.message)
      elif "start" in cb_data:
        await update.message.delete()
        await start(bot, update.message)

print(
    """
Bot Started!
"""
)

Jebot.run()
