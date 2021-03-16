
from models.service.ICommentService import ICommentService
from models.dao.Auth import *
from models.service.ITargetService import ITargetService
from app.applicationProperties import appProperties
from models.dao.Messages import Message

bot = Auth.bot
class Main :
    def getUserId():
        user_id = ITargetService.getUserIdFromUsername(bot, appProperties.TARGET)
        return print(user_id)

    def hateComment():
        
        return ICommentService.hateComment(bot, appProperties.TARGET, Message.hateMessage())
    