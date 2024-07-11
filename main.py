import requests
import time, datetime

class ltc_notify:
    def __init__(self, webhook_url, ltc_address, proxy_url=None):
        self.webhook_url = webhook_url
        self.ltc_address = ltc_address
        self.proxies = {
            "http": proxy_url,
            "https": proxy_url
        } if proxy_url else None
        self.ltc_price_usd = 0
        self.initial_tx_count = 0

    def fetch_ltc_price(self):
        try:
            response = requests.get('https://min-api.cryptocompare.com/data/price?fsym=LTC&tsyms=USD')
            response.raise_for_status()
            litecoin_price_usd = response.json().get('USD')
            self.ltc_price_usd = float(litecoin_price_usd)
        except requests.RequestException as error:
            print(f'[-] An Error Occured While Fetching Ltc Price : {error}')

    def send_notification(self, embed_data):
        try:
            payload = {
                'content': '',
                'embeds': [embed_data]
            }
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
        except requests.RequestException as error:
            print(f'[-] An Error Occured While Sending Notification : {error}')

    def monitor_transactions(self):
        endpoint = f'https://api.blockcypher.com/v1/ltc/main/addrs/{self.ltc_address}/full'

        try:
            response = requests.get(endpoint, proxies=self.proxies)
            response.raise_for_status()
            self.initial_tx_count = 2684 #response.json().get('n_tx')
            print(f'[+] Connected To Address : {self.ltc_address}')
            print(f'[+] Initial Transaction Count : {self.initial_tx_count}')
        except requests.RequestException as error:
            print(f'[-] An Error Occured : {error}')
            return

        while True:
            time.sleep(5)

            try:
                response = requests.get(endpoint, proxies=self.proxies)
                if response.status_code == 429:
                    print('[-] Rate Limit Exceeded, Retrying In 60 Seconds')
                    time.sleep(60)
                    continue

                current_tx_count = response.json().get('n_tx')
                if current_tx_count > self.initial_tx_count:
                    tx_data = response.json().get('txs')[0]
                    tx_hash = tx_data.get('hash')
                    outputs = tx_data.get('outputs')
                    ltc_amount = 0
                    usd_amount = 0

                    for output in outputs:
                        if output.get('addresses')[0] == self.ltc_address:
                            ltc_amount = output.get('value') / 100000000.0
                            usd_amount = ltc_amount * self.ltc_price_usd

                    usd_amount_str = f'${usd_amount:.2f}'
                    embed_data = {
                        'title': 'Litecoin Transaction Detected',
                        'thumbnail': {'url': 'https://cdn.discordapp.com/emojis/1119970943234744371.webp'},
                        'color': 8421504,
                        'description': f'**:moneybag: | Amount :** `{ltc_amount:.8f} LTC`\n**:money_with_wings: | Current Price :** `{usd_amount_str}`\n**:link: | Hash :** [{tx_hash}](https://blockchair.com/litecoin/transaction/{tx_hash})',
                        'footer': {
                            'text': 'https://github.com/JOY6IX9INE',
                            'icon_url': 'https://avatars.githubusercontent.com/u/95956256'
                        },
                        'timestamp': datetime.datetime.now(datetime.UTC).isoformat()
                    }

                    self.send_notification(embed_data)
                    self.initial_tx_count = current_tx_count

            except requests.RequestException as error:
                print(f'[-] An Error Occured : {error}')

if __name__ == '__main__':
    webhook_url = 'https://discord.com/api/webhooks/xxxxxx/xxxx'
    ltc_address = 'LP1m3ZMadZETjn6ukyXgPRBQoVqqNYQnX4'
    # Add Proxy Else Leave Blank Or Set None
    proxy_url = ""
    
    notifier = ltc_notify(webhook_url, ltc_address, proxy_url)
    notifier.fetch_ltc_price()
    notifier.monitor_transactions()
