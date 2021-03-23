from __future__ import unicode_literals

import json
import os
import shutil
import time
import imghdr
import struct
import random
from uuid import uuid4
from random import randint

from requests_toolbelt import MultipartEncoder

from . import config
from .api_photo import get_image_size, stories_shaper







def download_story(self, filename, story_url, username):
    path = "stories/{}".format(username)
    if not os.path.exists(path):
        os.makedirs(path)
    fname = os.path.join(path, filename)
    if os.path.exists(fname):  # already exists
        self.logger.info("Stories already downloaded...")
        return os.path.abspath(fname)
    response = self.session.get(story_url, stream=True)
    if response.status_code == 200:
        with open(fname, "wb") as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
        return os.path.abspath(fname)


def upload_story_photo_old(self, photo, upload_id=None):
    if upload_id is None:
        upload_id = str(int(time.time() * 1000))
    photo = stories_shaper(photo)
    if not photo:
        return False

    with open(photo, "rb") as f:
        photo_bytes = f.read()

    data = {
        "upload_id": upload_id,
        "_uuid": self.uuid,
        "_csrftoken": self.token,
        "image_compression": '{"lib_name":"jt","lib_version":"1.3.0",'
        + 'quality":"87"}',
        "photo": (
            "pending_media_%s.jpg" % upload_id,
            photo_bytes,
            "application/octet-stream",
            {"Content-Transfer-Encoding": "binary"},
        ),
    }
    m = MultipartEncoder(data, boundary=self.uuid)
    self.session.headers.update(
        {
            "Accept-Encoding": "gzip, deflate",
            "Content-type": m.content_type,
            "Connection": "close",
            "User-Agent": self.user_agent,
        }
    )
    response = self.session.post(config.API_URL + "rupload_igphoto/", data=m.to_string())

    if response.status_code == 200:
        upload_id = json.loads(response.text).get("upload_id")
        if self.configure_story(upload_id, photo):
            # self.expose()
            return True
    return False


def configure_story(self, upload_id, photo):
    (w, h) = get_image_size(photo)
    data = self.json_data(
        {
            "source_type": 4,
            "upload_id": upload_id,
            "story_media_creation_date": str(int(time.time()) - randint(11, 20)),
            "client_shared_at": str(int(time.time()) - randint(3, 10)),
            "client_timestamp": str(int(time.time())),
            "configure_mode": 1,  # 1 - REEL_SHARE, 2 - DIRECT_STORY_SHARE
            "device": self.device_settings,
            "edits": {
                "crop_original_size": [w * 1.0, h * 1.0],
                "crop_center": [0.0, 0.0],
                "crop_zoom": 1.3333334,
            },
            "extra": {"source_width": w, "source_height": h},
        }
    )
    return self.send_request("media/configure_to_story/?", data)

def resize_image(fname):
    from math import ceil

    try:
        from PIL import Image, ExifTags
    except ImportError as e:
        print("ERROR: {err}".format(err=e))
        print(
            "Required module `PIL` not installed\n"
            "Install with `pip install Pillow` and retry"
        )
        return False
    print("Analizing `{fname}`".format(fname=fname))
    h_lim = {"w": 90.0, "h": 47.0}
    v_lim = {"w": 4.0, "h": 5.0}
    img = Image.open(fname)
    (w, h) = img.size
    deg = 0
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == "Orientation":
                break
        exif = dict(img._getexif().items())
        o = exif[orientation]
        if o == 3:
            deg = 180
        if o == 6:
            deg = 270
        if o == 8:
            deg = 90
        if deg != 0:
            print("Rotating by {d} degrees".format(d=deg))
            img = img.rotate(deg, expand=True)
            (w, h) = img.size
    except (AttributeError, KeyError, IndexError) as e:
        print("No exif info found (ERR: {err})".format(err=e))
        pass
    img = img.convert("RGBA")
    ratio = w * 1.0 / h * 1.0
    print("FOUND w:{w}, h:{h}, ratio={r}".format(w=w, h=h, r=ratio))
    if w > h:
        print("Horizontal image")
        if ratio > (h_lim["w"] / h_lim["h"]):
            print("Cropping image")
            cut = int(ceil((w - h * h_lim["w"] / h_lim["h"]) / 2))
            left = cut
            right = w - cut
            top = 0
            bottom = h
            img = img.crop((left, top, right, bottom))
            (w, h) = img.size
        if w > 1080:
            print("Resizing image")
            nw = 1080
            nh = 1334
            img = img.resize((nw, nh), Image.ANTIALIAS)
    elif w < h:
        print("Vertical image")
        if ratio < (v_lim["w"] / v_lim["h"]):
            print("Cropping image")
            cut = int(ceil((h - w * v_lim["h"] / v_lim["w"]) / 2))
            left = 0
            right = w
            top = cut
            bottom = h - cut
            img = img.crop((left, top, right, bottom))
            (w, h) = img.size
        if h > 1080:
            print("Resizing image")
            nw = 1080
            nh = 1334
            img = img.resize((nw, nh), Image.ANTIALIAS)
    else:
        print("Square image")
        if w > 1080:
            print("Resizing image")
            img = img.resize((1080, 1080), Image.ANTIALIAS)
    (w, h) = img.size
    new_fname = "{fname}.CONVERTED.jpg".format(fname=fname)
    print("Saving new image w:{w} h:{h} to `{f}`".format(w=w, h=h, f=new_fname))
    new = Image.new("RGB", img.size, (255, 255, 255))
    new.paste(img, (0, 0, w, h), img)
    new.save(new_fname, quality=95)
    return new_fname

def compatible_aspect_ratio(size):
    min_ratio, max_ratio = 4.0 / 5.0, 90.0 / 47.0
    width, height = size
    ratio = width * 1.0 / height * 1.0
    print("FOUND: w:{w} h:{h} r:{r}".format(w=width, h=height, r=ratio))
    return min_ratio <= ratio <= max_ratio



def upload_story_photo(
    self,
    photo,
    upload_id=None,
    from_video=False,
    options={},
):
    """Upload photo to Instagram

    @param photo         Path to photo file (String)
    @param caption       Media description (String)
    @param upload_id     Unique upload_id (String). When None, then generate
                         automatically
    @param from_video    A flag that signals whether the photo is loaded from
                         the video or by itself
                         (Boolean, DEPRECATED: not used)
    @param force_resize  Force photo resize (Boolean)
    @param options       Object with difference options, e.g.
                         configure_timeout, rename (Dict)
                         Designed to reduce the number of function arguments!
                         This is the simplest request object.

    @return Boolean
    """
    options = dict({"configure_timeout": 15, "rename": True}, **(options or {}))
    if upload_id is None:
        upload_id = str(int(time.time() * 1000))
    if not photo:
        return False
    if not compatible_aspect_ratio(get_image_size(photo)):
        self.logger.error("Photo does not have a compatible photo aspect ratio.")
        photo = resize_image(photo)

    waterfall_id = str(uuid4())
    # upload_name example: '1576102477530_0_7823256191'
    upload_name = "{upload_id}_0_{rand}".format(
        upload_id=upload_id, rand=random.randint(1000000000, 9999999999)
    )
    rupload_params = {
        "retry_context": '{"num_step_auto_retry":0,"num_reupload":0,"num_step_manual_retry":0}',
        "media_type": "1",
        "xsharing_user_ids": "[]",
        "upload_id": upload_id,
        "image_compression": json.dumps(
            {"lib_name": "moz", "lib_version": "3.1.m", "quality": "80"}
        ),
    }
    photo_data = open(photo, "rb").read()
    photo_len = str(len(photo_data))
    self.session.headers.update(
        {
            "Accept-Encoding": "gzip",
            "X-Instagram-Rupload-Params": json.dumps(rupload_params),
            "X_FB_PHOTO_WATERFALL_ID": waterfall_id,
            "X-Entity-Type": "image/jpeg",
            "Offset": "0",
            "X-Entity-Name": upload_name,
            "X-Entity-Length": photo_len,
            "Content-Type": "application/octet-stream",
            "Content-Length": photo_len,
            "Accept-Encoding": "gzip",
        }
    )
    response = self.session.post(
        "https://{domain}/rupload_igphoto/{name}".format(
            domain=config.API_DOMAIN, name=upload_name
        ),
        data=photo_data,
    )
    if response.status_code != 200:
        self.logger.error(
            "Photo Upload failed with the following response: {}".format(response)
        )
        return False
    if from_video:
    # Not configure when from_video is True
     return True    
    # CONFIGURE
    configure_timeout = options.get("configure_timeout")
    for attempt in range(4):
        if configure_timeout:
            time.sleep(configure_timeout)
        if self.configure_story(upload_id, photo):
            media = self.last_json.get("media")
            self.expose()
            if options.get("rename"):
                os.rename(photo, "{fname}.REMOVE_ME".format(fname=photo))
                os.remove("{fname}.REMOVE_ME".format(fname=photo))
            return media
    return False