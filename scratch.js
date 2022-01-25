import axios from "axios";


const bombay_endpoints = [
    {
        ep: 'http://127.0.0.1:1317/cosmos/base/tendermint/v1beta1/blocks/latest',
    },         // 36k
    {
        ep: 'http://127.0.0.1:1317/cosmos/base/tendermint/v1beta1/validatorsets/latest',   // 28K
    },
    {
        ep: 'http://127.0.0.1:1317/blocks/latest',
    },
    // Anchor Price Oracle
    {
        ep: 'http://127.0.0.1:1317/wasm/contracts/terra1p4gg3p2ue6qy2qfuxtrmgv2ec3f4jmgqtazum8/store?query_msg={"prices":{}}',
    },
    // Anchor Liquidation Queue
    {
        ep: 'http://127.0.0.1:1317/wasm/contracts/terra18j0wd0f62afcugw2rx5y8e6j5qjxd7d6qsc87r/store?query_msg={"config":{}}',
    },
    // // bEth
    // {
    //     ep: 'http://127.0.0.1:1317/wasm/contracts/terra19mkj9nec6e3y5754tlnuz4vem7lzh4n0lc2s3l/store', params: {
    //         query_msg: { "pool": {} }
    //     }
    // },
    // // bLuna
    // {
    //     ep: 'http://127.0.0.1:1317/wasm/contracts/terra1seddp6u43xys0q85lpce9j6xwje7x7zqsf3fud/store', params: {
    //         query_msg: { "pool": {} }
    //     }
    // },
]

// for (var k of bombay_endpoints){
//     axios.get(k['ep'] ).then(r=>console.log(r.data))
// }

