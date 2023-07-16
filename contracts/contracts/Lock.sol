// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.9;

// Uncomment this line to use console.log
// import "hardhat/console.sol";

interface IVerifier {
    function verify(
        uint256[2] memory a,
        uint256[2][2] memory b,
        uint256[2] memory c,
        uint256[2] memory input
    ) external returns (bool);
}

contract PromptMarketplace{/// @notice Explain to an end user what this does
/// @dev Explain to a developer any extra details
/// @param Documents a parameter just like in doxygen (must be followed by parameter name){

    uint256 promptCount;

    mapping (uint256 => bool) public isProof;
    mapping (address => bytes32[]) public userHashes;

    IVerifier verifier = IVerifier();


    constructor() public {
        promptCount = 0;
    }

    function mint(
        bytes calldata aigcData,
        string calldata uri,
        bytes calldata proof
    ) public returns (uint256 tokenId){

    }

    function mintPromptImage(
        bytes32 ipfsHash, 
        uint256[2] memory a,
        uint256[2][2] memory b,
        uint256[2] memory c,
        uint256[2] memory input) 
    public payable {
        
        require(isProof[a[0]] == false, "Prompt already minted");
        require(verifier.verify(a,b,c,input), "Invalid proof")
        isProof[a[0]] = true;
        userHashes[msg.sender].push(ipfsHash);
        promptCount++;
    }

    function getUserHashes(address user) public view returns (bytes32[] memory) {
        return userHashes[user];
    }



}