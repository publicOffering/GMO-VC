import common_func as gmo_vc
from decimal import *
#https://resanaplaza.com/2021/07/23/%E3%80%90%E8%89%AF%E3%81%8F%E5%88%86%E3%81%8B%E3%82%8B%E3%80%91python-logger%E3%81%AE-%E4%BD%BF%E3%81%84%E6%96%B9%E3%81%A8%E6%B3%A8%E6%84%8F%E7%82%B9/#i
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    TextSendMessage, 
)

def lambda_handler(event, context):
    print("auto_trading hander was called")

    #現在レートの取得
    current_rate_response = gmo_vc.get_current_rate_with_json_format()

    #過去レートの取得

    #自動売り処理

    #自動買い処理


    #結果をメッセージ通知
    #line_bot_api = LineBotApi(channel_access_token=gmo_vc.get_param('GMO_VC_LINE_CHANNEL_ACCESS_TOKEN'))
    #line_bot_api.push_message(gmo_vc.get_param('GMO_VC_LINE_MY_USER_ID'), TextSendMessage(text="auto_trading hander was called"))

    return {"statusCode": 200, "body": "OK"}