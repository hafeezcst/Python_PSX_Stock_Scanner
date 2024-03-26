
import requests

def send_telegram_message( message):
    bot_token = '7041750811:AAFrXrmMKq3UAOtuU3xF6EX9T1U8KWsz7F8'
    chat_id = '-4159614564'  # Can be numeric ID or username for a user or a group
    send_url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}'
    response = requests.get(send_url)
    return response.json()


