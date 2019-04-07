CONSTRAINT ON ( hashtag:Hashtag ) ASSERT hashtag.tag IS UNIQUE;
CONSTRAINT ON ( source:Source ) ASSERT source.name IS UNIQUE;
CONSTRAINT ON ( tweet:Tweet ) ASSERT tweet.id IS UNIQUE;
CONSTRAINT ON ( url:URL ) ASSERT url.expanded_url IS UNIQUE;
CONSTRAINT ON ( user:User ) ASSERT user.user_key IS UNIQUE;