// delete everything
MATCH (n) DETACH DELETE n

MATCH (u:User { screen_name: "TEN_GOP" }) RETURN u;

// the TEN_GOP tweets
// https://www.buzzfeednews.com/article/kevincollier/twitter-was-warned-repeatedly-about-this-fake-account-run#.javj266Xk
MATCH (u:User)-[:POSTED]->(t:Tweet)-[:HAS_TAG]->(h:Hashtag)
WHERE u.screen_name = "TEN_GOP"
OPTIONAL MATCH (t)-[:HAS_LINK]->(l:Link)
RETURN u, t, h, l

// Most popular hashtags
MATCH (u:User)-[:POSTED]->(t:Tweet)-[:HAS_TAG]->(ht:Hashtag)
RETURN ht.tag AS hashtag, COUNT(*) AS num
ORDER BY num DESC LIMIT 10

// Most tweets used together
MATCH (h1:Hashtag)<-[:HAS_TAG]-(t:Tweet)-[:HAS_TAG]->(h2:Hashtag)
WHERE id(h1) < id(h2)
RETURN h1.tag, h2.tag, COUNT(*) AS num ORDER BY num DESC LIMIT 15

// Most 
MATCH (t:Tweet)-[:HAS_LINK]->(u:URL)
WITH t, replace(replace(u.expanded_url, "http://", '' ), "https://", '') AS url
RETURN COUNT(t) AS num, head(split(url, "/")) ORDER BY num DESC LIMIT 10
                                   
// tags
MATCH (u: User {screen_name:"TEN_GOP"})-[:POSTED]-(t: Tweet)-[:HAS_TAG]->(ht: Hashtag {tag: "blacklivesmatter"}) RETURN *;
MATCH (u: User {screen_name:"LeroyLovesUSA"})-[:POSTED]-(t: Tweet)-[:HAS_TAG]->(ht: Hashtag {tag: "thanksobama"}) RETURN *;
                                                                          

                       
CALL algo.pageRank(
  "MATCH (t:Troll) RETURN id(t) AS id", 
  "MATCH (t: Troll)-[:POSTED]->(tw:Tweet)<-[:RETWEETED]-(tw2:Tweet)<-[:POSTED]-(t2: Troll) RETURN id(t2) AS source, id(t) AS target",
  {graph:'cypher'});
  
MATCH (n:Troll) RETURN n.screen_name, n.pagerank ORDER BY n.pagerank DESC LIMIT 25;
  
CALL algo.pageRank(
  "MATCH (t:User) RETURN id(t) AS id", 
  "MATCH (t: User)-[:POSTED]->(tw:Tweet)<-[:RETWEETED]-(tw2:Tweet)<-[:POSTED]-(t2: User) RETURN id(t2) AS source, id(t) AS target",
  {graph:'cypher'});
  
MATCH (n:User) RETURN n.screen_name, n.pagerank ORDER BY n.pagerank DESC LIMIT 25; 