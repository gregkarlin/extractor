import smtplib
from db import conn,cur


fromaddr = 'gregory.l.karlin@gmail.com'
toaddrs  = 'rfusco@jouleassets.com'
#toaddrs  = 'gregory.l.karlin@gmail.com'


# Credentials (if needed)
username = 'gregory.l.karlin'
password = 'listeriusB2'



#Retrieve new message entries
def getNewMessages():
  cur.execute(''' SELECT time_stamp, message_type, message FROM emergency_message WHERE reviewed = FALSE; ''')
  messages = cur.fetchall()
  message_count = len(messages)
  if message_count == 0:
    return False
  message_string = '%s new emergency messages have been added to the database!\n\n----------------------------------------\n'%(str(message_count))
  for message in messages:
    message_string += '''message time: {0}\n message type: {1}\n message: {2}\n------------------------------------\n '''.format(*message)
  cur.execute(''' UPDATE emergency_message SET reviewed = TRUE; ''')
  conn.commit()
  cur.close()
  conn.close()
  return message_string

# The actual mail send  
def sendMail():
  message_string = getNewMessages()
  if message_string == False:
    message_string = 'There are no new messsages'
    print('No new messages')
  else:
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, message_string)
    server.quit()
    print('mail sent')
#sendMail()
