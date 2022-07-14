import os

from linebot import (
    LineBotApi
)

line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])

test_result = line_bot_api.get_followers_ids()
test_user = test_result[0]
profile = line_bot_api.get_profile(test_user)

print(profile.display_name)
print(profile.user_id)
print(profile.picture_url)
print(profile.status_message)