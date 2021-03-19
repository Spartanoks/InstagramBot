from instabot import Bot
from app.applicationProperties import appProperties

class Auth :

    bot = Bot(
        comment_delay=0,
        max_comments_per_day=100000
    )
    bot.login(username=appProperties.USER_EMAIL, password=appProperties.USER_PASSWORD)
