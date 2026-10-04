# Python Trading and Analysis Tools

This repository contains Python scripts for trading analysis and automation across multiple markets including PSX, QSE, and Crypto, along with MT5 trading connections and email/Telegram notification capabilities.

## Setup

### Configuration

This project requires credentials for email, Telegram, and MT5 trading platforms. Follow these steps to set up your configuration:

1. **Copy the example configuration file:**
   ```bash
   cp config.example.ini config.ini
   ```

2. **Edit `config.ini` and fill in your actual credentials:**
   - **Email credentials**: Gmail username and [app password](https://support.google.com/accounts/answer/185833)
   - **Telegram credentials**: Bot token and chat ID from [@BotFather](https://t.me/botfather)
   - **MT5 credentials**: Your MetaTrader 5 login, password, server, and installation path

3. **Keep your credentials secure:**
   - Never commit `config.ini` to version control (it's already in `.gitignore`)
   - Only commit changes to `config.example.ini` (with placeholder values)

### Configuration File Structure

The `config.ini` file should contain the following sections:

```ini
[email]
username=your_email@gmail.com
password=your_gmail_app_password

[telegram]
bot_token=your_telegram_bot_token
chat_id=your_telegram_chat_id

[mt5]
login=your_mt5_account_number
password=your_mt5_password
server=your_mt5_server_name
path=C:\Program Files\MetaTrader 5\terminal64.exe
```

## Features

- **Market Analysis**: Scripts for analyzing PSX (Pakistan Stock Exchange), QSE (Qatar Stock Exchange), and cryptocurrency markets
- **MT5 Integration**: Complete suite of MetaTrader 5 connection and trading functions
- **Notifications**: Email and Telegram notifications for trading signals and analysis
- **Technical Analysis**: RSI, moving averages, and other technical indicators
- **Automated Trading**: Signal generation and trade execution capabilities

## Security Notes

⚠️ **Important**: This repository does NOT store credentials in code or version control. All sensitive information must be stored in your local `config.ini` file which is excluded from git tracking.

If you accidentally commit credentials, immediately:
1. Revoke/rotate all exposed credentials
2. Contact your service providers (Gmail, Telegram, MT5 broker)
3. Update your local `config.ini` with new credentials

## Contributing

When contributing to this project:
- Never commit actual credentials
- Update `config.example.ini` if adding new configuration options
- Ensure all new scripts read credentials from `config.ini` using `configparser`
