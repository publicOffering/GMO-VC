import os
import boto3
import requests
import json

USE_FOR_UPDATE = "UPDATE"
USE_FOR_READ = "READ"

ssm = boto3.client('ssm')

from linebot import (
    LineBotApi, 
)
from linebot.models import (
    TextSendMessage, 
)

#レート割合の有効桁数を設定
from decimal import *
getcontext().prec = 3

#ラインでメッセージプッシュ
def line_push_text_message(send_text):
    line_bot_api = LineBotApi(channel_access_token=get_param('GMO_VC_LINE_CHANNEL_ACCESS_TOKEN'))
    line_bot_api.push_message(get_param('GMO_VC_LINE_MY_USER_ID'), TextSendMessage(text=send_text))
    return 0

#パラメータストア
def get_param(param):
    return ssm.get_parameter(Name=param).get('Parameter').get('Value')

#現物取引かレバレッジ取引か判定
def spot_trading(currency_type):
    #現物取引の判別。GMOだとシンボルが3文字のものが現物取引。レバレッジはBTC_JPYみたいに長くなる。
    return True if len(currency_type["symbol"])==3 else False

#DynamoDBのテーブル情報取得
#https://qiita.com/is_ryo/items/74f3fc70b7602888a2ac
def get_dynamoDBtable(table_name):
    try:
      dynamoDB = boto3.resource("dynamodb")
      #SAMで作成したDynamoDBのテーブル名取得(環境変数を使う)
      #https://www.ketancho.net/entry/2018/01/04/083000
      table = dynamoDB.Table(os.getenv(table_name))
    except Exception as e:
          print(e)
    return table

def get_current_rate_with_json_format():
    return requests.get('https://api.coin.z.com/public' + '/v1/ticker?symbol').json()

def get_VCname_rate(currency_type):
    VCname = json.dumps(currency_type["symbol"]).strip("\"")
    rate = Decimal(json.dumps(currency_type["bid"]).strip("\""))
    return VCname, rate

def get_current_rate_from_market():
    current_rate_response= requests.get('https://api.coin.z.com/public' + '/v1/ticker?symbol').json()

    #ifも使った内包表記
    #https://atmarkit.itmedia.co.jp/ait/articles/2107/06/news020.html
    dict = {json.dumps(currency["symbol"]).strip("\""): Decimal(json.dumps(currency["bid"]).strip("\"")) \
        for currency in current_rate_response["data"] if spot_trading(currency)}

    return dict

def get_daily_rate_from_dynamoDB():
    current_rate_dict = get_current_rate_from_market()
    SpotTradingVcNameList= [key for key in current_rate_dict.keys()]

    vc_daily_rate_table = get_dynamoDBtable('VcRateTableName')
    try:
        dict = {SpotTradingVcName: vc_daily_rate_table.get_item(Key={'VCname': SpotTradingVcName+"_Daily"}).get('Item').get('rate') \
            for SpotTradingVcName in SpotTradingVcNameList}
    except Exception as e :
        line_push_text_message("DynamoDBからの読み取りに失敗しています。仮想通貨のレートが多分入ってません")

    return dict
