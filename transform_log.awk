#! /usr/bin/awk -f 

# 1.http_reqs,1643101997,1.000000,,,,true,,GET,"http://127.0.0.1:1317/wasm/contracts/terra18j0wd0f62afcugw2rx5y8e6j5qjxd7d6qsc87r/store?query_msg={""config"":{}}",HTTP/1.1,default,,200,,,"http://127.0.0.1:1317/wasm/contracts/terra18j0wd0f62afcugw2rx5y8e6j5qjxd7d6qsc87r/store?query_msg={""config"":{}}",
# 2.http_req_duration,1643101997,2.069201,,,,true,,GET,"http://127.0.0.1:1317/wasm/contracts/terra18j0wd0f62afcugw2rx5y8e6j5qjxd7d6qsc87r/store?query_msg={""config"":{}}",HTTP/1.1,default,,200,,,"http://127.0.0.1:1317/wasm/contracts/terra18j0wd0f62afcugw2rx5y8e6j5qjxd7d6qsc87r/store?query_msg={""config"":{}}",
# 3.http_req_blocked,1643101997,19.225506,,,,true,,GET,"http://127.0.0.1:1317/wasm/contracts/terra18j0wd0f62afcugw2rx5y8e6j5qjxd7d6qsc87r/store?query_msg={""config"":{}}",HTTP/1.1,default,,200,,,"http://127.0.0.1:1317/wasm/contracts/terra18j0wd0f62afcugw2rx5y8e6j5qjxd7d6qsc87r/store?query_msg={""config"":{}}",
# 4.http_req_connecting,1643101997,19.042426,,,,true,,GET,"http://127.0.0.1:1317/wasm/contracts/terra18j0wd0f62afcugw2rx5y8e6j5qjxd7d6qsc87r/store?query_msg={""config"":{}}",HTTP/1.1,default,,200,,,"http://127.0.0.1:1317/wasm/contracts/terra18j0wd0f62afcugw2rx5y8e6j5qjxd7d6qsc87r/store?query_msg={""config"":{}}",
# 5.http_req_tls_handshaking,1643101997,0.000000,,,,true,,GET,"http://127.0.0.1:1317/wasm/contracts/terra18j0wd0f62afcugw2rx5y8e6j5qjxd7d6qsc87r/store?query_msg={""config"":{}}",HTTP/1.1,default,,200,,,"http://127.0.0.1:1317/wasm/contracts/terra18j0wd0f62afcugw2rx5y8e6j5qjxd7d6qsc87r/store?query_msg={""config"":{}}",
# 6.http_req_sending,1643101997,0.216120,,,,true,,GET,"http://127.0.0.1:1317/wasm/contracts/terra18j0wd0f62afcugw2rx5y8e6j5qjxd7d6qsc87r/store?query_msg={""config"":{}}",HTTP/1.1,default,,200,,,"http://127.0.0.1:1317/wasm/contracts/terra18j0wd0f62afcugw2rx5y8e6j5qjxd7d6qsc87r/store?query_msg={""config"":{}}",
# 7.http_req_waiting,1643101997,1.776042,,,,true,,GET,"http://127.0.0.1:1317/wasm/contracts/terra18j0wd0f62afcugw2rx5y8e6j5qjxd7d6qsc87r/store?query_msg={""config"":{}}",HTTP/1.1,default,,200,,,"http://127.0.0.1:1317/wasm/contracts/terra18j0wd0f62afcugw2rx5y8e6j5qjxd7d6qsc87r/store?query_msg={""config"":{}}",
# 8.http_req_receiving,1643101997,0.077039,,,,true,,GET,"http://127.0.0.1:1317/wasm/contracts/terra18j0wd0f62afcugw2rx5y8e6j5qjxd7d6qsc87r/store?query_msg={""config"":{}}",HTTP/1.1,default,,200,,,"http://127.0.0.1:1317/wasm/contracts/terra18j0wd0f62afcugw2rx5y8e6j5qjxd7d6qsc87r/store?query_msg={""config"":{}}",
# 9.http_req_failed,1643101997,0.000000,,,,true,,GET,"http://127.0.0.1:1317/wasm/contracts/terra18j0wd0f62afcugw2rx5y8e6j5qjxd7d6qsc87r/store?query_msg={""config"":{}}",HTTP/1.1,default,,200,,,"http://127.0.0.1:1317/wasm/contracts/terra18j0wd0f62afcugw2rx5y8e6j5qjxd7d6qsc87r/store?query_msg={""config"":{}}",
# 10.data_sent,1643101997,169.000000,,,,,,,,,default,,,,,,
# 11.data_received,1643101997,509.000000,,,,,,,,,default,,,,,,
# 12.iteration_duration,1643101997,21.749667,,,,,,,,,default,,,,,,
# 13.iterations,1643101997,1.000000,,,,,,,,,default,,,,,,

BEGIN { FS="," }
{ if (NR%11==1)
     {print $1,$2,$3}
else (NR%5=)

}