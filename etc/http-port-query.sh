curl -H accept:application/json -H content-type:application/json -u neo4j:tail-analyses-experiences \
     -d '{"statements":[{"statement":"MATCH (u:User) RETURN u.id as id, u.name as name, u.friends_count as friends_count, u.screen_name as screen_name, u.location as location, u.description as description, u.listed_count as listed_count, u.followers_count as followers_count, u.favourites_count as favourites_count, u.created_at as created_at, u.user_key as user_key, u.lang as lang, u.verified as verified, u.time_zone as time_zone, u.statuses_count as statuses_count"}]}' \
     http://52.3.253.48:37880/db/data/transaction/commit \
     | jq -r '(.results[0]) | .columns,.data[].row | map(if type == "string" then gsub("\n|\r"; "þ") else . end) | @csv' > dump/node_User.csv

curl -H accept:application/json -H content-type:application/json -u neo4j:tail-analyses-experiences \
     -d '{"statements":[{"statement":"MATCH (u:Troll) RETURN u.id as id, u.name as name, u.friends_count as friends_count, u.screen_name as screen_name, u.location as location, u.description as description, u.listed_count as listed_count, u.followers_count as followers_count, u.favourites_count as favourites_count, u.created_at as created_at, u.user_key as user_key, u.lang as lang, u.verified as verified, u.time_zone as time_zone, u.statuses_count as statuses_count"}]}' \
     http://52.3.253.48:37880/db/data/transaction/commit \
     | jq -r '(.results[0]) | .columns,.data[].row | map(if type == "string" then gsub("\n|\r"; "þ") else . end) | @csv' > dump/node_Troll.csv

curl -H accept:application/json -H content-type:application/json -u neo4j:tail-analyses-experiences \
     -d '{"statements":[{"statement":"MATCH (u:URL) RETURN u.expanded_url as expanded_url"}]}' \
     http://52.3.253.48:37880/db/data/transaction/commit \
     | jq -r '(.results[0]) | .columns,.data[].row | map(if type == "string" then gsub("\n|\r"; "þ") else . end) | @csv' > dump/node_URL.csv

curl -H accept:application/json -H content-type:application/json -u neo4j:tail-analyses-experiences \
     -d '{"statements":[{"statement":"MATCH (u:Hashtag) RETURN u.tag as tag"}]}' \
     http://52.3.253.48:37880/db/data/transaction/commit \
     | jq -r '(.results[0]) | .columns,.data[].row | map(if type == "string" then gsub("\n|\r"; "þ") else . end) | @csv' > dump/node_Hashtag.csv

curl -H accept:application/json -H content-type:application/json -u neo4j:tail-analyses-experiences \
     -d '{"statements":[{"statement":"MATCH (u:Source) RETURN u.name as name"}]}' \
     http://52.3.253.48:37880/db/data/transaction/commit \
     | jq -r '(.results[0]) | .columns,.data[].row | map(if type == "string" then gsub("\n|\r"; "þ") else . end) | @csv' > dump/node_Source.csv

curl -H accept:application/json -H content-type:application/json -u neo4j:tail-analyses-experiences \
     -d '{"statements":[{"statement":"MATCH (u:Tweet) RETURN u.id as id, u.text as text, u.created_at as created_at, u.created_str as created_str, u.retweeted as retweeted, u.favorite_count as favorite_count, u.retweet_count as retweet_count"}]}' \
     http://52.3.253.48:37880/db/data/transaction/commit \
     | jq -r '(.results[0]) | .columns,.data[].row | map(if type == "string" then gsub("\n|\r"; "þ") else . end) | @csv' > dump/node_Tweet.csv
