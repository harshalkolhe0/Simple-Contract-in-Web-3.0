pragma solidity >=0.6.0;

contract Counter{
    uint count;

    event Increment(uint value);
    event Decrement(uint value);

    constructor() public {
        count=0;
    }

    function getCount() view public returns(uint)
    {
        return count;
    }

    function increment() public{
        count+=1;
        emit Increment(count);
    }
    function decrement() public{
        count-=1;
        emit Decrement(count);
    }
}