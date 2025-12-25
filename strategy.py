def check_ema5_signal(c1, c2, ema_c1, ema_c2):
    """
    Checks for EMA 5 Rejection & Confirmation Strategy.

    Args:
        c1: Setup candle (dict-like with open, high, low, close)
        c2: Confirmation candle (dict-like with open, high, low, close)
        ema_c1: EMA 5 value at C1
        ema_c2: EMA 5 value at C2

    Returns:
        "BUY", "SELL" or None
    """
    # Rule 1: C1 must NOT touch EMA (using EMA at C1)
    if c1["low"] <= ema_c1 <= c1["high"]:
        return None

    body = abs(c2["close"] - c2["open"])
    if body == 0:
        return None

    # BUY SIGNAL
    # C1 closed below EMA (at C1 time) and C2 closed above EMA (at C2 time)
    if c1["close"] < ema_c1 and c2["close"] > ema_c2:
        # Rule 3: 30% of C2 body above EMA
        # If open < EMA, body part is Close - EMA
        # If open > EMA, body part is Close - Open (full body)
        # using max(open, ema) handles both
        body_above = c2["close"] - max(c2["open"], ema_c2)
        if body_above / body >= 0.30:
            return "BUY"

    # SELL SIGNAL
    # C1 closed above EMA (at C1 time) and C2 closed below EMA (at C2 time)
    if c1["close"] > ema_c1 and c2["close"] < ema_c2:
        # Rule 3: 30% of C2 body below EMA
        # using min(open, ema) handles both
        body_below = min(c2["open"], ema_c2) - c2["close"]
        if body_below / body >= 0.30:
            return "SELL"

    return None
