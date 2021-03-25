import time
from app.models.dao.Messages import Message
from app.models.dao.Target import Target

class Comment :

    def hateComment(bot,target, message) :

        posts = bot.get_total_user_medias(target)
        
        for post in posts:
            
           
            msg = bot.comment(post, message)
            
            if msg is True :
                print('POST: ' + post + ' Comentado')
                time.sleep(2)
            else : 
                print('No se pudo comentar el POST: '+ post)
        return print('Operacion realizada, comentarios hechos')
    
    def getComments(bot, post) :
        return bot.get_media_comments_all(post)



    def autoReply(bot, posts, message) :
        
        for post in posts :

            if bot.is_commented(post):
                print("Respondiendo el POST: "+ post)
                for comment in Comment.getComments(bot, post) :

                    if Target.getUsernameFromId(bot,bot.user_id) != Target.getUsernameFromId(bot,comment["user_id"]) :
                        like = bot.like_comment(comment["pk"])
                        time.sleep(3)
                        if like is True :
                            bot.reply_to_comment(post, message, comment["pk"], comment["user_id"]) 
                            Message.sendMessage(bot, Message.textMessage(), str(comment["user_id"]))
                            time.sleep(2)
                      
            else :
                print("NO esta comentado el POST: "+ post)
                
        return print("Operacion realizada!")



