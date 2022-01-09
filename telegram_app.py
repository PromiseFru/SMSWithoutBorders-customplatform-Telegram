#!/usr/bin/env python3

from telegram.client import Telegram, AuthorizationState
import configparser

class TelegramApp:
    def __init__(self, phone):
        self.phone = phone
        configs = configparser.ConfigParser()
        configs.read('configs.conf')

        api_id = int(configs['DEV']['API_ID'])
        api_hash = configs['DEV']['API_HASH']
        database_encryption_key = configs['DEV']['ENCRYPTION_KEY']

        self.tg = Telegram(
            api_id = api_id,  
            api_hash = api_hash,
            phone = phone,
            database_encryption_key='changeme1234')

        self.login_state=None
        self.tg.add_message_handler(self.new_message_handler)


    def wait_login(self,code=None,password=None,blocking=False):
        if not self.login_state:
            self.login_state = self.tg.login(blocking=blocking)

        if code:
            print('* Using code for login')
            if self.login_state == AuthorizationState.WAIT_CODE:
                self.tg.send_code(code)
                login_state = self.tg.login(blocking=blocking)

        elif password:
            print('* Using code for login')
            if self.login_state == AuthorizationState.WAIT_PASSWORD:
                self.tg.send_password(password)
                login_state = self.tg.login(blocking=blocking)

        print('* Logged in')

    def login(self,blocking=False):
        self.login_state = self.tg.login(blocking=blocking)
        if self.login_state == AuthorizationState.READY:
            return 'ready'
        if self.login_state == AuthorizationState.WAIT_PASSWORD:
            return 'waiting password'
        if self.login_state == AuthorizationState.WAIT_CODE:
            return 'waiting code'

    def idle(self):
        self.tg.idle()

    def new_message_handler(self, update):
        print('+ New message')
        message_content = update['message']['content'].get('text', {})
        message_text = message_content.get('text', '').lower()

        if message_text == 'ping':
            chat_id = update['message']['chat_id']
            print(f'Pint has been received from {chat_id}')

            self.tg.send_message(
                    chat_id = chat_id,
                    text = 'pong')
