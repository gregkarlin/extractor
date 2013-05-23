from extractor import Extractor
from mail import sendMail
from threading import Thread
import time
#import sys

#sys.stdout = open('log.txt','w')
def extract():
  extractor = Extractor()
  extractor.extract()

def mail():
  sendMail()

if __name__ == '__main__':

  #while True:
    try:
      extract()
    except:
      print('extraction failed')
    sendMail()
    #time.sleep(500)
    #extract_thread = Thread(target=extract)
    #extract_thread.start()
    #print('Waiting 10 seconds')
    #time.sleep(10)
    #mail_thread = Thread(target=mail)
    #mail_thread.start()
    #print('Waiting 3600 seconds')
    #time.sleep(3600)
