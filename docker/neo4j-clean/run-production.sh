sudo docker stop $(sudo docker ps -q --filter ancestor=borisyartsev9taxify/neo4j-stuff:trolls-1 )
sudo docker run -d -p 7474:7474 -p 7687:7687 borisyartsev9taxify/neo4j-stuff:neo4j-clean-1
