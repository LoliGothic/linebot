from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi(
    '/EF+GGjKrbIUq9ph5Wt2XiyPLmT3+3aBpYNRFESKIWA2Pxq+HnlsiuSoqd9pjZGtnSjq9D53Om+9W0wU9SFzyk5piqhxGYtwit+eySTn7u18jdOiTfY2Hz65P6NyJrTMhYZ+GdpJKED+y1RCy7kXVAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('76c1a65f62b652e9e942b1b1a3efb7ce')


@app.route("/")
def test():
    return "OK"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "ありがとう":
        reply_message="どういたしまして"

    else:
        reply_message=f"あなたは{event.message.text}といいました．"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message))


if __name__ == "__main__":
    app.run()
