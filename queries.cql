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

// fraud tweets
MATCH (t:Troll)-[:POSTED]->(tw:Tweet)
WHERE tw.text CONTAINS "fraud"
OPTIONAL MATCH p=(tw)-[:HAS_TAG|HAS_LINK|MENTIONS|IN_REPLY_TO]-(a)
RETURN * LIMIT 50

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

MATCH (t:Troll) WHERE EXISTS(t.pagerank)
WITH t ORDER BY t.pagerank LIMIT 25
MATCH (t)-[:POSTED]->(tw:Tweet)-[:HAS_TAG]-(ht:Hashtag)
RETURN ht.tag, COUNT(tw) AS num ORDER BY num DESC LIMIT 25

// label propagation
CALL algo.labelPropagation("MATCH (t:Troll) RETURN id(t) AS id","MATCH (r1:Troll)-[:POSTED]->(t:Tweet)<-[:RETWEETED]-(:Tweet)<-[:POSTED]-(r2:Troll) RETURN id(r2) AS source, id(r1) AS target, COUNT(t) AS weight","OUTGOING",   
    {graph:'cypher', write: true, iterations: 200})

MATCH (t:Troll) WHERE EXISTS(t.partition)
RETURN COLLECT(t.screen_name) AS members, t.partition AS community
ORDER BY SIZE(members) DESC LIMIT 10

MATCH (t:Troll) WHERE EXISTS(t.partition)
WITH COLLECT(t) AS members, t.partition AS community
ORDER BY SIZE(members) DESC LIMIT 10
UNWIND members AS t
MATCH (t)-[:POSTED]->(tw:Tweet)-[:HAS_TAG]->(ht:Hashtag)
WITH community, ht.tag AS tag, COUNT(tw) AS num ORDER BY num DESC
RETURN community, COLLECT(tag)[..10] AS toptags
LIMIT 10