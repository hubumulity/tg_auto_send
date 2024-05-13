# 卷毛鼠签到脚本
from telegram.client import Telegram
import os, time

an=[1] #账号数量
# 如有两个账号，则an=[1，2]，以此类推，并在下方填入多账号信息
for accn in an:
    if accn == 1: # 第一个账号
        tg_args = {
            'api_id': '', # 填入 api id
            'api_hash': '', # 填入 api hash
            'phone': '', # Telegram账号
            'database_encryption_key': '',
            'files_directory': f"{os.getcwd()}/sessions", # 修改储存session文件位置，防止重启后session失效
            'library_path': '/root/emby-server-checkin/libtdjson_amd64.so' # tdlib 的绝对路径
        }

        tg = Telegram(**tg_args)

    # #多账号支持
    # if accn == 2:
    #     tg_args = {
    #         'api_id': f"{os.getenv('api_id')}", # 填入 api id
    #         'api_hash': f"{os.getenv('api_hash')}", # 填入 api hash
    #         'phone': f"{os.getenv('phone')}", # Telegram账号
    #         'database_encryption_key': 'passw0rd!',
    #         'files_directory': f"{os.getcwd()}/sessions", # 修改储存session文件位置，防止重启后session失效
    #         'library_path': f"{os.getcwd()}/libtdjson.so" # tdlib 的绝对路径
    #     }
    #     if proxy_server and proxy_port:
    #         tg_args['proxy_server'] = proxy_server
    #         tg_args['proxy_port'] = proxy_port
    #         tg_args['proxy_type'] = proxy_type

    #     tg = Telegram(**tg_args)

    tg.login()
    # chat id
    # 厂妹 1429576125
    # 卷毛鼠活动机器人 1723810586

    answers = []
    message = {}
    sending = False
    num = 1
    now = int(time.time())

    def send_checkin():
        global sending
        if (sending):
            return
        sending = True
        result=tg.send_message(
            chat_id=6245046199,
            text="太平管理", # 发送签到指令
        )
        result.wait()
        sending = False

    def send_verification_code(update):
        global text
        global answers
        global message
        global num
        # 所有的新消息都会被监听，增加判断只监听自己感兴趣的
        if 6245046199 == update['message']['chat_id']:
            # print(update)
            message = update['message']
            print(message)
            # 获取收到的消息文本
            date = message['date']
            # 如果消息文本不是"太平管理"，则删除该消息
            if now > date:
               return
            # message = update['message']['content']
            # print('content', message['content'])
            if (message['sender_id']['user_id'] == 6245046199):
                time.sleep(1)
                text = {
                 1: '1',
                 2: '3',
                 3: '2',
                 4: '6'
                }.get(num, '')
                result=tg.send_message(
                    chat_id=6245046199,
                    text=text, # 发送指令
                )
                result.wait()
                num += 1
            else:
               print(1)

    tg.add_update_handler('updateNewMessage', send_verification_code)

    result = tg.get_chats()
    result.wait()
    send_checkin()

    time.sleep(30) # 等待120秒签到完毕后退出程序
    tg.stop()