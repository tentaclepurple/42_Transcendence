module.exports = {
	networks: {
	  development: {
		host: "ganache-trascendence",
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
  