CREATE VIEW new_messages AS 
  SELECT * FROM emergency_message WHERE reviewed != FALSE;
