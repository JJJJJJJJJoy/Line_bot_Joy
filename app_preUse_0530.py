import os
import json
import numpy as np
import requests

# from PIL import Image, ImageOps
from flask import Flask, request, abort
import subprocess
import shutil



from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, URITemplateAction, CarouselTemplate, CarouselColumn, URIAction, FlexSendMessage, CameraAction, CameraRollAction, QuickReply,
    QuickReplyButton, PostbackAction)
from linebot.exceptions import LineBotApiError


#我把資料都寫在env.json裡 記得進去裡面修改成自己要套用的Linebot API
with open('env.json') as f:
    env = json.load(f)
    
line_bot_api = LineBotApi(env['YOUR_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(env['YOUR_CHANNEL_SECRET'])



app = Flask(__name__)

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
    except Exception as e:
        print("Error occurred while handling webhook: ", e)
        abort(500)

    return 'OK'


#根據訊息內容  做處理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    if event.message.text == '關於我':
        with open('about_me.json',encoding='utf-8') as d:       ### about_me.json ####
            test = json.load(d)
        line_bot_api.reply_message(
        event.reply_token,FlexSendMessage('關於我',test)
        )


    elif event.message.text == '專案作品':
        with open('project.json',encoding='utf-8') as d:       ### project.json ####
            test = json.load(d)
        line_bot_api.reply_message(
        event.reply_token,FlexSendMessage('專案作品',test)
        )


    elif event.message.text == '聯絡資訊':
        with open('connect.json',encoding='utf-8') as d:       ### connect.json ####
            test = json.load(d)
        line_bot_api.reply_message(
        event.reply_token,FlexSendMessage('聯絡資訊',test)
        )




if __name__ == "__main__":
    app.run()
