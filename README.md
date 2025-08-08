# Currency Converter — API Bug vs Fix

## 📌 Challenge Statement
This project addresses a common **"Base Currency Assumption"** bug in currency converters.

**Reference Source:** [ExchangeRate API – Pair Conversion Requests](https://www.exchangerate-api.com/docs/pair-conversion-requests)

**Problem:**  
Many implementations assume that the API's **base currency** is the same as the user-selected "From" currency.  
APIs return rates relative to a fixed base (e.g., USD or EUR). If `fromCurrency ≠ baseCurrency`, directly multiplying:
```js
converted = amount * rates[to];
