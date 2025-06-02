import json
from collections import defaultdict
from datetime import datetime, timedelta

# Load JSON transactions
with open('transactions.json', 'r', encoding='utf-8') as f:
    transactions = json.load(f)

# Data holders
total_amount = 0
customer_totals = defaultdict(float)
daily_totals = defaultdict(lambda: defaultdict(float))
tx_by_customer = defaultdict(list)
suspicious = {
    "large_amount": [],
    "high_freq": [],
    "rapid_location": [],
    "daily_limit": []
}

# Preprocess
for tx in transactions:
    name = tx['customer_name']
    amount = tx['amount']
    location = tx['location']
    timestamp = datetime.fromisoformat(tx['timestamp'].replace("Z", "+00:00"))

    total_amount += amount
    customer_totals[name] += amount
    daily_key = timestamp.date()
    daily_totals[name][daily_key] += amount
    tx_by_customer[name].append((timestamp, location, amount))

    if amount > 50000:
        suspicious["large_amount"].append(tx)

# Check advanced patterns
for name, txs in tx_by_customer.items():
    txs.sort()  # by time
    for i in range(len(txs)):
        t1, loc1, _ = txs[i]
        window_count = 1
        for j in range(i + 1, len(txs)):
            t2, loc2, _ = txs[j]
            if t2 - t1 <= timedelta(hours=1):
                window_count += 1
                # Rule 1: High frequency
                if window_count > 3:
                    suspicious["high_freq"].append({"customer": name, "start": t1.isoformat(), "count": window_count})
                    break
            else:
                break

        # Rule 2: Rapid location switch
        if i + 1 < len(txs):
            t_next, loc_next, _ = txs[i + 1]
            if loc1 != loc_next and (t_next - t1).total_seconds() < 3600:
                suspicious["rapid_location"].append({
                    "customer": name,
                    "from": loc1,
                    "to": loc_next,
                    "time_diff": str(t_next - t1)
                })

# Rule 3: Daily limits
for name, days in daily_totals.items():
    for day, amount in days.items():
        if amount > 100000:
            suspicious["daily_limit"].append({
                "customer": name,
                "date": str(day),
                "total": amount
            })

# ----------- Results ----------- #

print("📊 Transaction Summary")
print(f"Total transactions: {len(transactions)}")
print(f"Total amount: {total_amount:,.2f} SAR")

print("\n💼 Amount by Customer:")
for name, amt in customer_totals.items():
    print(f"  {name}: {amt:,.2f} SAR")

# Show all suspicious
print("\n🚨 Suspicious Transactions")

print("\n  🔴 Large Single Transactions (> 50,000 SAR):")
for tx in suspicious["large_amount"]:
    print(f"    {tx['customer_name']} - {tx['amount']} SAR in {tx['location']} at {tx['timestamp']}")

print("\n  🔴 High Frequency Transactions (> 3/hr):")
for tx in suspicious["high_freq"]:
    print(f"    {tx['customer']} made {tx['count']} transactions starting at {tx['start']}")

print("\n  🔴 Rapid Location Switch:")
for tx in suspicious["rapid_location"]:
    print(f"    {tx['customer']} moved from {tx['from']} to {tx['to']} in {tx['time_diff']}")

print("\n  🔴 Daily Total > 100,000 SAR:")
for tx in suspicious["daily_limit"]:
    print(f"    {tx['customer']} sent {tx['total']:,.2f} SAR on {tx['date']}")
