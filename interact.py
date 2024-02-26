#this script works with ganache-cli and contract compiled and deployed in remix

from web3 import Web3
from eth_account import Account
#from web3.middleware import geth_poa_middleware

# Conectar a la instancia de Ganache (o tu nodo Ethereum local)
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545')) #host y puerto que pone en ganache-cli

# Dirección del contrato desplegado en Remix
contract_address = '0x34E047d0FCD820EBEe0b03827caE808B9aAf4c83'  # Reemplaza con la dirección de tu contrato

# ABI del contrato
contract_abi = [
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "newData",
				"type": "uint256"
			}
		],
		"name": "DataUpdated",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_data",
				"type": "uint256"
			}
		],
		"name": "setData",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getData",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

# Crear una instancia del contrato
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Obtener el valor actual almacenado en el contrato
current_value = contract.functions.getData().call()
print(f'Valor actual en el contrato: {current_value}')

# Actualizar el valor almacenado en el contrato (necesitas la clave privada para firmar la transacción)
#sacada de ganache-cli
private_key = '0x776a1d5ae9683851d1b325feb95aa33b20a624dc5282a5f1d938607cd6488424'  
account = Account.from_key(private_key)

# Construir la transacción
transaction = contract.functions.setData(12).build_transaction({
    'from': account.address,
    'gas': 2000000,  # Puedes ajustar este valor según sea necesario
    'gasPrice': web3.to_wei('50', 'gwei'),
    'nonce': web3.eth.get_transaction_count(account.address),
})

# Firmar la transacción
signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)

# Enviar la transacción
transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

# Esperar la confirmación de la transacción
transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

# Obtener el nuevo valor almacenado en el contrato
updated_value = contract.functions.getData().call()
print(f'Nuevo valor en el contrato: {updated_value}')
