import time

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

                    like = bot.like_comment(comment["pk"])
                    if like is True :
                        bot.reply_to_comment(post, message, comment["pk"], comment["user_id"]) 
                      
            else :
                print("NO esta comentado el POST: "+ post)
                
        return print("Operacion realizada!")



