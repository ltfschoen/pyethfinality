Output when running demo_mockchain.py using:
    `chain = gen_chain(max_height=3, p_revert=0.6, num_accounts=2, max_transfers=1)`

root@f42e80e34039:/code# python3 scripts/src/main.py
Main path in Docker container is: /code/scripts
Running Demo - Mockchain
json dumps: [
    {
        "balances": {
            "0xdfd5f9": 5,
            "0xe25388": 37
        },
        "hash": "0x6f0a32",
        "number": 0,
        "prevhash": "0x46e8e7",
        "transfers": []
    },
    {
        "balances": {
            "0xdfd5f9": 5,
            "0xe25388": 37
        },
        "hash": "0xa75153",
        "number": 1,
        "prevhash": "0x6f0a32",
        "transfers": []
    },
    {
        "balances": {
            "0xdfd5f9": 0,
            "0xe25388": 42
        },
        "hash": "0x71b766",
        "number": 2,
        "prevhash": "0xa75153",
        "transfers": [
            {
                "amount": 5,
                "receiver": "0xe25388",
                "sender": "0xdfd5f9"
            }
        ]
    },
    {
        "balances": {
            "0xdfd5f9": 9,
            "0xe25388": 33
        },
        "hash": "0x1827fd",
        "number": 1,
        "prevhash": "0x6f0a32",
        "transfers": [
            {
                "amount": 4,
                "receiver": "0xdfd5f9",
                "sender": "0xe25388"
            }
        ]
    },
    {
        "balances": {
            "0xdfd5f9": 9,
            "0xe25388": 33
        },
        "hash": "0xc4fdbc",
        "number": 2,
        "prevhash": "0x1827fd",
        "transfers": []
    },
    {
        "balances": {
            "0xdfd5f9": 0,
            "0xe25388": 42
        },
        "hash": "0x0b7ab1",
        "number": 1,
        "prevhash": "0x6f0a32",
        "transfers": [
            {
                "amount": 5,
                "receiver": "0xe25388",
                "sender": "0xdfd5f9"
            }
        ]
    },
    {
        "balances": {
            "0xdfd5f9": 4,
            "0xe25388": 38
        },
        "hash": "0x236222",
        "number": 2,
        "prevhash": "0x0b7ab1",
        "transfers": [
            {
                "amount": 4,
                "receiver": "0xdfd5f9",
                "sender": "0xe25388"
            }
        ]
    },
    {
        "balances": {
            "0xdfd5f9": 5,
            "0xe25388": 37
        },
        "hash": "0xfb8ee7",
        "number": 1,
        "prevhash": "0x6f0a32",
        "transfers": []
    },
    {
        "balances": {
            "0xdfd5f9": 39,
            "0xe25388": 3
        },
        "hash": "0x5a9a34",
        "number": 2,
        "prevhash": "0xfb8ee7",
        "transfers": [
            {
                "amount": 34,
                "receiver": "0xdfd5f9",
                "sender": "0xe25388"
            }
        ]
    },
    {
        "balances": {
            "0xdfd5f9": 39,
            "0xe25388": 3
        },
        "hash": "0x512d98",
        "number": 3,
        "prevhash": "0x5a9a34",
        "transfers": []
    }
]
blocks: 10 max reverted:1
total transfers:5 unique transfers:3