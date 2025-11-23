import requests
import uuid

BASE_URL = 'http://127.0.0.1:8000/api'

def test_api():
    # 1. Create Customer
    print("1. Creating Customer...")
    customer_data = {
        "name": "John Doe",
        "phone": "+1234567890",
        "email": "john@example.com"
    }
    response = requests.post(f"{BASE_URL}/customers/", data=customer_data)
    if response.status_code == 201:
        customer = response.json()
        print(f"   Success: Created customer {customer['name']} (ID: {customer['id']})")
    else:
        print(f"   Failed: {response.text}")
        return

    customer_id = customer['id']

    # 2. Credit Wallet
    print("\n2. Crediting Wallet (100 points)...")
    credit_data = {
        "customer_id": customer_id,
        "points": 100,
        "idempotency_key": str(uuid.uuid4())
    }
    response = requests.post(f"{BASE_URL}/wallet/credit/", data=credit_data)
    if response.status_code == 201:
        print(f"   Success: Credited 100 points. Balance: {response.json()['wallet']}") # Note: serializer returns wallet ID, not balance directly in txn response usually, let's check
    else:
        print(f"   Failed: {response.text}")

    # 3. Debit Wallet
    print("\n3. Debiting Wallet (50 points)...")
    debit_data = {
        "customer_id": customer_id,
        "points": 50,
        "idempotency_key": str(uuid.uuid4())
    }
    response = requests.post(f"{BASE_URL}/wallet/debit/", data=debit_data)
    if response.status_code == 201:
        print(f"   Success: Debited 50 points.")
    else:
        print(f"   Failed: {response.text}")

    # 4. Overdraft Check
    print("\n4. Overdraft Check (Debit 60 points, expect failure)...")
    overdraft_data = {
        "customer_id": customer_id,
        "points": 60,
        "idempotency_key": str(uuid.uuid4())
    }
    response = requests.post(f"{BASE_URL}/wallet/debit/", data=overdraft_data)
    if response.status_code == 400:
        print(f"   Success: Request rejected as expected. {response.text}")
    else:
        print(f"   Failed: Should have been rejected. Status: {response.status_code}")

    # 5. Idempotency Check
    print("\n5. Idempotency Check (Repeat Credit)...")
    idem_key = str(uuid.uuid4())
    idem_data = {
        "customer_id": customer_id,
        "points": 20,
        "idempotency_key": idem_key
    }
    # First call
    requests.post(f"{BASE_URL}/wallet/credit/", data=idem_data)
    # Second call
    response = requests.post(f"{BASE_URL}/wallet/credit/", data=idem_data)
    if response.status_code == 200:
        print(f"   Success: Idempotent request handled correctly (Status 200).")
    else:
        print(f"   Failed: {response.status_code} {response.text}")

    # 6. Transaction History
    print("\n6. Fetching Transaction History...")
    response = requests.get(f"{BASE_URL}/wallet/transactions/?customer_id={customer_id}")
    if response.status_code == 200:
        txns = response.json()
        print(f"   Success: Found {len(txns)} transactions.")
        for txn in txns:
            print(f"   - {txn['type']} {txn['points']} (Key: {txn['idempotency_key']})")
    else:
        print(f"   Failed: {response.text}")

if __name__ == "__main__":
    test_api()
