import common_func as gmo_vc
import boto3
import requests
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
    TextSendMessage, 
)

def lambda_handler(event, context):
    print("daily_report hander was called")
 
    current_rate_dict = gmo_vc.get_current_rate_from_market()
    daily_rate_dict = gmo_vc.get_daily_rate_from_dynamoDB()

    vc_rate_table = gmo_vc.get_dynamoDBtable('VcRateTableName')

    result = "以下の通り現在時刻で更新\n"
    for VCname, current_rate in current_rate_dict.items():
        vc_rate_table.put_item(Item={'VCname': VCname+"_Daily", 'rate': current_rate})
        print(VCname)
        print(type(VCname))
        print(current_rate)
        print(type(current_rate))
        print(daily_rate_dict[VCname])
        print(type(daily_rate_dict[VCname]))
        result += VCname + ("新: ") + str(current_rate) + (" 旧: ") + str(daily_rate_dict[VCname]) + ("\n 前日比 ") + str(current_rate/daily_rate_dict[VCname]*100) + ("％\n")

#vc_rate_table.put_item(Item={'VCname': VCname+"_Daily", 'rate': str(rate)})

    #閾値とラインのメッセージ回数も出力したいな

    #LINEでメッセージ通知
    gmo_vc.line_push_text_message(result)

    return {"statusCode": 200, "body": "OK"}
