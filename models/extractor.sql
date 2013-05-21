CREATE TABLE extraction_method
(
  id                                        SERIAL PRIMARY KEY,
  name                                      VARCHAR(16),
  tested                                    BOOLEAN,
  verified                                  BOOLEAN
);


CREATE TABLE extractor
(
  id                                        SERIAL PRIMARY KEY,
  name                                      VARCHAR(80),
  description                               TEXT,
  base_url                                  VARCHAR(360),
  extraction_method                         INTEGER REFERENCES extraction_method(id)
);
