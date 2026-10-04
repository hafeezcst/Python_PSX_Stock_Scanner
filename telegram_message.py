
import requests
import configparser

def send_telegram_message( message):
    # Load Telegram credentials from config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    bot_token = config.get('telegram', 'bot_token')
    chat_id = config.get('telegram', 'chat_id')
    
    send_url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}'
    response = requests.get(send_url)
    return response.json()