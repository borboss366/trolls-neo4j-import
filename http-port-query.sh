curl -H accept:application/json -H content-type:application/json \
     -d '{"statements":[{"statement":"MATCH (u:User) RETURN u LIMIT 1"}]}' \
     http://52.3.253.48:37880/db/data/transaction/commit \
     | jq -r '(.results[0]) | .columns,.data[].row | @csv'
