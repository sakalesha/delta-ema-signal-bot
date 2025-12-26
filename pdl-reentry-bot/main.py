import time
import pandas as pd
from datetime import datetime
import config
import delta_wrapper
from strategy import Strategy
import notifier
import signal
import sys

# Global State
running = True
strategy = Strategy()
last_processed_time = None

def signal_handler(sig, frame):
    global running
    print("\nShutting down bot...")
    running = False

def run_bot():
    global last_processed_time
    print(f"[{datetime.now()}] PDL/PDH Re-entry Bot Started for {config.SYMBOL}")
    notifier.send_alert(f"🚀 PDL/PDH Bot Started on {config.SYMBOL}")

    while running:
        try:
            # 1. Update Daily Levels (PDH/PDL)
            # Fetch daily candles
            daily_candles = delta_wrapper.fetch_candles(config.SYMBOL, config.TIMEFRAME_1D, limit=5)
            if not daily_candles.empty:
                strategy.update_levels(daily_candles)
            else:
                print("Warning: Could not fetch daily candles.")

            # 2. Check 15m Signals
            # Fetch 15m candles
            candles_15m = delta_wrapper.fetch_candles(config.SYMBOL, config.TIMEFRAME_15M, limit=20)
            
            if not candles_15m.empty:
                # Get the last COMPLETED candle time (2nd to last in list usually)
                last_completed_candle = candles_15m.iloc[-2]
                last_completed_time = last_completed_candle["time"]

                # Only run logic if we have a NEW closed candle
                if last_processed_time != last_completed_time:
                    
                    sig_type, reason = strategy.check_signal(candles_15m)
                    
                    print(f"[{last_completed_time}] Context: {strategy.get_context()} | Result: {sig_type} ({reason})")
                    
                    if sig_type:
                        # Construct Alert Message
                        msg = (
                            f"🚨 **{sig_type} SIGNAL** 🚨\n"
                            f"Symbol: {config.SYMBOL}\n"
                            f"Time: {last_completed_time}\n"
                            f"Reason: {reason}\n"
                            f"Levels: PDH={strategy.pdh}, PDL={strategy.pdl}\n"
                        )
                        print(">>> SENDING ALERT <<<")
                        notifier.send_alert(msg)
                    
                    last_processed_time = last_completed_time
                else:
                    # Just heartbeat or wait
                    pass
            else:
                print("Warning: Could not fetch 15m candles.")

        except Exception as e:
            print(f"Error in main loop: {e}")
            notifier.send_alert(f"⚠️ Bot Error: {e}")

        # Sleep to avoid spamming API
        # We need to run every few seconds to catch the candle close, but for 15m candles, 
        # checking every 30-60s is usually fine.
        time.sleep(60)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    run_bot()
