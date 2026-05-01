import telebot
import ccxt
import time

# --- आपकी भरी हुई डिटेल्स ---
BINANCE_API = "aY6tvWpG08tHo3nT2C0LK65c9SuEuc0ZZIngKFztyP4u36lcbMuMmr8pTmRtXIt6"
BINANCE_SECRET = "xfRNDbN0LmwukA6NLMxrqENbQRJ9bk93wm7Y8yX5L7VIuf0tesn7KWNkNdtug5lk"

WAZIRX_API = "0FYVRs5SIxDXHpiJ2rIvO2DRFmmbRsTnDE70UcEcwcjuzkAq7hnZEBatK9lh073K"
WAZIRX_SECRET = "xATonbAaHdDw3AAIM07JCf7NNPnQlRLdAOWUAnzY"

TOKEN = "8621795447:AAFwfiwvrMM3cUCGoEMgGWGZflbifS141s" # फोटो से नया टोकन
MY_CHAT_ID = "8722887885" # आपकी फोटो से ID

bot = telebot.TeleBot(TOKEN)

# एक्सचेंज सेटअप
binance = ccxt.binance({'apiKey': BINANCE_API, 'secret': BINANCE_SECRET, 'enableRateLimit': True})
wazirx = ccxt.wazirx({'apiKey': WAZIRX_API, 'secret': WAZIRX_SECRET, 'enableRateLimit': True})

def piyush_scanner():
    # इन कॉइन्स पर नज़र रखेंगे
    coins = ['SOL/USDT', 'BTC/USDT', 'ETH/USDT', 'DOGE/USDT', 'XRP/USDT']
    
    for symbol in coins:
        try:
            # भाव मंगाना
            b_price = binance.fetch_ticker(symbol)['last']
            w_price = wazirx.fetch_ticker(symbol)['last']
            
            # मुनाफ़ा निकालना
            diff = w_price - b_price
            profit_pct = (diff / b_price) * 100
            
            # अगर मुनाफ़ा 0.5% से ज़्यादा है (फीस काटकर मुनाफ़े के लिए)
            if profit_pct > 0.5:
                msg = (f"🚀 **Piyush Bhai, Profit Opportunity!**\n\n"
                       f"Coin: {symbol}\n"
                       f"Binance Price: ${b_price}\n"
                       f"WazirX Price: ${w_price}\n"
                       f"Profit: {profit_pct:.2f}%")
                bot.send_message(MY_CHAT_ID, msg)
                print(f"Alert Sent for {symbol}")
                
        except Exception as e:
            print(f"Error checking {symbol}: {e}")

if __name__ == "__main__":
    bot.send_message(MY_CHAT_ID, "✅ पीयूष भाई, जासूस अब लाइव मार्केट स्कैन कर रहा है!")
    print("Scanner Started...")
    while True:
        piyush_scanner()
        time.sleep(30) # हर 30 सेकंड में बाज़ार चेक करेगा