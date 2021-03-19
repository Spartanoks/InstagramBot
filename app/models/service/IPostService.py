from app.models.service.implements.PostImpl import PostImpl

class IPostService :

    def uploadStoryPhoto(bot, photo) :
        return PostImpl.uploadStoryPhoto(bot, photo)