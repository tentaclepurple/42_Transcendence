from web3 import Web3, middleware
import json
import warnings

# Conéctate a la instancia local de Ganache
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))  # Asegúrate de usar el puerto correcto

# web3.middleware_onion.inject(middleware.simple_cache_middleware, layer=0)
# web3.middleware_onion.inject(middleware.ignore_eth_warning_middleware, layer=0)

warnings.filterwarnings("ignore", category=UserWarning, module="web3")

# Dirección de la cuenta desde la que desplegarás el contrato (cambia según tu configuración)
cuenta = web3.eth.accounts[0]

print(cuenta)

# Obtén el nonce actual de la cuenta
nonce = web3.eth.get_transaction_count(cuenta)

# Ruta al ABI y bytecode del contrato ya compilado
ruta_abi = './build/SimpleStorage_sol_SimpleStorage.abi'
ruta_bytecode = './build/SimpleStorage_sol_SimpleStorage.bin'
with open(ruta_abi, 'r') as archivo_abi:
    abi = json.load(archivo_abi)
with open(ruta_bytecode, 'r') as archivo_bytecode:
    bytecode = archivo_bytecode.read()

# Crear instancia del contrato
contrato = web3.eth.contract(abi=abi, bytecode=bytecode)

# Desplegar el contrato
try:
    transaccion = contrato.constructor().build_transaction({
        'from': cuenta,
        'gas': 4712388,
        'nonce': nonce,
        # Eliminamos 'gas_price' ya que no es necesario para Ganache
        # 'gas_price': web3.to_wei('1', 'gwei'), 
    })
except ValueError as e:
    print(f"Error al construir la transacción: {e}")
    # Manejar la excepción aquí según sea necesario
    # Puedes imprimir un mensaje, registrar el error, o tomar otra acción

# Realizar la firma solo si la transacción fue construida con éxito
if 'transaccion' in locals():
    firma = web3.eth.account.sign_transaction(transaccion, '0x95792eaedf73edacdc084180d0d9a563fed476f4fd7407f29315d399c3532ca7')  # Reemplaza 'tu_clave_privada'
    tx_hash = web3.eth.send_raw_transaction(firma.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    # Obtener la dirección del contrato desplegado
    direccion_contrato = tx_receipt['contractAddress']
    print(f'Contrato desplegado en la dirección: {direccion_contrato}')
