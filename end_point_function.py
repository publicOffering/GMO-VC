import common_func as gmo_vc
import datetime
from decimal import *
import json
#https://resanaplaza.com/2021/07/23/%E3%80%90%E8%89%AF%E3%81%8F%E5%88%86%E3%81%8B%E3%82%8B%E3%80%91python-logger%E3%81%AE-%E4%BD%BF%E3%81%84%E6%96%B9%E3%81%A8%E6%B3%A8%E6%84%8F%E7%82%B9/#i
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, PostbackEvent, TemplateSendMessage, ButtonsTemplate, PostbackAction
)

handler = WebhookHandler(gmo_vc.get_param('GMO_VC_LINE_CHANNEL_SECRET'))
line_bot_api = LineBotApi(gmo_vc.get_param('GMO_VC_LINE_CHANNEL_ACCESS_TOKEN'))

def lambda_handler(event, context):
    print("hander was called")
    headers = event["headers"]
    body = event["body"]

    # get X-Line-Signature header value
    signature = headers['x-line-signature']

    # handle webhook body
    handler.handle(body, signature)

    return {"statusCode": 200, "body": "OK"}


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="メニューから選んでください。"))

#postbackメソッドの対応
#https://qiita.com/w2or3w/items/fbe588d7147bb8e65628
@handler.add(PostbackEvent)
def on_postback(line_event):
    data = line_event.postback.data
    if data == gmo_vc.get_param('GMO_VC_MENU_A'):
        reply = menu_confirm_current_rate()
#    elif data == gmo_vc.get_param('GMO_VC_MENU_F'):
#        reply = menu_confirm_current_rate2()
    else:
        reply = "聞いています"

    if isinstance(reply, str):
        line_bot_api.reply_message(line_event.reply_token, TextSendMessage(reply))
    else :
        line_bot_api.reply_message(line_event.reply_token, reply)

    logger.info(line_bot_api.get_profile(line_event.source.user_id))
    return 0

def menu_confirm_current_rate():
    logger.info("menu_confirm_current_rate was called")
    #時差を加味して出力日を設定
    DIFF_JST_FROM_UTC = 9
    dt_now = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)

    current_rate_dict = gmo_vc.get_current_rate_from_market()
    daily_rate_dict = gmo_vc.get_daily_rate_from_dynamoDB()

    result = dt_now.strftime('%Y/%m/%d') + ("\n")
    for VCname, current_rate in current_rate_dict.items():
        result += VCname + ("新: ") + str(current_rate) + (" 旧: ") + str(daily_rate_dict[VCname]) + ("\n 前日比 ") + str(current_rate/daily_rate_dict[VCname]*100) + ("％\n")

    return result


    


