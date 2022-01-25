import http from 'k6/http';
import { Trend, Rate, Counter, Gauge } from 'k6/metrics';

//@ts-check
export const fail_counter = new Counter('FailedRequests')

//-⋯⋯⋅⋱⋰⋆⋅⋅⋄⋅⋅∶⋅⋅⋄▫▪▭┈┅✕⋅⋅⋄⋅⋅✕∶⋅⋅⋄⋱⋰⋯⋯⋯⋯⋅⋱⋰⋆⋅⋅⋄⋅⋅∶⋅⋅⋄▫▪▭┈┅✕⋅⋅⋄⋅⋅✕∶⋅⋅⋄⋱⋰⋯⋯⋯⋅⋱⋰⋆⋅⋅⋄⋅⋅∶⋅⋅⋄▫▪▭┈┅✕⋅⋅⋄⋅⋅✕∶⋅⋅⋄⋱⋰⋯⋯⋯

export const options = {
  stages: [
    { duration: '10s', target: 200 },
    // { duration: '10s', target: 300 },
    { duration: '10s', target: 400 },
    // { duration: '10s', target: 500 },
    // { duration: '10s', target: 600 },
    { duration: '10s', target: 700 },
  ],
  thresholds: {
    "http_req_duration": [
      {
        threshold     : 'p(95) < 100',
        abortOnFail   : false,           
        delayAbortEval: '2s',            
      },
    ],
  },
};

export default function () {
  http.get(
      bombay_endpoints[Math.floor(Math.random()*5)]['ep'])
}

const bombay_endpoints = [
  {ep: 'http://127.0.0.1:1317/cosmos/base/tendermint/v1beta1/blocks/latest',},         
  {ep: 'http://127.0.0.1:1317/cosmos/base/tendermint/v1beta1/validatorsets/latest'},
  {ep: 'http://127.0.0.1:1317/blocks/latest'},
  {ep: 'http://127.0.0.1:1317/wasm/contracts/terra1p4gg3p2ue6qy2qfuxtrmgv2ec3f4jmgqtazum8/store?query_msg={"prices":{}}',},// Anchor Price Oracle
  {ep: 'http://127.0.0.1:1317/wasm/contracts/terra18j0wd0f62afcugw2rx5y8e6j5qjxd7d6qsc87r/store?query_msg={"config":{}}',},// Anchor Liquidation Queue
  
  // {ep: 'http://127.0.0.1:1317/wasm/contracts/terra19mkj9nec6e3y5754tlnuz4vem7lzh4n0lc2s3l/store', params: {query_msg: { "pool": {} }}},
  // {ep: 'http://127.0.0.1:1317/wasm/contracts/terra1seddp6u43xys0q85lpce9j6xwje7x7zqsf3fud/store', params: {query_msg: { "pool": {} }}},// bEth & bLuna
]

// const columbus_endpoints = [
//   '/cosmos/base/tendermint/v1beta1/blocks/latest',         // 36k
//   '/cosmos/base/tendermint/v1beta1/validatorsets/latest'   // 28K

//   '/blocks/latest', 
// 
  // Anchor Price Oracle
  // '/wasm/contracts/terra1cgg6yef7qcdm070qftghfulaxmllgmvk77nc7t/store?query_msg={"prices":{}}',

  // Anchor Liquidation Queue
  // '/wasm/contracts/terra1e25zllgag7j9xsun3me4stnye2pcg66234je3u/store?query_msg={"config":{}}',

  // Kujira UST-KUJI Staking
  // '/wasm/contracts/terra1cf9q9lq7tdfju95sdw78y9e34a6qrq3rrc6dre/store?query_msg={"state":{}}',

  // bEth
  // '/wasm/contracts/terra1c0afrdc5253tkp5wt7rxhuj42xwyf2lcre0s7c/store?query_msg={"pool":{}}',

  // bLuna
  // '/wasm/contracts/terra1jxazgm67et0ce260kvrpfv50acuushpjsz2y0p/store?query_msg={"pool":{}}',
  // '/wasm/contracts/terra1seddp6u43xys0q85lpce9j6xwje7x7zqsf3fud/store?query_msg={"pool":{}}', 

  // Terraswap LUNA-UST Pair
  // '/wasm/contracts/terra1tndcaqxkpc5ce9qee5ggqf430mr2z3pefe5wj6/store?query_msg={"pool":{}}',

  // Pylon Governance
  // '/wasm/contracts/terra1xu8utj38xuw6mjwck4n97enmavlv852zkcvhgp/store?query_msg={"polls":{}}',
// ]