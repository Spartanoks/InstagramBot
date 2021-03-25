
class Message :

    def defaultMessage():
        return "Default Message!"

    def hateMessage():
        return "Son unos ESTAFADORES, al momento en el que le pagas, te bloquean y no realizan ningun pago, SON ESTAFADORES, NO LES COMPREN"

    def replyMessage():
        return '@[[username]] Hi'

    def textMessage() :
        return "Hi"

    def sendMessage(bot, message, target):
        return bot.send_message(message, target)

    def sendPhoto(bot, target, photo):
        return bot.send_photo(target, photo)

    def getMessages(bot):
        return bot.get_messages()

    def getInbox(bot) :
        inbox = []
        for messages in Message.getMessages(bot)["inbox"]["threads"] :
            chat = []
            chat.append("item_id", str(messages["items"][0]["item_id"]))
            chat.append("user_id", str(messages["items"][0]["user_id"]))
            chat.append("text", str(messages["items"][0]["text"]))
            inbox.append(chat)
          
        return inbox
            