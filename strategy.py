def check_liquidity_sweep_signal(c1, c2, ema_c1, ema_c2, recent_lows, recent_highs):
    """
    Checks for EMA 5 Liquidity Sweep Confirmation Strategy.

    Args:
        c1: Setup candle (Liquidity Sweep)
        c2: Confirmation candle (EMA Acceptance)
        ema_c1: EMA 5 value corresponding to C1
        ema_c2: EMA 5 value corresponding to C2
        recent_lows: List of lows of previous N candles (excluding C1, C2)
        recent_highs: List of highs of previous N candles (excluding C1, C2)

    Returns:
        "BUY", "SELL" or None
    """
    
    body_c2 = abs(c2["close"] - c2["open"])
    if body_c2 == 0:
        return None

    # --- BUY SETUP (Liquidity Sweep + EMA Confirmation) ---
    # ✅ Condition 1: Price Goes Below EMA 5 (Already happened for Setup to exist, verified by context or C1 nature)
    # Market shows short-term bearish pressure. Traps early buyers.
    if c1["close"] < ema_c1:
        # ✅ Condition 2: Previous Low is Swept
        # Price breaks previous swing low slightly. Purpose: Hit seller stop-losses.
        prev_candle_low = recent_lows[-1] if recent_lows else float('inf')
        
        if c1["low"] < prev_candle_low:
             # ✅ Condition 3: Strong Rejection Wick
             # Long lower wick. Shows sellers failed to continue. Indicates absorption.
             c1_range = c1["high"] - c1["low"]
             c1_lower_wick = min(c1["open"], c1["close"]) - c1["low"]
             
             if c1_range > 0 and (c1_lower_wick / c1_range) >= 0.3:
                 # ✅ Condition 4: EMA Acceptance with Strong Body Close
                 # Next candle closes above EMA 5. At least 30% of candle body above EMA.
                 if c2["close"] > ema_c2:
                     body_above = c2["close"] - max(c2["open"], ema_c2)
                     if body_above / body_c2 >= 0.30:
                         return "BUY"

    # --- SELL SETUP (Liquidity Sweep + EMA Confirmation) ---
    # ✅ Condition 1: Price Goes Above EMA 5
    # Market shows short-term bullish pressure. Traps early sellers.
    if c1["close"] > ema_c1:
        # ✅ Condition 2: Previous High is Swept
        # Price breaks previous swing high slightly. Purpose: Hit buyer stop-losses.
        prev_candle_high = recent_highs[-1] if recent_highs else float('-inf')
        
        if c1["high"] > prev_candle_high:
            # ✅ Condition 3: Strong Rejection Wick
            # Long upper wick. Buyers fail to continue. Indicates distribution.
            c1_range = c1["high"] - c1["low"]
            c1_upper_wick = c1["high"] - max(c1["open"], c1["close"])
            
            if c1_range > 0 and (c1_upper_wick / c1_range) >= 0.3:
                # ✅ Condition 4: EMA Acceptance with Strong Body Close
                # Next candle closes below EMA 5. At least 30% of candle body below EMA.
                if c2["close"] < ema_c2:
                    body_below = min(c2["open"], ema_c2) - c2["close"]
                    if body_below / body_c2 >= 0.30:
                        return "SELL"
    return None

def check_ema_detach(candle, ema_val):
    """
    Checks if the candle is completely detached from EMA 5 (No Touch).
    Triggers separate alerts as requested.
    
    Args:
        candle: The candle to check
        ema_val: EMA 5 value for this candle
    
    Returns:
        "BEARISH_DETACH" (High < EMA)
        "BULLISH_DETACH" (Low > EMA)
        None
    """
    # Price Below EMA 5 and NOT Toucing (High < EMA)
    if candle["high"] < ema_val:
        return "BEARISH_DETACH"
    
    # Price Above EMA 5 and NOT Touching (Low > EMA)
    if candle["low"] > ema_val:
        return "BULLISH_DETACH"
        
    return None
