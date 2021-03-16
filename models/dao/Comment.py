import time

class Comment :

    def hateComment(bot,target, message) :

        posts = bot.get_total_user_medias(target)
        
        for post in posts:
            
            time.sleep(2)
            msg = bot.comment(post, message)
            
            if msg is True :
                print('POST: ' + post + ' Comentado')
            else : 
                print('No se pudo comentar el POST: '+ post)
        return print('Operacion realizada, comentarios hechos')
        


