//En Remix, "Dev Ganache provider" necesaria version de solidity 0.8.19

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
