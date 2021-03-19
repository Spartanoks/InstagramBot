from app.models.dao.Target import Target

class TargetImpl :
    
    def getUserIdFromUsername(bot, username) :
        return Target.getUserIdFromUsername(bot, username)