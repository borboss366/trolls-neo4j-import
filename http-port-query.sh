curl -H accept:application/json -H content-type:application/json -u neo4j:tail-analyses-experiences \
     -d '{"statements":[{"statement":"MATCH (u:User) RETURN u"}]}' \
     http://52.3.253.48:37880/db/data/transaction/commit \
     | jq -r '(.results[0]) | .columns,.data[].row | @csv'
