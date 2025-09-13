from dataclasses import dataclass
from datetime import date
@dataclass
class Transaction:
    date: date
    merchant: str
    amount: float
    category: str
    raw: tuple