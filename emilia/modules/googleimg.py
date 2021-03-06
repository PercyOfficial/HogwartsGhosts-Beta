import os
import shutil
import glob
from re import findall
from bing_image_downloader import downloader
from telethon import *
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.types import *

from emilia import client
from emilia.events import register

from emilia import dispatcher

from emilia.modules.disable import DisableAbleCommandHandler
async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):

        return isinstance(
            (await client(functions.channels.GetParticipantRequest(chat, user))).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator)
        )
    elif isinstance(chat, types.InputPeerChat):

        ui = await client.get_peer_id(user)
        ps = (await client(functions.messages.GetFullChatRequest(chat.chat_id))) \
            .full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator)
        )
    else:
        return None


@register(pattern="^/img (.*)")
async def img_sampler(event):
     if event.fwd_from:
        return
     if event.is_group:
       if not (await is_register_admin(event.input_chat, event.message.sender_id)):
          await event.reply("ğ Hai.. You are not admin..ğ¤­ You can't use this command.. But you can use in my pmğ")
          return
     args = context.args
     query = str(args)
     jit = f'"{query}"'
     downloader.download(jit, limit=5, output_dir='store', adult_filter_off=False, force_replace=False, timeout=60)
     os.chdir(f'./store/"{query}"')
     types = ('*.png', '*.jpeg', '*.jpg') # the tuple of file types
     files_grabbed = []
     for files in types:
         files_grabbed.extend(glob.glob(files))
     await event.client.send_file(event.chat_id, files_grabbed, reply_to=event.id)
     os.remove(files_grabbed)
     os.chdir('./')

    
IMG_HANDLER = DisableAbleCommandHandler("img", img_sampler, pass_args=True, admin_ok=True)

dispatcher.add_handler(IMG_HANDLER)


__command_list__ = ["img"]
__handlers__ = [
    IMG_HANDLER
]
