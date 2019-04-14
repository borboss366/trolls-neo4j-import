## Docker setup ##

Pulls docker image 
```sh
sudo docker pull borisyartsev9taxify/neo4j-stuff:neo4j-clean-1
```

Launches clean docker image with neo4j for import testing
```sh
sudo docker run -d -p 7474:7474 -p 7687:7687 borisyartsev9taxify/neo4j-stuff:neo4j-clean-1
```

```sh
sudo docker pull borisyartsev9taxify/neo4j-stuff:trolls-1
```

Launches docker image with trolls database
```sh
sudo docker run -d -p 7474:7474 -p 7687:7687 borisyartsev9taxify/neo4j-stuff:trolls-1
```
