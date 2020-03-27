from telethon.sync import TelegramClient
from telethon import events
import logging
from pathlib import Path
import secrets
import time
from telethon.errors import FloodWaitError
import os


api_id = secrets.API_ID
api_hash = secrets.API_HASH

phone = secrets.PHONE
username = secrets.USERNAME
searchStr = ['BLURAY', 'HDRIP', 'BRRIP']
series = ['דה וויס', 'חתונה ממבט ראשון']
DOWNLOAD_DIR = "C:/Plex/Movies"
MOVIES_FILE_NAME = 'movies.txt'


class TgClient:

    def run(self):
        if not os.path.isfile(MOVIES_FILE_NAME):
            with open(MOVIES_FILE_NAME, "a+") as f:
                f.write('*******' + '\n')
        with TelegramClient('name', api_id, api_hash) as client:
            client.send_message('me', 'Server is UP!')
            client.allow_cache = False

            @client.on(events.NewMessage)
            async def my_event_handler(event):
                media = event.message.media
                _from = None
                if event.is_channel:
                    _from = event.chat.title
                if event.is_private:
                    _from = event.chat.first_name
                if media is not None and hasattr(media, 'document'):
                    if hasattr(media, 'document'):
                        try:
                            _fileName = media.document.attributes[0]\
                                .file_name.upper()
                            if any(x in _fileName for x
                                   in searchStr) \
                                    and ('2019' or '2020') in _fileName:
                                await download(media, _fileName, _from)
                            else:
                                if event.chat_id == secrets.CHAT_ID:
                                    await download(media, _fileName, _from)

                        except Exception as inst:
                            logging.info(media.document.mime_type + ' ' +
                                         event.chat.title)
                            # await client.send_message('me', event.message)
                    # else:
                        # print('skipping: ' + str(event.raw_text))
                        # await event.forward_to('me')

            async def download(media, fileName, channel=None):
                try:
                    logging.info("Start download: " + fileName + ' From: ' +
                                 str(channel))
                    await client.send_message('me', 'Start download: '
                                              + fileName)

                    with open(MOVIES_FILE_NAME, 'r', encoding='utf-8') as f:
                        _movies = f.readlines()
                        if fileName in _movies:
                            logging.info('DownLoad Skipped, file exists ' +
                                         fileName)
                            await client.send_message('me',
                                                      'DownLoad Skipped, '
                                                      'file exists '
                                                      + fileName)
                            return

                    with open(MOVIES_FILE_NAME, 'a', encoding='utf-8') as file:
                        file.write(f'\n{fileName}')

                    download_res = \
                        await client.download_media(media, DOWNLOAD_DIR)
                    await client.send_message('me', 'DownLoad Done: ' +
                                              str(download_res))
                    logging.info("Download done: " + str(download_res))
                except FloodWaitError as ex:
                    logging.log(logging.INFO, '%s: flood wait')
                    time.sleep(ex.seconds)
                    await download(media, fileName)
                except Exception as inst:
                    await client.send_message('me', 'DownLoad Failed!!! '
                                              + fileName)
                    logging.exception(inst)
                    logging.info(fileName + " - DownLoad Failed!!! ")

            client.run_until_disconnected()
