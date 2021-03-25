
class Target :

    def getUserIdFromUsername(bot, username):
        return bot.get_user_id_from_username(username)

    def getUsernameFromId(bot, user_id):
        return bot.get_username_from_user_id(user_id)