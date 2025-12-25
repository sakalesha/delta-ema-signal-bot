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
        # 2. Previous Low Swept (User definition: Previous candle low is swept)
        # recent_lows[-1] is the low of the candle immediately before C1
        prev_candle_low = recent_lows[-1] if recent_lows else float('inf')
        
        # Check if C1 Low broke the Previous Candle Low
        if c1["low"] < prev_candle_low:
             # 3. Strong Rejection Wick (Lower wick should be significant)
             c1_range = c1["high"] - c1["low"]
             c1_lower_wick = min(c1["open"], c1["close"]) - c1["low"]
             
             if c1_range > 0 and (c1_lower_wick / c1_range) >= 0.3:
                 # 4. EMA Acceptance (C2 closes above EMA C2)
                 if c2["close"] > ema_c2:
                     # 5. Strong Body Close (>= 30% of C2 body above EMA 5)
                     body_above = c2["close"] - max(c2["open"], ema_c2)
                     if body_above / body_c2 >= 0.30:
                         return "BUY"

    # --- SELL SETUP ---
    # 1. Price Above EMA 5 (C1 closes above EMA C1)
    if c1["close"] > ema_c1:
        # 2. Previous High Swept (User definition: Previous candle high is swept)
        # recent_highs[-1] is the high of the candle immediately before C1
        prev_candle_high = recent_highs[-1] if recent_highs else float('-inf')
        
        if c1["high"] > prev_candle_high:
            # 3. Strong Rejection Wick (Upper wick should be significant)
            c1_range = c1["high"] - c1["low"]
            c1_upper_wick = c1["high"] - max(c1["open"], c1["close"])
            
            if c1_range > 0 and (c1_upper_wick / c1_range) >= 0.3:
                # 4. EMA Acceptance (C2 closes below EMA C2)
                if c2["close"] < ema_c2:
                    # 5. Strong Body Close (>= 30% of C2 body below EMA 5)
                    body_below = min(c2["open"], ema_c2) - c2["close"]
                    if body_below / body_c2 >= 0.30:
                        return "SELL"

    return None

def check_ema_crossover(c1, c2, ema_c1, ema_c2):
    """
    Checks for Price crossing EMA 5 (Setup Condition 1).
    
    Args:
        c1: Previous candle
        c2: Current confirmed candle
        ema_c1: EMA at C1
        ema_c2: EMA at C2
    
    Returns:
        "BULLISH_CROSS" (Price Goes Above EMA)
        "BEARISH_CROSS" (Price Goes Below EMA)
        None
    """
    # Price Goes Below EMA 5 (Bearish Pressure / Early Buyer Trap)
    # C1 Close > EMA (or Open > EMA) -> C2 Close < EMA
    # We check if C2 closed below EMA while C1 was above (or just cross logic)
    if c1["close"] >= ema_c1 and c2["close"] < ema_c2:
        return "BEARISH_CROSS"
    
    # Price Goes Above EMA 5 (Bullish Pressure / Early Seller Trap)
    if c1["close"] <= ema_c1 and c2["close"] > ema_c2:
        return "BULLISH_CROSS"
        
    return None
