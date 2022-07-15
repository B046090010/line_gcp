from flask import Flask, request, abort
from google.cloud import pubsub_v1
import os
import json

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent, UnfollowEvent
)

app = Flask(__name__)


# line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

project_id = "wingwill-demo-lab-jeff"
topic_id = "line_pubsub"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

@app.route("/", methods=['POST'])
def hello_world():
    return 'OK'

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


# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
    
#     output = {
#         'id':  event.message.id,
#         'text': event.message.text, 
#         'timestamp': event.timestamp,
#         'source_user': event.source.user_id
#     }
    
#     print(output)
#     output = json.dumps(output).encode("utf-8")

#     future = publisher.publish(topic_path, output)
#     print(f"Published messages to {topic_path}.")

@handler.add(FollowEvent)
def handle_follow(follwer):
    # do something
    
    output = {
        'timestamp': follwer.timestamp,
        'source_user': follwer.source.user_id,
        'action': 'follow'
    }
    
    print(output)
    output = json.dumps(output).encode("utf-8")

    future = publisher.publish(topic_path, output)
    print(f"Published messages to {topic_path}.")

@handler.add(UnfollowEvent)
def handle_unfollow(unfollwer):
    # do something
    
    output = {
        'timestamp': unfollwer.timestamp,
        'source_user': unfollwer.source.user_id,
        'action': 'unfollow'
    }
    
    print(output)
    output = json.dumps(output).encode("utf-8")

    future = publisher.publish(topic_path, output)
    print(f"Published messages to {topic_path}.")

if __name__ == "__main__":
    app.run()