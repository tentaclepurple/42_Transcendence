const {Web3} = require('web3');
const fs = require('fs');

// Configurar la conexión con Ganache (o la red Ethereum que estés usando)
const web3 = new Web3('http://127.0.0.1:8545'); // Cambia la URL por la de tu nodo Ethereum

// Leer el ABI del contrato
const abi = JSON.parse(fs.readFileSync('output/SimpleStorage_sol_SimpleStorage.abi', 'utf8'));

// Dirección del contrato desplegado
const contractAddress = '0x4eEA49EA23Af169AB1B1743247D67338b9FCD772'; // Reemplaza con la dirección de tu contrato

// Crear una instancia del contrato
const contract = new web3.eth.Contract(abi, contractAddress);

// Obtener una lista de cuentas de Ganache
web3.eth.getAccounts()
    .then(accounts => {
        // Realizar una transacción para llamar a la función setData del contrato
        return contract.methods.setData(42).send({ 
            from: accounts[0],
            gas: 2000000,
            gasPrice: '30000000000',
        }); // Cambia el valor 42 por el que desees establecer
    })
    .then(() => {
        // Llamar a la función getData del contrato para obtener el valor establecido
        return contract.methods.getData().call();
    })
    .then((data) => {
        console.log('El valor actual del contrato es:', data);
    })
    .catch((error) => {
        console.error('Error al interactuar con el contrato:', error);
    });
