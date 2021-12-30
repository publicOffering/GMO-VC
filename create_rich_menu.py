#https://developers.line.biz/ja/reference/messaging-api/#rich-menu

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, URIAction, PostbackAction
)
import line_token
import requests

line_bot_api = LineBotApi(line_token.TOKEN)

MENU_A='日次レート確認'
MENU_B='上昇閾値修正'
MENU_C='降下閾値修正'
MENU_D='口座情報確認'
MENU_E='手動買い'
MENU_F='手動売り'

#リッチメニューを作成する
rich_menu_to_create = RichMenu(
    size=RichMenuSize(width=2500, height=1680),
    selected=True,
    name="Nice richmenu",
    chat_bar_text="Tap here",
    areas=[RichMenuArea(bounds=RichMenuBounds(x=0, y=0, width=833, height=843),
        action=PostbackAction(label=MENU_A, display_text=MENU_A, data=MENU_A)),
        RichMenuArea(bounds=RichMenuBounds(x=834, y=0, width=833, height=843),
        action=PostbackAction(label=MENU_B, display_text=MENU_B, data=MENU_B)),
        RichMenuArea(bounds=RichMenuBounds(x=1667, y=0, width=833, height=843),
        action=PostbackAction(label=MENU_C, display_text=MENU_C, data=MENU_C)),
        RichMenuArea(bounds=RichMenuBounds(x=0, y=844, width=833, height=843),
        action=PostbackAction(label=MENU_D, display_text=MENU_D, data=MENU_D)),
        RichMenuArea(bounds=RichMenuBounds(x=834, y=844, width=833, height=843),
        action=PostbackAction(label=MENU_E, display_text=MENU_E, data=MENU_E)),
        RichMenuArea(bounds=RichMenuBounds(x=1666, y=844, width=833, height=843),
        action=PostbackAction(label=MENU_F, display_text=MENU_F, data=MENU_F)),
        ]
)
rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
#print(rich_menu_id)

#リッチメニューの画像をアップロードする
with open('./rich_menu_image.png', 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)

#リッチメニューの画像をDLする
content = line_bot_api.get_rich_menu_image(rich_menu_id)
with open('./Download.png', 'wb') as fd:
    for chunk in content.iter_content():
        fd.write(chunk)

#リッチメニューの配列を取得する
rich_menu_list = line_bot_api.get_rich_menu_list()
#print(rich_menu_list)

#デフォルトのリッチメニューを設定する
#https://intellectual-curiosity.tokyo/2019/08/31/python%E3%81%A7curl%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89%E3%81%A8%E5%90%8C%E7%AD%89%E3%81%AE%E5%87%A6%E7%90%86%E3%82%92%E5%AE%9F%E8%A1%8C%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95/

url = 'https://api.line.me/v2/bot/user/all/richmenu/' + rich_menu_id
headers = {
    'Authorization': 'Bearer {'+line_token.TOKEN+'}',
}

response = requests.post(url, headers=headers)
