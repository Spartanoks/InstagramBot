from app.models.service.implements.CommentImpl import CommentImpl

class ICommentService :
    def hateComment(bot, username, message) :
        return CommentImpl.hateComment(bot, username, message)

    def autoReply(bot, message):
        return CommentImpl.autoReply(bot, message)