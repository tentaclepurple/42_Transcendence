import os
from web3 import Web3
from solcx import compile_standard

# Definir el nombre del archivo del contrato
contract_file = 'SimpleStorage.sol'

# Leer el código fuente del contrato
with open(contract_file, 'r') as file:
    contract_source_code = file.read()

# Compilar el contrato
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {
        contract_file: {
            "content": contract_source_code
        }
    },
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "evm.bytecode"]
            }
        }
    }
})

# Obtener el bytecode y el ABI del contrato compilado
contract_interface = compiled_sol['contracts'][contract_file]['SimpleStorage']
bytecode = contract_interface['evm']['bytecode']['object']
abi = contract_interface['abi']

# Establecer la conexión con la red de Ethereum (por ejemplo, Ganache)
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Obtener la cuenta predeterminada
account = web3.eth.accounts[0]

# Crear una instancia del contrato
SimpleStorage = web3.eth.contract(abi=abi, bytecode=bytecode)

# Desplegar el contrato
tx_hash = SimpleStorage.constructor().transact({'from': account})
tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

# Imprimir la dirección del contrato desplegado
print('Contrato desplegado en la dirección:', tx_receipt.contractAddress)
