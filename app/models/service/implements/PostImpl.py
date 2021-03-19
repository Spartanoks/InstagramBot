from app.models.dao.Post import Post

class PostImpl :

    def uploadStoryPhoto(bot, photo):
        return Post.uploadStoryPhoto(bot, photo)