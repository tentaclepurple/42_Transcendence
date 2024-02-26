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
        // Llamar a la función getData del contrato para obtener el valor actual
        return contract.methods.getData().call({ from: accounts[0] });
    })
    .then((data) => {
        console.log('El valor actual del contrato es:', data);
        
        // Llamar a la función setData del contrato para establecer un nuevo valor
        return contract.methods.setData(99).send({ 
            from: accounts[0],
            gas: 2000000, // Limite de gas para la transacción
            gasPrice: '30000000000' // Precio del gas
        }); // Cambia el valor 99 por el que desees establecer
    })
    .then(() => {
        console.log('Se ha establecido un nuevo valor en el contrato.');
        
        // Llamar a la función getData del contrato nuevamente para obtener el valor cambiado
        return contract.methods.getData().call({ from: accounts[0] }); // Debería añadirse 'accounts[0]' aquí también
    })
    .then((newData) => {
        console.log('El valor actualizado del contrato es:', newData);
    })
    .catch((error) => {
        console.error('Error al interactuar con el contrato:', error);
    });