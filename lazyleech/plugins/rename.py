# lazyleech - Telegram bot primarily to leech from torrents and upload to Telegram
# Copyright (c) 2021 lazyleech developers <theblankx protonmail com, meliodas_bot protonmail com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import html
import math
import os
import re
import time

from pyrogram import Client, filters

from .. import ALL_CHATS


@Client.on_message(filters.command('rename') & filters.chat(ALL_CHATS))
async def rename(client, message):
    c_time = time.time()
    name = message.text.split(None, 1)[1]
    available_media = ("audio", "document", "photo", "sticker", "animation", "video", "voice", "video_note")
    download_message = None
    for i in available_media:
        if getattr(message, i, None):
            download_message = message
            break
    else:
        reply = message.reply_to_message
        if not getattr(reply, 'empty', True):
            for i in available_media:
                if getattr(reply, i, None):
                    download_message = reply
                    break
    if download_message is None:
        await message.reply_text('Media required')
        return
    msg = await message.reply_text('<code>Downloading</code>')
    filepath = os.path.join(str(message.from_user.id), name)
    await download_message.download(filepath)
    await asyncio.sleep(5)
    await msg.edit_text('<code>Uploading</code>')
    await message.reply_document(filepath, caption=name)
    await msg.delete()
    os.remove(filepath)