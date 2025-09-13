from budgetbuddy.models.transaction import Transaction

class TransactionIterator:
    def __init__(self, transactions):
        self._transactions = transactions
        self._index = 0

    def __next__(self):
        if self._index < len(self._transactions):
            transaction = self._transactions[self._index]
            self._index += 1
            return transaction
        raise StopIteration

class TransactionLedger:
    def __init__(self, transactions=None):
        self.transactions = transactions if transactions is not None else []

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def __iter__(self):
        return TransactionIterator(self.transactions)

    def filter_by_month(self, year, month):
        filtered_transactions = [
            t for t in self.transactions 
            if t.date.year == year and t.date.month == month
        ]
        return TransactionLedger(filtered_transactions)

    def filter_by_category(self, category_name):
        filtered_transactions = [
            t for t in self.transactions 
            if t.category.lower() == category_name.lower()
        ]
        return TransactionLedger(filtered_transactions)

    def search_by_text(self, query):
        normalized_query = query.lower()
        filtered_transactions = [
            t for t in self.transactions 
            if normalized_query in t.merchant.lower()
        ]
        return TransactionLedger(filtered_transactions)