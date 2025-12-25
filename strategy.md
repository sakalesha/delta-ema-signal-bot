# EMA 5 Rejection & Confirmation Strategy

## 1. Strategy Overview
The EMA 5 Rejection & Confirmation Strategy is a price-action–based momentum strategy designed to capture strong directional moves after price clearly rejects the 5-period Exponential Moving Average (EMA).

This strategy avoids:
- EMA hugging
- Sideways markets
- Weak candle closes

## 2. Market & Instrument
- **Market Type**: Cryptocurrency
- **Exchange**: Delta Exchange India
- **Instruments**: Perpetual Futures (e.g., BTCUSD, ETHUSD)
- **Timeframe**: 15-minute (Primary), 5-minute (Alternative)

## 3. Indicator Used
- **Exponential Moving Average (EMA)**
  - Period: 5
  - Source: Closing price

## 4. Candle Definitions
- **C1 (Setup Candle)**: Establishes rejection from EMA
- **C2 (Confirmation Candle)**: Confirms direction with strength

## 5. Entry Conditions (Core Logic)

### Rule 1: EMA Must NOT Be Touched (C1)
The setup candle (C1) must not touch EMA 5.
- EMA 5 should be completely outside the candle range.
- EMA 5 is neither between C1 high nor C1 low.

### Rule 2: Directional Confirmation (C2)
The immediate next candle (C2) must close on the opposite side of EMA 5 relative to C1.
- **Bullish Case**: C1 closes below EMA 5, C2 closes above EMA 5.
- **Bearish Case**: C1 closes above EMA 5, C2 closes below EMA 5.

### Rule 3: Minimum 30% Candle Body Strength (C2)
At least 30% of C2’s real body must be beyond EMA 5 in the signal direction.

## 6. Buy Signal Conditions
- C1 does not touch EMA 5
- C1 closes below EMA 5
- C2 closes above EMA 5
- ≥ 30% of C2 body is above EMA 5

## 7. Sell Signal Conditions
- C1 does not touch EMA 5
- C1 closes above EMA 5
- C2 closes below EMA 5
- ≥ 30% of C2 body is below EMA 5
