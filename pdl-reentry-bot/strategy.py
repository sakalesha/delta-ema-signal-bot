import pandas as pd
import config

class Strategy:
    def __init__(self):
        self.pdh = None
        self.pdl = None
        self.last_day_ts = None

    def update_levels(self, daily_candles):
        """
        Updates PDH and PDL based on the last closed daily candle.
        Assumes daily_candles is sorted by time.
        """
        if daily_candles.empty:
            return

        # Get the last COMPLETED daily candle.
        # If the last row is today (still open), we need the one before it.
        # Usually APIs return the current open candle as the last one.
        # We'll check timestamps to be sure, but taking the second to last is safest if "latest" is current day.
        
        # Validating based on typical API behavior:
        # -1 is typically the current incomplete candle (if fetching up to 'now')
        # -2 is yesterday (completed)
        
        if len(daily_candles) < 2:
            return

        prev_day = daily_candles.iloc[-2]
        
        # Only update if we haven't processed this day yet or levels are unset
        if self.last_day_ts != prev_day["time"]:
            self.pdh = prev_day["high"]
            self.pdl = prev_day["low"]
            self.last_day_ts = prev_day["time"]
            print(f"[Strategy] Updated Levels | PDH: {self.pdh}, PDL: {self.pdl} (Date: {prev_day['time'].date()})")

    def check_signal(self, candles_15m):
        """
        Checks for Buy/Sell signals based on 15m candles and PDH/PDL.
        """
        if self.pdh is None or self.pdl is None:
            return None, "Levels not set"

        if len(candles_15m) < 3:
            return None, "Not enough data"

        # Candles:
        # -1: Current (Open/Incomplete) - Ignore for signal confirmation usually, or use if "Re-entry Close" implies waiting for close. The strategy says "Candle closes...", so we must look at COMPLETED candles.
        # -2: Last Completed Candle (Result Candle?)
        # -3: Previous Completed Candle (Trap Candle?)
        
        # We iterate backwards looking for the pattern in recent history?
        # Or just check if the *just closed* candle completed the pattern.
        
        # Let's focus on the last completed candle (-2) completing the setup.
        
        c_last = candles_15m.iloc[-2] # The candle that just closed
        c_prev = candles_15m.iloc[-3] # The candle before that
        
        # We also might need to look slightly further back for the Trap candle if it wasn't immediately previous.
        # Strategy: "A subsequent candle (same day) Closes back..."
        # This implies the Trap could have happened a few candles ago.
        
        # Simplification for automation:
        # Monitor for ANY close below PDL (Trap). Set a flag "Potential Buy Trap Active".
        # If "Active", check for Re-entry.
        # OR
        # Scan last N candles for the pattern sequence.
        
        # Let's scan the last 5 candles to see if any valid trap + re-entry sequence completed *just now* (at c_last).
        
        signal = None
        reason = ""

        # --- BUY LOGIC (Seller Trap) ---
        # 1. Trap: Candle Closed < PDL
        # 2. Re-entry: 
        #    A: Close > PDL
        #    B: Sweep (Low < PDL), Rejection (Close > PDL), Next Green
        
        # Check condition 2 exists at c_last
        
        # 2A Check: c_last closed > PDL
        cond_2a_buy = c_last["close"] > self.pdl
        
        if cond_2a_buy:
             # Look for Condition 1 (Trap) in recent candles BEFORE c_last
             # Iterate back from c_prev
             for i in range(3, 8): # Check last few candles
                 if i > len(candles_15m): break
                 c_historical = candles_15m.iloc[-i]
                 
                 # Condition 1: Close < PDL
                 if c_historical["close"] < self.pdl:
                     # Valid Trap found!
                     # Verify it wasn't invalidated in between? (Strategy doesn't specify, but implies immediate re-entry is better)
                     # For now, if we found a trap and now we re-entered, it's a valid 2A signal.
                     return "BUY", f"Trap at {c_historical['time'].strftime('%H:%M')} (Close < PDL), Re-entry at {c_last['time'].strftime('%H:%M')} (Close > PDL)"

        # 2B Check: Rejection + Confirmation
        # Setup: c_prev swept PDL but closed > PDL. c_last is GREEN.
        
        # c_prev stats
        c_prev_sweep = c_prev["low"] < self.pdl
        c_prev_rejection = c_prev["close"] > self.pdl
        
        # c_last stats
        c_last_green = c_last["close"] > c_last["open"]
        
        if c_prev_sweep and c_prev_rejection and c_last_green:
            # This is setup 2B.
            # Does it require a PRIORT "Close < PDL" (Condition 1)?
            # Strategy says:
            # "Condition 1 (Mandatory - Liquidity Grab): Any candle closes BELOW PDL ... 
            # Condition 2 (Any one must occur)... 2B: Same candle low < PDL, Close > PDL, Next Green"
            
            # 2B description seems to merge the sweep and rejection into one candle. 
            # But Condition 1 says "Close BELOW PDL" is MANDATORY.
            # If 2B happens (Sweep + Close > PDL), then the candle did NOT close below PDL.
            # CONTRADICTION in text:
            # "Condition 1 (MANDATORY...): Any candle closes BELOW PDL... Meaning... Trap is created. 
            #  Condition 2... 2A... 2B... Same candle low < PDL, Close > PDL" -> If Close > PDL, it didn't Close Below PDL.
            
            # Interpretation:
            # Scenario A (Classic): Candle X closes < PDL (Trap). Candle Y closes > PDL.
            # Scenario B (Advanced): Candle X wicks < PDL but closes > PDL (Sweep/Hammer). Candle Y is Green. 
            #   In Scenario B, the "Condition 1 (Close < PDL)" technically didn't happen, but "Liquidity Grab" (Low < PDL) happened.
            #   The text "Condition 1 (MANDATORY... Any candle closes BELOW PDL)" might be one distinct setup type, 
            #   OR the user copy-pasted slightly conflicting rules.
            #   Re-reading 2B description: "This condition captures fast traps without waiting for multiple candles."
            #   This implies 2B stands ALONE as a valid entry mechanism where you don't wait for a close below.
            #   The "Liquidity Grab" is the VICIOUS WICK.
            
            # I will implement 2B as a standalone valid path: Sweep (Low < PDL), Close > PDL, Next Green.
            
            return "BUY", f"2B Setup: Sweep at {c_prev['time'].strftime('%H:%M')}, Confirmed Green at {c_last['time'].strftime('%H:%M')}"

        # --- SELL LOGIC (Buyer Trap) ---
        # 1. Trap: Candle Closed > PDH
        # 2. Re-entry: Cast Back Below PDH (2A) OR Sweep/Rejection (2B)
        
        # 2A Check: c_last closed < PDH
        if c_last["close"] < self.pdh:
             # Check for recent Close > PDH
             for i in range(3, 8):
                 if i > len(candles_15m): break
                 c_historical = candles_15m.iloc[-i]
                 if c_historical["close"] > self.pdh:
                     return "SELL", f"Trap at {c_historical['time'].strftime('%H:%M')} (Close > PDH), Re-entry at {c_last['time'].strftime('%H:%M')} (Close < PDH)"

        # 2B Check: Sweep PDH (High > PDH), Close < PDH, Next Red
        c_prev_sweep_sell = c_prev["high"] > self.pdh
        c_prev_reject_sell = c_prev["close"] < self.pdh
        c_last_red = c_last["close"] < c_last["open"]
        
        if c_prev_sweep_sell and c_prev_reject_sell and c_last_red:
            return "SELL", f"2B Setup: Sweep at {c_prev['time'].strftime('%H:%M')}, Confirmed Red at {c_last['time'].strftime('%H:%M')}"

        return None, "No Signal"

    def get_context(self):
        return f"PDH: {self.pdh}, PDL: {self.pdl}"
