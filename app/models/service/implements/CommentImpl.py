from app.models.dao.Comment import Comment

class CommentImpl :
    
     def hateComment(bot, target, message) :
         return Comment.hateComment(bot, target, message)