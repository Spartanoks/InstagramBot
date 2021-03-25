
class Post:

    def uploadStoryPhoto(bot, photo) :
        upload = bot.upload_story_photo(photo)
        if upload is True :
            print('Foto subida a la Historia con Exito!')
        else :
            print('No se pudo subir la foto'+ photo +' a la Historia con Exito!')
        return print('Operacion finalizada!')

    def uploadPhoto(bot, photo) :
        upload = bot.upload_photo(photo)
        if upload is True :
            print('Post realizado con Exito!')
        else :
            print('No se pudo subir la foto'+ photo +'!')
        return print('Operacion finalizada!')
