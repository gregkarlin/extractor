DROP TABLE IF EXISTS emergency_message cascade;

CREATE TABLE emergency_message
(
  message_id                                INTEGER PRIMARY KEY,
  time_stamp                                VARCHAR(200),
  message_type                              VARCHAR(100),
  region_area                               VARCHAR(100),
  canceled_time_stamp                       VARCHAR(200),
  message                                   TEXT,
  reviewed                                  BOOLEAN DEFAULT FALSE
);
