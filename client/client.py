from telethon.sync import TelegramClient
from telethon import events
import logging
from pathlib import Path
import secrets


api_id = secrets.API_ID
api_hash = secrets.API_HASH

phone = secrets.PHONE
username = secrets.USERNAME
searchStr = ['BLURAY', 'HDRIP', 'BRRIP']
series = ['דה וויס', 'חתונה ממבט ראשון']


class TgClient:

    def run(self):
        with TelegramClient('name', api_id, api_hash) as client:
            client.send_message('me', 'Server is UP!')
            client.allow_cache = False

            @client.on(events.NewMessage)
            async def my_event_handler(event):
                media = event.message.media
                # if media is None:
                    # print('not media: ' + str(event.raw_text))
                if media is not None:
                    if hasattr(media, 'document'):
                        try:
                            _fileName = media.document.attributes[0]\
                                .file_name.upper()
                            if any(x in _fileName for x
                                   in searchStr) \
                                    and ('2019' or '2020') in _fileName:
                                await download(media, _fileName)

                         #   if any(x in _fileName for x
                         #          in series) and '720' in _fileName:
                        #      await download(media, _fileName)

                            if event.chat_id == secrets.CHAT_ID:
                                await download(media, _fileName)

                        except Exception as inst:
                            logging.info(media.document.mime_type)
                            # await client.send_message('me', event.message)
                    # else:
                        # print('skipping: ' + str(event.raw_text))
                        # await event.forward_to('me')

            async def download(media, fileName):
                try:
                    logging.info("Start download: " + fileName)
                    await client.send_message('me', 'Start download: '
                                              + fileName)
                    my_file = Path('C:/Users/moran/Downloads/Telegram Desktop/'
                                   + fileName)
                    if my_file.exists():
                        logging.info('DownLoad Skipped, file exists ' +
                                     fileName)
                        await client.send_message('me', 'DownLoad Skipped, '
                                                  'file exists - ' + fileName)
                        return
                    download_res = await client.download_media(
                        media, 'C:/Users/moran/Downloads/Telegram Desktop')
                    await client.send_message('me', 'DownLoad Done: ' +
                                              str(download_res))
                    logging.info("Download done: " + str(download_res))
                except Exception as inst:
                    await client.send_message('me', 'DownLoad Failed!!! '
                                              + fileName)
                    logging.exception(inst)
                    logging.info(fileName + " - DownLoad Failed!!! ")

            client.run_until_disconnected()