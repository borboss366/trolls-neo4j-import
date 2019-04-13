FROM neo4j:3.5.4
ENV NEO4J_AUTH=neo4j/12345

LABEL maintainer="Boris yartsev"

ENV APOC_VERSION 3.5.0.2
ENV APOC_URI https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/${APOC_VERSION}/apoc-${APOC_VERSION}-all.jar

ENV GRAPH_VERSION 3.5.4.0
ENV GRAPH_URI https://github.com/neo4j-contrib/neo4j-graph-algorithms/releases/download/${GRAPH_VERSION}/graph-algorithms-algo-${GRAPH_VERSION}.jar

RUN wget $APOC_URI && mv apoc-${APOC_VERSION}-all.jar plugins/apoc-${APOC_VERSION}-all.jar
RUN wget $GRAPH_URI && mv graph-algorithms-algo-${GRAPH_VERSION}.jar plugins/graph-algorithms-algo-${GRAPH_VERSION}.jar

COPY ./volumes/data/ ./data/

EXPOSE 7474 7473 7687

CMD ["neo4j"]