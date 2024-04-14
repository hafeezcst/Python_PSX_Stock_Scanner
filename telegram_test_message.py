from telegram_message import send_telegram_message

message="test message"

try :
    send_telegram_message ( message )
    print ( "Telegram message sent successfully" )
except Exception as e :
    print ( "Error sending Telegram message:", e )