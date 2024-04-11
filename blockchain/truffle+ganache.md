
#### run ganache-cli
    ganache-cli

En otra terminal:

Crear carpeta para truffle (optional)

    truffle init

Se crea el sistema de archivos:

    build
    contracts
    migrations
    test

Creamos truffle-config.js en /

    module.exports = {
    	networks: {
    	  development: {
    		host: "127.0.0.1",
    		port: 8545, // Ajusta este puerto según la configuración de Ganache
    		network_id: "*", // Puedes usar un valor específico o "*" para cualquier network_id
    	  },
    	  // Otras configuraciones de red, como ropsten, rinkeby, mainnet, etc.
    	},
    	mocha: {
    	  // timeout: 100000
    	},
    	compilers: {
    	  solc: {
    		version: "0.8.19", // Versión exacta de solc-bin (puedes cambiarla según tus necesidades)
    		// docker: true,
    		// settings: {
    		//   optimizer: {
    		//     enabled: false,
    		//     runs: 200
    		//   },
    		//   evmVersion: "byzantium"
    		// }
    	  }
    	},
      };
  

Metemos el contrato .sol en /contracts

    // SPDX-License-Identifier: MIT
    pragma solidity 0.8.19;
    
    contract SimpleStorage {
        uint256 private data;
    
        event DataUpdated(uint256 newData);
    
        function setData(uint256 _data) external {
            data = _data;
            emit DataUpdated(_data);
        }
    
        function getData() external view returns (uint256) {
            return data;
        }
    }

Creamos 2_deploy_contracts.js en /migrations

    // 2_deploy_contracts.js
    
    const SimpleStorage = artifacts.require("SimpleStorage");
    
    module.exports = function (deployer) {
    deployer.deploy(SimpleStorage);
    };


Compilar el contrato

    truffle compile

Migrar contratos a la red de desarrollo

    truffle migrate --network development

Y lanzar consola truffle:

    truffle console --network development

o ejecutar script para interactuar con contrato:

    truffle exec myscript.js --network development


