import http from 'k6/http';
import { Trend, Rate, Counter, Gauge } from 'k6/metrics';

//@ts-check
export const fail_counter = new Counter('FailedRequests')

//-⋯⋯⋅⋱⋰⋆⋅⋅⋄⋅⋅∶⋅⋅⋄▫▪▭┈┅✕⋅⋅⋄⋅⋅✕∶⋅⋅⋄⋱⋰⋯⋯⋯⋯⋅⋱⋰⋆⋅⋅⋄⋅⋅∶⋅⋅⋄▫▪▭┈┅✕⋅⋅⋄⋅⋅✕∶⋅⋅⋄⋱⋰⋯⋯⋯⋅⋱⋰⋆⋅⋅⋄⋅⋅∶⋅⋅⋄▫▪▭┈┅✕⋅⋅⋄⋅⋅✕∶⋅⋅⋄⋱⋰⋯⋯⋯
const endpoints = [
  '/cosmos/base/tendermint/v1beta1/blocks/latest',         // 36k
  '/cosmos/base/tendermint/v1beta1/validatorsets/latest'   // 28K
  // '/blocks/latest', 
  // '/wasm/contracts/terra1cgg6yef7qcdm070qftghfulaxmllgmvk77nc7t/store?query_msg={"prices":{}}',
  // '/wasm/contracts/terra1e25zllgag7j9xsun3me4stnye2pcg66234je3u/store?query_msg={"config":{}}',
  // '/wasm/contracts/terra1cf9q9lq7tdfju95sdw78y9e34a6qrq3rrc6dre/store?query_msg={"state":{}}',
  // '/wasm/contracts/terra1c0afrdc5253tkp5wt7rxhuj42xwyf2lcre0s7c/store?query_msg={"pool":{}}',
  // '/wasm/contracts/terra1jxazgm67et0ce260kvrpfv50acuushpjsz2y0p/store?query_msg={"pool":{}}',
  // '/wasm/contracts/terra1tndcaqxkpc5ce9qee5ggqf430mr2z3pefe5wj6/store?query_msg={"pool":{}}',
  // '/wasm/contracts/terra1xu8utj38xuw6mjwck4n97enmavlv852zkcvhgp/store?query_msg={"polls":{}}',
]

export const options = {
  // ext: {
  //   loadimpact: {
  //     apm: [
  //       {
  //         provider: 'prometheus',
  //         remoteWriteURL: 'https://prometheus-prod-10-prod-us-central-0.grafana.net/api/prom/push',
  //         credentials: {
  //           username: '308504',
  //           password: 'eyJrIjoiZDM1MWRlMzkwMGRkMGVlMWE5NTAyNzc2M2Q5MmRhNmI0ZTc2NjU3YSIsIm4iOiJ0ZXJyYWs2IiwiaWQiOjU5MTQ5N30=',
  //         },
  //         // optional parameters
  //         // metrics: ['http_req_sending', 'my_rate', 'my_gauge'], // ...
  //         includeDefaultMetrics: true,
  //         includeTestRunId: false,
  //       },
  //     ],
  //   },
  // },
  vus       : 200,
  duration  : "10s",
  // thresholds: {
    // http_req_failed: [{ threshold: 'count<1', abortOnFail: true, delayAbortEval: '2s'}],
    // FailedRequests : [{ threshold: 'count<1', abortOnFail: true, delayAbortEval: '2s'}],
  // },
};

export default function () {
  // Randomized query
  // http.get( encodeURI(`http://127.0.0.1:1317${endpoints[Math.floor(Math.random() * 10)]}`)) 
http.get(encodeURI('http://127.0.0.1:1317/cosmos/base/tendermint/v1beta1/blocks/latest'))
  // resp.status !== 200 ?    FailedReqs.add(1) : ( ()=>{} )();

  // sleep(5)
}