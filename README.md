# Trolls archive #

## Info ##
Uses scripts from this article
https://www.lyonwj.com/2017/11/12/scraping-russian-twitter-trolls-python-neo4j/

## Docker ##

### Clean docker neo4j image ###
Pulls docker image with clean neo4j instance with additional procedures
```sh
sudo docker pull borisyartsev9taxify/neo4j-stuff:neo4j-clean-1
```
Launches clean docker image with neo4j for import testing
```sh

sudo docker run -d -p 7474:7474 -p 7687:7687 borisyartsev9taxify/neo4j-stuff:neo4j-clean-1
```

### Docker image with russian trolls database ###
Pulls docker image with russian trolls archive
```sh
sudo docker pull borisyartsev9taxify/neo4j-stuff:trolls-1
```

Launches docker image with trolls database
```sh
sudo docker run -d -p 7474:7474 -p 7687:7687 borisyartsev9taxify/neo4j-stuff:trolls-1
```

# Accessing # 
This link opens the web interface for the database
[http://localhost:7474](http://localhost:7474 "Graph data set")
