def assign_category(transaction, rules):
    """
    Assigns a category to a transaction based on keyword rules.
    """
    # Normalize the merchant name for case-insensitive matching
    normalized_merchant = transaction.merchant.lower()

    # Iterate through the rules to find a matching keyword
    for category, keywords in rules.items():
        for keyword in keywords:
            if keyword in normalized_merchant:
                transaction.category = category
                return transaction

    # If no match is found, assign 'Uncategorized'
    transaction.category = 'Uncategorized'
    return transaction