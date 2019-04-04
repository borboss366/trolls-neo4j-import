curl -H accept:application/json -H content-type:application/json \
     -d '{"statements":[{"statement":"MATCH (p1:PROFILES)-[:RELATION]-(p2) RETURN ... LIMIT 4"}]}' \
     http://ws-10-0-1-234-37879.neo4jsandbox.com:443