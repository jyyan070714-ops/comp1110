from collections import defaultdict
from datetime import datetime


def check_alerts(transactions, rules):
    alert_list = []
    for rule in rules:
        category = rule['category']
        time_period = rule['time period']
        threshold = rule['threshold']
        alert_type = rule['alert type']
        if alert_type == 'cap':
            alert_list += _check_spending_cap(transactions, category, time_period, threshold)
        elif alert_type == 'percentage':
            alert_list += _check_percentage(transactions, category, threshold)
    alert_list += _check_uncategorized(transactions)
    alert_list += _check_consecutive_overspend(transactions, rules)
    return alert_list


def _check_spending_cap(transactions, category, time_period, threshold):
    alerts = []
    period_totals = defaultdict(float)
    for t in transactions:
        if t['category'] != category:
            continue
        try:
            d = datetime.strptime(t['date'], '%Y-%m-%d')
        except ValueError:
            continue
        if time_period == 'daily':
            key = t['date']
        elif time_period == 'weekly':
            key = f"{d.year}-W{d.strftime('%W')}"
        elif time_period == 'monthly':
            key = d.strftime('%Y-%m')
        else:
            continue
        period_totals[key] += t['amount']
    for period, total in sorted(period_totals.items()):
        if total > threshold:
            alerts.append(f"[CAP EXCEEDED] {category} ({time_period}) {period}: HK${total:.2f} > cap HK${threshold:.2f}")
    return alerts


def _check_percentage(transactions, category, threshold_pct):
    total = sum(t['amount'] for t in transactions)
    if total == 0:
        return []
    cat_total = sum(t['amount'] for t in transactions if t['category'] == category)
    pct = (cat_total / total) * 100
    if pct > threshold_pct:
        return [f"[HIGH %] {category} is {pct:.1f}% of total spending (threshold: {threshold_pct:.1f}%)"]
    return []


def _check_uncategorized(transactions):
    count = sum(1 for t in transactions if t['category'] == 'Others')
    if count > 0:
        return [f"[UNCATEGORIZED] {count} transaction(s) in 'Others' — consider recategorizing."]
    return []


def _check_consecutive_overspend(transactions, rules):
    alerts = []
    daily_cap_rules = [r for r in rules if r['alert type'] == 'cap' and r['time period'] == 'daily']
    for rule in daily_cap_rules:
        category = rule['category']
        cap = rule['threshold']
        daily_totals = defaultdict(float)
        for t in transactions:
            if t['category'] == category:
                daily_totals[t['date']] += t['amount']
        streak = 0
        streak_alerted = False
        prev_date = None
        sortable_dates = []
        for date_str in daily_totals:
            try:
                d = datetime.strptime(date_str, '%Y-%m-%d')
                sortable_dates.append((d, date_str))
            except ValueError:
                continue
        for d, date_str in sorted(sortable_dates):
            if daily_totals[date_str] > cap:
                if prev_date and (d - prev_date).days == 1:
                    streak += 1
                else:
                    streak = 1
                    streak_alerted = False
                if streak >= 3 and not streak_alerted:
                    alerts.append(f"[STREAK] {category} exceeded daily cap HK${cap:.2f} for {streak} consecutive days (latest: {date_str})")
                    streak_alerted = True
            else:
                streak = 0
                streak_alerted = False
            prev_date = d
    return alerts
