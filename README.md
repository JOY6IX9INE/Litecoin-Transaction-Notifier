
# Litecoin Transaction Notifier

This Python script monitors a specified Litecoin (LTC) address for new transactions and sends a notification to a Discord webhook when a transaction is detected. The script supports the use of a proxy for network requests.

## Features

- Fetches the current Litecoin price in USD.
- Monitors a Litecoin address for new transactions.
- Sends a notification to a specified Discord webhook with details about the transaction.
- Supports optional proxy settings for network requests.

## Requirements

- Python 3.x
- `requests` library

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/JOY6IX9INE/ltc_notify.git
    cd ltc_notify
    ```

2. Install the required Python libraries:
    ```sh
    pip install requests
    ```

## Usage

1. Update the `webhook_url` and `ltc_address` variables in the script with your Discord webhook URL and Litecoin address, respectively.

2. (Optional) If you want to use a proxy, set the `proxy_url` variable. If not, leave it blank or set it to `None`.

3. Run the script:
    ```sh
    python ltc_notify.py
    ```

## Configuration

- **webhook_url**: The URL of your Discord webhook where notifications will be sent.
- **ltc_address**: The Litecoin address to be monitored for new transactions.
- **proxy_url** [ Optional ] : The proxy URL for network requests. Leave it blank or set it to `None` if not using a proxy.

## Example

Here's an example of how to set up the script:

```python
if __name__ == '__main__':
    webhook_url = 'https://discord.com/api/webhooks/xxxxxx/xxxx'
    ltc_address = 'LP1m3ZMadZETjn6ukyXgPRBQoVqqNYQnX4'
    # Add Proxy Else Leave Blank Or Set None
    proxy_url = ""
    
    notifier = ltc_notify(webhook_url, ltc_address, proxy_url)
    notifier.fetch_ltc_price()
    notifier.monitor_transactions()
```


# Disclaimer
This tool is created for educational purposes and ethical use only. Any misuse of this tool for malicious purposes is not condoned. The developers of this tool are not responsible for any illegal or unethical activities carried out using this tool.

[![Star History Chart](https://api.star-history.com/svg?repos=JOY6IX9INE/Litecoin-Transaction-Notifier&type=Date)](https://star-history.t9t.io/#JOY6IX9INE/Litecoin-Transaction-Notifier&Date)
