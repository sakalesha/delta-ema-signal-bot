# EMA 5 Liquidity Sweep Confirmation Strategy

**(Signal-Only | Crypto | Delta Exchange India)**

## 1. Strategy Name & Philosophy
**Strategy Name**: EMA 5 Liquidity Sweep Confirmation Strategy
**Core Idea**: "Pro entry ka secret yahin hai" - combines Liquidity grab (stop-loss hunt), EMA 5 mean re-acceptance, and Strong candle body confirmation. Based on Smart Money Concepts (SMC).

## 2. Market & Instrument
- **Market**: Cryptocurrency
- **Exchange**: Delta Exchange India
- **Instruments**: Perpetual Futures (BTCUSD, ETHUSD, etc.)
- **Execution**: Signal-only (Telegram alerts)
- **Style**: Intraday / Momentum Reversal after Sweep

## 3. Timeframe
- **Primary**: 15-minute
- **Advanced**: 5-minute (experienced traders only)

## 4. Indicators Used
- **Exponential Moving Average (EMA)**
    - Period: 5
    - Source: Close
    - Role: Dynamic equilibrium & Confirmation

## 5. Key Concepts
### 5.1 Liquidity Sweep (Stop-loss Hunt)
- Price slightly breaks a previous high or low.
- Triggers stop-losses of retail traders.
- Immediately shows rejection via wick.
- **Rule**: If sweep does not happen → NO TRADE.

### 5.2 Candle Definitions
- **C1**: Liquidity Sweep Candle
- **C2**: Confirmation Candle (EMA acceptance)
- Signals checked after C2 closes.

## 6. BUY SETUP (Long)
**Conditions:**
1.  **Price Below EMA 5**: Market shows short-term bearish pressure.
2.  **Previous Low Swept**: Price breaks previous swing low slightly (Condition: C1 Low < Previous Swing Low).
3.  **Strong Rejection Wick**: Long lower wick on C1.
4.  **EMA Acceptance**: C2 closes above EMA 5.
5.  **Strong Body Close**: ≥ 30% of C2 body is above EMA 5.

## 7. SELL SETUP (Short)
**Conditions:**
1.  **Price Above EMA 5**: Market shows short-term bullish pressure.
2.  **Previous High Swept**: Price breaks previous swing high slightly (Condition: C1 High > Previous Swing High).
3.  **Strong Rejection Wick**: Long upper wick on C1.
4.  **EMA Acceptance**: C2 closes below EMA 5.
5.  **Strong Body Close**: ≥ 30% of C2 body is below EMA 5.

## 8. Trade Avoidance Rule
**IF NO LIQUIDITY SWEEP → NO TRADE**

## 9. Risk Management
- **Stop Loss**: Low of sweep candle (BUY) / High of sweep candle (SELL)
- **Target**: Minimum 1:1, Ideal 1:2
