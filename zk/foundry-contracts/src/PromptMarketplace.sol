// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.9;

import "./verifier.sol";

// Uncomment this line to use console.log
// import "hardhat/console.sol";



contract PromptMarketplace{
    uint256 promptCount;

    mapping (uint256 => bool) public isProof;
    mapping (address => bytes32[]) public userHashes;

    Verifier verifier;

    constructor() public {
        promptCount = 0;
        verifier = new Verifier();
    }

    function mintPromptImage(
        bytes32 ipfsHash, 
        uint256[1] calldata pubInputs,
        bytes calldata proof
        ) 
    public payable {
        
        require(isProof[pubInputs[0]] == false, "Prompt already minted");
        require(verifier.verify(pubInputs, proof), "Invalid proof");
        isProof[pubInputs[0]] = true;
        userHashes[msg.sender].push(ipfsHash);
        promptCount++;
    }

    function getUserHashes(address user) public view returns (bytes32[] memory) {
        return userHashes[user];
    }
}