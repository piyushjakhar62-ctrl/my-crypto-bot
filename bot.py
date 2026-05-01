import ccxt.async_support as ccxt
import asyncio
import urllib.parse
import aiohttp
import time

# --- सेटिंग्स ---
TOKEN = "8621795447:AAFwfiwvrMM3cUFCGoEMgGWGZflbifS141s"
CHAT_ID = "8722887885"

async def send_telegram_msg(text):
    try:
        msg = urllib.parse.quote(text)
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=15) as response:
                status = response.status
                if status == 200:
                    return True
                else:
                    print(f"!!! Telegram Error: Status {status}")
                    return False
    except Exception as e:
        print(f"!!! Network Error: {e}")
        return False

async def check_coin(symbol, bn, wz, investment, fee_percent):
    try:
        ticker_bn, ticker_wz = await asyncio.gather(
            bn.fetch_ticker(symbol),
            wz.fetch_ticker(symbol)
        )
        b_p = ticker_bn['last']
        w_p = ticker_wz['last']
        gap = ((w_p - b_p) / b_p) * 100
        net_profit = (investment * (gap/100)) - (investment * fee_percent)

        # टेस्टिंग के लिए: अगर प्रॉफिट ₹0.10 से ऊपर है तो मैसेज भेजें
        if net_profit >= 0.10: 
            alert = f"DEBUG ALERT: {symbol} | Profit: {net_profit:.2f}"
            await send_telegram_msg(alert)
            return f"Found: {symbol}(INR {net_profit:.2f})"
        return None
    except:
        return None

async def main():
    print("--- SCANNER STARTING: PIYUSH PRO ---")
    
    # चेक करने के लिए पहला मैसेज
    print("Sending test message to Telegram...")
    success = await send_telegram_msg("🚀 Piyush Bhai, Bot is starting NOW!")
    if success:
        print("Test Message Sent Successfully!")
    else:
        print("FAILED to send message. Please check your Internet/Token.")

    bn = ccxt.binance()
    wz = ccxt.wazirx()
    
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'DOGE/USDT', 'XRP/USDT', 'LTC/USDT', 'MATIC/USDT', 'TRX/USDT']
    investment = 1000
    fee_percent = 0.003

    try:
        while True:
            start_time = time.time()
            tasks = [check_coin(s, bn, wz, investment, fee_percent) for s in symbols]
            results = await asyncio.gather(*tasks)
            
            # जो कॉइन्स चेक हुए उनकी लिस्ट दिखाएगा
            found = [r for r in results if r is not None]
            print(f"Done in {time.time() - start_time:.2f}s | Opportunities: {len(found)}")
            
            # थोड़ा रुकिए ताकि सिस्टम को सांस लेने का मौका मिले
            await asyncio.sleep(5) 
    finally:
        await bn.close()
        await wz.close()

if __name__ == "__main__":
    asyncio.run(main())