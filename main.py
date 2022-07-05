from flask import Flask, request, abort
from google.cloud import pubsub_v1
import os

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


line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

project_id = "wingwill-demo-lab-jeff"
topic_id = "line_pubsub"


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

@app.route("/get_users", methods=['GET'])
def get_users():
    
    test_result = line_bot_api.get_followers_ids()
    print(test_result.user_ids)
    print(test_result.next)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # publisher = pubsub_v1.PublisherClient()
    # topic_path = publisher.topic_path(project_id, topic_id)
    # data_str = event.message.text
    # data = data_str.encode("utf-8")
    # future = publisher.publish(topic_path, data)
    # print(f"Published messages to {topic_path}.")
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

@handler.add(MessageEvent, message=TextMessage)
def handle_pubsub(event):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    data_str = event.message.text
    data = data_str.encode("utf-8")
    future = publisher.publish(topic_path, data)
    print(f"Published messages to {topic_path}.")
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    app.run()