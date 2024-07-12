
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('jMZEyDqno2Ek+Jt9q9CZIoX1D+lVkldNhPQR8D7MMfUCpcLFofqQhsY+GhRnqNOtfL0VRnZz19yDD93Mf+S79Z+Xq/cloRumjnqFX4lLQSlpB0z6/705OsalAEFx2S+qLrKwWsTNCBa8WwntZ8hKoAdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('ab153ef10df31e3946777e579af78073')


# 監聽所有來自 /callback 的 Post Request
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
        abort(400)

    return 'OK'

# 訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if re.match('找文具', message):
        image_message = ImageSendMessage(original_content_url='https://drive.google.com/uc?export=view&id=1VB_dAXoUu918CpGhwAtPleHm7Kx8hHEH', preview_image_url='https://drive.google.com/uc?export=view&id=1VB_dAXoUu918CpGhwAtPleHm7Kx8hHEH')
        line_bot_api.reply_message(event.reply_token, image_message)
    elif re.match('送公文流程', message):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='送公文流程:\n    1.向職員確認還有沒有公文要送?\n    2.集中所有要送的公文\n    3.寫公文傳送紀錄單\n    4.送出公文'))

# 主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
