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

    # --- BUY SETUP ---
    # 1. Price Below EMA 5 (C1 closes below EMA C1)
    if c1["close"] < ema_c1:
        # 2. Previous Low Swept (C1 Low < lowest of recent lows)
        prev_swing_low = min(recent_lows) if recent_lows else float('inf')
        
        if c1["low"] < prev_swing_low:
             # 3. Strong Rejection Wick (Lower wick should be significant)
             # Let's say lower wick is at least 30% of total range of C1
             c1_range = c1["high"] - c1["low"]
             c1_lower_wick = min(c1["open"], c1["close"]) - c1["low"]
             
             if c1_range > 0 and (c1_lower_wick / c1_range) >= 0.3:
                 # 4. EMA Acceptance (C2 closes above EMA C2)
                 if c2["close"] > ema_c2:
                     # 5. Strong Body Close (>= 30% of C2 body above EMA 5)
                     # Body Above = Close - Max(Open, EMA)
                     body_above = c2["close"] - max(c2["open"], ema_c2)
                     if body_above / body_c2 >= 0.30:
                         return "BUY"

    # --- SELL SETUP ---
    # 1. Price Above EMA 5 (C1 closes above EMA C1)
    if c1["close"] > ema_c1:
        # 2. Previous High Swept (C1 High > highest of recent highs)
        prev_swing_high = max(recent_highs) if recent_highs else float('-inf')
        
        if c1["high"] > prev_swing_high:
            # 3. Strong Rejection Wick (Upper wick should be significant)
            c1_range = c1["high"] - c1["low"]
            c1_upper_wick = c1["high"] - max(c1["open"], c1["close"])
            
            if c1_range > 0 and (c1_upper_wick / c1_range) >= 0.3:
                # 4. EMA Acceptance (C2 closes below EMA C2)
                if c2["close"] < ema_c2:
                    # 5. Strong Body Close (>= 30% of C2 body below EMA 5)
                    # Body Below = Min(Open, EMA) - Close
                    body_below = min(c2["open"], ema_c2) - c2["close"]
                    if body_below / body_c2 >= 0.30:
                        return "SELL"

    return None
