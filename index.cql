CREATE INDEX ON :Tweet(text);
CREATE INDEX ON :User(id);
CREATE CONSTRAINT ON ( hashtag:Hashtag ) ASSERT hashtag.tag IS UNIQUE;
CREATE CONSTRAINT ON ( source:Source ) ASSERT source.name IS UNIQUE;
CREATE CONSTRAINT ON ( tweet:Tweet ) ASSERT tweet.id IS UNIQUE;
CREATE CONSTRAINT ON ( url:URL ) ASSERT url.expanded_url IS UNIQUE;
CREATE CONSTRAINT ON ( user:User ) ASSERT user.user_key IS UNIQUE;