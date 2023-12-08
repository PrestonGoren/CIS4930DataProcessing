class InMemoryDB:
    def __init__(self):
        self.main_state = {}
        self.transaction_state = None

    def get(self, key):
        # Return value from main_state regardless of transaction state
        return self.main_state.get(key, None)

    def put(self, key, val):
        if self.transaction_state is None:
            raise Exception("No transaction in progress")
        # Store updates in transaction_state
        self.transaction_state[key] = val

    def begin_transaction(self):
        if self.transaction_state is not None:
            raise Exception("Transaction already in progress")
        # Copy current state to transaction_state
        self.transaction_state = self.main_state.copy()

    def commit(self):
        if self.transaction_state is None:
            raise Exception("No transaction to commit")
        # Apply changes to main_state
        self.main_state = self.transaction_state
        self.transaction_state = None

    def rollback(self):
        if self.transaction_state is None:
            raise Exception("No transaction to rollback")
        # Discard transaction_state
        self.transaction_state = None

# Test the functionalities as per the scenarios provided

inmemoryDB = InMemoryDB()

# Test cases
print("Testing scenarios:")
print("1. Get on non-existent key 'A':", inmemoryDB.get("A"))  # None

try:
    inmemoryDB.put("A", 5)  # Error expected
except Exception as e:
    print("2. Error on put without transaction:", e)

inmemoryDB.begin_transaction()
inmemoryDB.put("A", 5)
print("3. Get 'A' within transaction (should still be None):", inmemoryDB.get("A"))  # None

inmemoryDB.put("A", 6)
inmemoryDB.commit()
print("4. Get 'A' after commit (should be 6):", inmemoryDB.get("A"))  # 6

try:
    inmemoryDB.commit()  # Error expected
except Exception as e:
    print("5. Error on commit without open transaction:", e)

try:
    inmemoryDB.rollback()  # Error expected
except Exception as e:
    print("6. Error on rollback without open transaction:", e)

print("7. Get on non-existent key 'B':", inmemoryDB.get("B"))  # None

inmemoryDB.begin_transaction()
inmemoryDB.put("B", 10)
inmemoryDB.rollback()
print("8. Get 'B' after rollback (should still be None):", inmemoryDB.get("B"))  # None
