cat k6_stages.csv | grep "waiting" | awk -F "," '{print$1 ,$3}'
cat k6_stages.csv | tail -n +2     | grep -E 'connecting|data_received|http_req_waiting' | awk -F "," '{print $1,$2,$3}'
