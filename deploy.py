from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()#loading env file
with open("./First.sol","r") as file:
    content=file.read()

print("Installing...")
install_solc("0.6.0")

compiled_sol =  compile_standard(
    {
        "language":"Solidity",
        "sources":{"First.sol":{"content":content}},
        "settings":{
            "outputSelection":{
                "*":{"*":["abi","metadata","evm.bytecode","evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)
#print(compiled_sol)
with open("compiled_code.json","w") as file:
    json.dump(compiled_sol,file)

bytecode =  compiled_sol["contracts"]["First.sol"]["Counter"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["First.sol"]["Counter"]["abi"]


# For connecting to rinkby #ganache
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/d97432b6f09346f8b8cc2bc56441fb27"))#http://127.0.0.1:7545
chain_id = 4 #1337
my_address = "0x17f9e475B23A49EDc486f61E5447bAB25cf905b5"
private_key = os.getenv("PRIVATE_KEY")

# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
#build a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")
# Send transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)


# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

# Working with deployed Contracts
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print(f"Initial Stored Value { simple_storage.functions.getCount().call() } ")
greeting_transaction = simple_storage.functions.increment().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_greeting_txn = w3.eth.account.sign_transaction(
    greeting_transaction, private_key=private_key
)
tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
print("Updating stored Value...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)

print(simple_storage.functions.getCount().call())