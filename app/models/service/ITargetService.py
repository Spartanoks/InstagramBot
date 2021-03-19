from app.models.service.implements.TargetImpl import TargetImpl

class ITargetService :

    def getUserIdFromUsername(bot, username):
        return TargetImpl.getUserIdFromUsername(bot, username)