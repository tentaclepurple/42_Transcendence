const { Web3 } = require('web3');
const fs = require('fs');

// Configurar la conexión con Ganache (o la red Ethereum que estés usando)
const web3 = new Web3('http://127.0.0.1:8545'); // Cambia la URL por la de tu nodo Ethereum

// Leer el ABI del contrato
const abi = JSON.parse(fs.readFileSync('output/SimpleStorage_sol_SimpleStorage.abi', 'utf8'));

// Dirección del contrato desplegado
const contractAddress = '0x4eEA49EA23Af169AB1B1743247D67338b9FCD772'; // Reemplaza con la dirección de tu contrato

// Crear una instancia del contrato
const contract = new web3.eth.Contract(abi, contractAddress);

async function main() {
    try {
        // Obtener una lista de cuentas de Ganache
        const accounts = await web3.eth.getAccounts();

        // Obtener el valor pasado como argumento para setData
        const value = process.argv[2]; // El primer argumento después del nombre del script

        // Verificar si el valor es un número válido
        if (!value || isNaN(value)) {
            console.error('Error: El valor proporcionado no es válido.');
            return;
        }

        // Llamar a la función getData del contrato para obtener el valor actual
        const data = await contract.methods.getData().call({ from: accounts[0] });
        console.log('El valor actual del contrato es:', data);
        
        // Llamar a la función setData del contrato para establecer un nuevo valor
        await contract.methods.setData(value).send({ 
            from: accounts[0],
            gas: 2000000, // Limite de gas para la transacción
            gasPrice: '30000000000' // Precio del gas
        });
        console.log('Se ha establecido un nuevo valor en el contrato:', value);
        
        // Llamar a la función getData del contrato nuevamente para obtener el valor cambiado
        const newData = await contract.methods.getData().call({ from: accounts[0] });
        console.log('El valor actualizado del contrato es:', newData);
    } catch (error) {
        console.error('Error al interactuar con el contrato:', error);
    }
}

main();
