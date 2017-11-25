pragma solidity ^0.4.0;

contract Greeter {
  string public greeting;
  
  event LogGreeting();
  
  /// Greeter smart contract - Greeter() function called
  function Greeter() {
    greeting = 'Hello';
  }

  /// Greeter smart contract - setGreeter() function called
  function setGreeting(string _greeting) public {
    greeting = _greeting;
  }

  /// Greeter smart contract - greet() function called
  function greet() constant returns (string) {
    LogGreeting();
    return greeting;
  }
}