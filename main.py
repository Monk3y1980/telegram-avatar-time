import time
# Библиотека telethon - https://docs.telethon.dev/en/latest/
from telethon import TelegramClient
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from config.config import api_hash, api_id
from utils.utils import time_has_changed, generate_time_image_bytes
from datetime import datetime, timedelta
# https://docs.python.org/3/library/argparse.html
import argparse
# https://pypi.org/project/pytz/
import pytz


def valid_tz(region):
    try:
        return pytz.timezone(region)
    except:
        msg = "Not a valid tz: '{0}'.".format(region)
        raise argparse.ArgumentTypeError(msg)


parser = argparse.ArgumentParser()
parser.add_argument("--api_id", required=False, help="user api ID", type=str, default=api_id)
parser.add_argument("--api_hash", required=False, help="user api Hash", type=str, default=api_hash)
parser.add_argument("--tz", required=False, help="user api Hash", type=valid_tz, default=valid_tz('Europe/Berlin'))

args = parser.parse_args()

client = TelegramClient("AvatarTime", args.api_id, args.api_hash)
client.start()


async def main():
    prev_update_time = datetime.now() - timedelta(minutes=1)

    while True:
        if time_has_changed(prev_update_time):
            bts = generate_time_image_bytes(datetime.now(args.tz).replace(tzinfo=None))
            await client(DeletePhotosRequest(await client.get_profile_photos('me')))
            file = await client.upload_file(bts)
            await client(UploadProfilePhotoRequest(file))
            prev_update_time = datetime.now()
            time.sleep(1)


if __name__ == '__main__':
    import asyncio

    asyncio.get_event_loop().run_until_complete(main())