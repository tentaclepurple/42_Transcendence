const fs = require('fs');
const ganache = require('ganache-cli');
const Web3 = require('web3');
const solc = require('solc');

// Leer el código fuente del contrato
const contractCode = fs.readFileSync('SimpleStorage.sol', 'utf8');

// Compilar el contrato con solcjs
const input = {
    language: 'Solidity',
    sources: {
        'SimpleStorage.sol': {
            content: contractCode
        }
    },
    settings: {
        outputSelection: {
            '*': {
                '*': ['*']
            }
        }
    }
};

const compiledContract = JSON.parse(solc.compile(JSON.stringify(input)));

// Obtener el bytecode y el ABI del contrato compilado
const bytecode = compiledContract.contracts['SimpleStorage.sol']['SimpleStorage'].evm.bytecode.object;
const abi = compiledContract.contracts['SimpleStorage.sol']['SimpleStorage'].abi;

const provider = ganache.provider();

// Conectar a la red de Ethereum (por ejemplo, utilizando Ganache)
const web3 = new Web3(provider);

// Obtener una lista de cuentas generadas por Ganache
web3.eth.getAccounts()
  .then(accounts => {
    // Usar una de las cuentas para desplegar el contrato (cambiar según tus necesidades)
    const fromAddress = accounts[0]; // Puedes cambiar el índice para usar una cuenta diferente

    // Obtener una instancia del objeto del contrato
    const Contract = new web3.eth.Contract(abi);

    // Desplegar el contrato
    Contract.deploy({
        data: '0x' + bytecode,
        // arguments: [constructorArguments] // Si tu contrato tiene argumentos de constructor
    })
    .send({
        from: fromAddress, // Usar la dirección obtenida
        gas: 2000000, // Limite de gas para el despliegue
        gasPrice: '20000000000' // Precio del gas
    })
    .then((newContractInstance) => {
        console.log('Contrato desplegado en la dirección:', newContractInstance.options.address);
    })
    .catch((error) => {
        console.error('Error al desplegar el contrato:', error);
    });
  })
  .catch(error => {
    console.error('Error al obtener cuentas:', error);
  });
