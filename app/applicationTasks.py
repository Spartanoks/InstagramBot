
from app.models.service.ICommentService import ICommentService
from app.models.dao.Auth import *
from app.models.service.ITargetService import ITargetService
from app.applicationProperties import appProperties
from app.models.dao.Messages import Message
from app.models.service.IPostService import IPostService
import os
from PIL import Image

bot = Auth.bot
class Main :
    def getUserId():
        user_id = ITargetService.getUserIdFromUsername(bot, appProperties.TARGET)
        return print(user_id)

    def hateComment():
        
        return ICommentService.hateComment(bot, appProperties.TARGET, Message.hateMessage())

    def uploadStory() :
        photo = 'app/resources/img/lego.jpg'
        return IPostService.uploadStoryPhoto(bot, photo)

    def autoReply() :
        return ICommentService.autoReply(bot, Message.replyMessage())


    
    