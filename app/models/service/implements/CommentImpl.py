from app.models.service.ITargetService import ITargetService
from app.models.dao.Comment import Comment


class CommentImpl :
    
    def hateComment(bot, username, message) :
        target = ITargetService.getUserIdFromUsername(bot, username)
        return Comment.hateComment(bot, target, message)

    def autoReply(bot, message) :
        posts = bot.get_your_medias()
        return Comment.autoReply(bot, posts, message)
    