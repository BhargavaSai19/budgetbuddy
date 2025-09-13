from collections import defaultdict

def spend_by_category(ledger):
    """
    Aggregates total spending for each category in the ledger.
    Returns a dictionary of {category: total_spend}.
    """
    category_spend = defaultdict(float)
    for transaction in ledger:
        if transaction.amount < 0:
            category_spend[transaction.category] += abs(transaction.amount)
    return dict(category_spend)

def top_merchants(ledger, top_n):
    """
    Identifies the top N merchants by total spending.
    Returns a sorted list of (merchant, total_spend) tuples.
    """
    merchant_spend = defaultdict(float)
    for transaction in ledger:
        if transaction.amount < 0:
            merchant_spend[transaction.merchant.lower().strip()] += abs(transaction.amount)

    sorted_merchants = sorted(merchant_spend.items(), key=lambda item: item[1], reverse=True)
    return sorted_merchants[:top_n]

def monthly_summary(ledger):
    """
    Calculates total income, expenses, and net balance for the ledger.
    Returns a dictionary with these values.
    """
    total_income = 0
    total_expenses = 0

    for transaction in ledger:
        if transaction.amount > 0:
            total_income += transaction.amount
        else:
            total_expenses += transaction.amount
    
    net_balance = total_income + total_expenses
    
    return {
        'income': total_income,
        'expenses': abs(total_expenses),  # Stored as a positive number for display
        'net_balance': net_balance
    }