const {Web3} = require('web3');
const {fs} = require('fs');

// Configurar la conexión con Ganache
const web3 = new Web3('http://localhost:8545');

// Leer el bytecode y el ABI del contrato compilado
const bytecode = fs.readFileSync('SimpleStorage_sol_SimpleStorage.bin', 'utf8');
const abi = JSON.parse(fs.readFileSync('SimpleStorage_sol_SimpleStorage.abi', 'utf8'));

// Crear una instancia del contrato
const contract = new web3.eth.Contract(abi);

// Obtener una lista de cuentas de Ganache
web3.eth.getAccounts()
    .then(accounts => {
        // Desplegar el contrato desde la primera cuenta
        return contract.deploy({
            data: '0x' + bytecode,
        }).send({
            from: accounts[0],
            gas: 1500000,
            gasPrice: '30000000000'
        });
    })
    .then((newContractInstance) => {
        console.log('Contrato desplegado en la dirección:', newContractInstance.options.address);
    })
    .catch((error) => {
        console.error('Error al desplegar el contrato:', error);
    });
