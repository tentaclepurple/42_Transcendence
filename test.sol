// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PlayerScores {
    // Definir el mapa que almacenará las puntuaciones de los jugadores
    mapping(string => uint256) public playerScores;
    
    // Almacenar temporalmente datos para visualización
    string[] public playerNamesArray;

    // Función para establecer la puntuación de un jugador
    function setScore(string memory playerName, uint256 score) public {
        // Actualizar el mapa
        playerScores[playerName] = score;

        // Actualizar la matriz auxiliar
        if (score != 0) {
            playerNamesArray.push(playerName);
        }
    }

    // Función para obtener la puntuación de un jugador
    function getScore(string memory playerName) public view returns (uint256) {
        return playerScores[playerName];
    }

    // Función para obtener el estado actual del mapeo playerScores
    function getPlayerScoresState() public view returns (string[] memory, uint256[] memory) {
        uint256 length = playerNamesArray.length;

        string[] memory playerNames = new string[](length);
        uint256[] memory scores = new uint256[](length);

        for (uint256 i = 0; i < length; i++) {
            string memory playerName = playerNamesArray[i];
            playerNames[i] = playerName;
            scores[i] = playerScores[playerName];
        }

        return (playerNames, scores);
    }
}
