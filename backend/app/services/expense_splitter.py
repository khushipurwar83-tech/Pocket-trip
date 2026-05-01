from typing import Dict, List

def split_equal(amount: float, users: List[str]) -> Dict[str, float]:
    """
    Splits the amount equally among a list of users.
    """
    if not users:
        return {}
    share = round(amount / len(users), 2)
    return {user: share for user in users}

def split_custom(amount: float, custom_splits: Dict[str, float]) -> Dict[str, float]:
    """
    Validates and returns custom splits. Ensures they sum up to the total amount.
    """
    if abs(sum(custom_splits.values()) - amount) > 0.01:
        raise ValueError("Sum of custom amounts does not match total amount")
    return custom_splits

def calculate_balances(expenses: List[dict]) -> Dict[str, Dict[str, float]]:
    """
    Calculates who owes whom based on list of expenses.
    expenses format: [{'paid_by': 'user1', 'amount': 100, 'splits': {'user1': 50, 'user2': 50}}]
    """
    balances = {}
    net_balances = {}
    
    # Calculate net balance for each user
    for exp in expenses:
        paid_by = exp['paid_by']
        amount = exp['amount']
        splits = exp['splits'] 

        if paid_by not in net_balances:
            net_balances[paid_by] = 0
        net_balances[paid_by] += amount

        for user_id, owed in splits.items():
            if user_id not in net_balances:
                net_balances[user_id] = 0
            net_balances[user_id] -= owed

    # Separate into those who owe money (debtors) and those owed money (creditors)
    debtors = []
    creditors = []
    
    for user_id, balance in net_balances.items():
        if balance < -0.01:
            debtors.append([user_id, -balance])
        elif balance > 0.01:
            creditors.append([user_id, balance])

    # Sort descending by amount 
    debtors.sort(key=lambda x: x[1], reverse=True)
    creditors.sort(key=lambda x: x[1], reverse=True)

    i = 0
    j = 0
    while i < len(debtors) and j < len(creditors):
        debtor_id, debt_amount = debtors[i]
        creditor_id, credit_amount = creditors[j]
        
        settle_amount = round(min(debt_amount, credit_amount), 2)
        
        if debtor_id not in balances:
            balances[debtor_id] = {}
        balances[debtor_id][creditor_id] = settle_amount
        
        debtors[i][1] -= settle_amount
        creditors[j][1] -= settle_amount
        
        if debtors[i][1] < 0.01:
            i += 1
        if creditors[j][1] < 0.01:
            j += 1
            
    return balances
