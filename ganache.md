
Instalar Node.js y npm:

    sudo apt update
    sudo apt install nodejs
    sudo apt install npm
    
Instalar Ganache:

Una vez que Node.js y npm estén instalados, puedes instalar Ganache globalmente utilizando npm. Ejecuta el siguiente comando en la terminal:

###  bash 
    sudo npm install -g ganache-cli
Ejecutar Ganache:

Ahora que Ganache está instalado, puedes ejecutarlo en tu subsistema Linux. Abre una terminal y ejecuta el siguiente comando:

    ganache-cli

Esto iniciará Ganache y generará un conjunto de cuentas de Ethereum con fondos ficticios que puedes utilizar para desarrollo y pruebas.

Usar Ganache con tu entorno de desarrollo:

Puedes conectar tu aplicación o entorno de desarrollo a Ganache utilizando la URL proporcionada por Ganache (por defecto, http://localhost:8545). Configura tu aplicación o herramienta de desarrollo para utilizar esta URL como el punto final de tu red de Ethereum.

Recuerda que Ganache es una cadena de bloques local y se utiliza comúnmente para desarrollo y pruebas. En un entorno de producción, deberías conectarte a la red principal de Ethereum u otra red de prueba.

Con estos pasos, deberías tener Ganache instalado y funcionando en tu subsistema Linux. Puedes comenzar a desarrollar y probar tus contratos inteligentes en este entorno local de Ethereum.

Ejemplo:

$ganache-cli
Ganache CLI v6.12.2 (ganache-core: 2.13.2)

Available Accounts
==================
(0) 0x7211413B08B36324E3f8C0da5c9017669FEadD2e (100 ETH)
(1) 0x55164fA548beB3Ef63228D81459961fF7960F508 (100 ETH)
(2) 0xa1f42f928E741fEF94C6798A41419857f4Ac7841 (100 ETH)
(3) 0xBfBF6957C8Ea455Cec17A11915f0c1Eb0d24aa00 (100 ETH)
(4) 0x1a69F997733CF800A3B6037567cA7455887E390B (100 ETH)
(5) 0x3ff2659098AA733258f98cB0Fe8AC6227e83baF8 (100 ETH)
(6) 0x8bDD3faBF08616a24d09d663580FB7353E8aaD98 (100 ETH)
(7) 0x7c4008A6f246cB294E3BDD4BE961A6bA589ca295 (100 ETH)
(8) 0xD9Da55B3E9fd9eADE540baf20509D9B43c9f973D (100 ETH)
(9) 0xdDd5c0869803b396A7A544F34Ee7C03107F252ee (100 ETH)

Private Keys
==================
(0) 0x4d735b6733487f5e9a79db44786ea5d4c283eac6ac6a1637f2edc8690f795bdc
(1) 0x2d94ac8f0bd07a3472775b02a4eeb1a6815a8414c35d61084ee75dc96d273950
(2) 0x61f94084c5e3387a3f62e1a8f50187bca79ed2c801d5eab0c26cdfcd40cb7c59
(3) 0x931be388eac6acdb8786336585db96a2737aff49b623ccb08f778c260919655c
(4) 0xb81dc61208c2fedd7a91f18082b2edf2172d552217f60155446d649f9c850439
(5) 0x3ca0c318bffdbf9b175a57c4208ceba37a23c3b9d4c624ebbaf8d69bcf21126f
(6) 0xda6bcfd716e330886b03bdd043d52aa1a2982671e2d4bca22e3bcf607484e5ab
(7) 0xb31cdeb7f1f631c320f201dbda9ab8350ae8d4300de9f28e740476867ff820e4
(8) 0xc718ebe99b466246141541de98bca17393fb8b88f7cbd8ddc262a49778cca7fe
(9) 0x93362321a0eb9d950c97c2d8952a7d8bf7f3ad4522b3424f61bfc85819bca709

HD Wallet
==================
Mnemonic:      denial comic year mad maze mechanic brain coffee evolve skin group vocal
Base HD Path:  m/44'/60'/0'/0/{account_index}

Gas Price
==================
20000000000

Gas Limit
==================
6721975

Call Gas Limit
==================
9007199254740991

Listening on 127.0.0.1:8545
