from os import remove
import os
from instabot import Bot
from app.applicationProperties import appProperties

if os.path.isfile("config/gudrizimlu_uuid_and_cookie.json") :
    remove("config/gudrizimlu_uuid_and_cookie.json")
class Auth :

    bot = Bot(
        comment_delay=0,
        like_delay=0,
        unlike_delay=0,
        follow_delay=0,
        unfollow_delay=0,
        block_delay=0,
        unblock_delay=0,
        message_delay=0,
        max_comments_per_day=10000000000000000,
        max_likes_per_day=10000000000000000,
        max_follows_per_day=10000000000000000,
        max_unfollows_per_day=10000000000000000,
        max_likes_to_like=10000000000000000,
        max_followers_to_follow=10000000000000,
        max_messages_per_day=10000000000000
    )
    bot.login(username=appProperties.USER_EMAIL, password=appProperties.USER_PASSWORD)
