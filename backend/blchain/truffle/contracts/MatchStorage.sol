// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract MatchStorage {
    string[] private matchStorage;

    // Método para añadir un nuevo string al array
    function addString(string memory newString) public {
        matchStorage.push(newString);
    }

    // Método para devolver todo el array
    function getAllStrings() public view returns (string[] memory) {
        return matchStorage;
    }
}