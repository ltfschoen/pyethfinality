pragma solidity ^0.4.17;

contract Greeter {
    string public greeting;

    /// Greeter smart contract - LogGreeter() function event called
    event LogGreeting(string log);

    /// Greeter smart contract - Greeter() function called
    function Greeter() public {
        greeting = 'Hello';
    }

    /// Greeter smart contract - setGreeter() function called
    function setGreeting(string _greeting) public {
        greeting = _greeting;
    }

    /// Greeter smart contract - greet() function called
    function greet() public payable returns (string) {
        LogGreeting(greeting);
        return greeting;
    }

    /// Greeter smart contract - Fallback function called
    // Fallback function called when contract is called but
    // no existing function was specified.
    // Allows ETH sent to be reverted.
    function() public payable {
        LogGreeting('Reverting');
    }
}