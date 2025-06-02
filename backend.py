# backend.py
from flask import Flask, jsonify
import json
from collections import defaultdict
from datetime import datetime, timedelta

app = Flask(__name__)

def analyze_transactions():
    with open('transactions.json', 'r', encoding='utf-8') as f:
        transactions = json.load(f)

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

    for name, txs in tx_by_customer.items():
        txs.sort()
        for i in range(len(txs)):
            t1, loc1, _ = txs[i]
            window_count = 1
            for j in range(i + 1, len(txs)):
                t2, loc2, _ = txs[j]
                if t2 - t1 <= timedelta(hours=1):
                    window_count += 1
                    if window_count > 3:
                        suspicious["high_freq"].append({"customer": name, "start": t1.isoformat(), "count": window_count})
                        break
                else:
                    break

            if i + 1 < len(txs):
                t_next, loc_next, _ = txs[i + 1]
                if loc1 != loc_next and (t_next - t1).total_seconds() < 3600:
                    suspicious["rapid_location"].append({
                        "customer": name,
                        "from": loc1,
                        "to": loc_next,
                        "time_diff": str(t_next - t1)
                    })

    for name, days in daily_totals.items():
        for day, amount in days.items():
            if amount > 100000:
                suspicious["daily_limit"].append({
                    "customer": name,
                    "date": str(day),
                    "total": amount
                })

    summary = {
        "total_transactions": len(transactions),
        "total_amount": total_amount,
        "customer_totals": customer_totals,
        "suspicious": suspicious
    }

    # Convert defaultdicts to regular dicts for JSON serialization
    summary["customer_totals"] = dict(summary["customer_totals"])

    return summary

@app.route('/api/analysis')
def get_analysis():
    result = analyze_transactions()
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5000)
