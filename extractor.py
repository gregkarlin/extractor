import mechanize
import cookielib
from StringIO import StringIO
from lxml import etree
from db import conn, cur
import time

class Extractor:
  def __init__(self):
    self.base_url = 'https://emergproc.pjm.com'

  def setOptions(self):
    
    print('setting options')
    # Browser
    self.br = mechanize.Browser()

    # Cookie Jar
    self.cj = cookielib.LWPCookieJar()
    self.br.set_cookiejar(self.cj)

  
    # Browser options
    self.br.set_handle_equiv(True)
    self.br.set_handle_gzip(True)
    self.br.set_handle_redirect(True)
    self.br.set_handle_referer(True)
    self.br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # Want debugging messages?
    #br.set_debug_http(True)
    #br.set_debug_redirects(True)
    #br.set_debug_responses(True)

    # User-Agent (this is cheating, ok?)
    self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

  def login(self):  
    print('Attempting to Login at url: https://emergproc.pjm.com/epsql/ep_nav.login_proc?p_user=guest&p_password=guest&p_guest=1&p_link=1 ')
    #print('waiting 80 seconds')
    #time.sleep(80)
    self.login_url = self.br.open('https://emergproc.pjm.com/epsql/ep_nav.login_proc?p_user=guest&p_password=guest&p_guest=1&p_link=1')
    
  def getResponse(self):  
    print('Attempting to Get Reponse From: https://emergproc.pjm.com/epsql/ep_report.messages?p_apply=1&p_last2act=1&p_type=ALL&p_region=ALL&p_sort=Z')
    #print('Waiting 80 seconds')
    #time.sleep(80)
    self.response =  self.br.open('https://emergproc.pjm.com/epsql/ep_report.messages?p_apply=1&p_last2act=1&p_type=ALL&p_region=ALL&p_sort=Z')

  def parseResponse(self):
    #read response into html string
    self.html = self.response.read()
    
    self.parser = etree.HTMLParser()

    
    print('Parsing HTML response')
    self.parsed_tree = etree.parse(StringIO(self.html),self.parser)

  def getDownloadLink(self):
 
    self.route_link_text = self.parsed_tree.xpath('//div[@id="s_button_1"]/a')[1].values()[0]
    print('Finding Download Link')
    self.link_text = self.base_url + self.route_link_text
  
  def download(self):
    print('Attempting to download from %s' % (self.link_text))

    self.xml_string = self.br.open(self.link_text)

  def parseXML(self):
    print('parsing xml')
    self.xml_tree = etree.parse(self.xml_string) 
    self.root = self.xml_tree.getroot()
    
  def storeXML(self):
    print('Storing xml elements into a dictionary list')
    self.insert_dict_list = []
    messages = self.root.getchildren()
    for message in messages:
      message_elements = message.getchildren()
      insert_dict = {}
      for element in message_elements:
        try: escaped_quote_text = element.text.replace("'","''")
        except: escaped_quote_text = element.text
        insert_dict[element.tag] = escaped_quote_text
      self.insert_dict_list.append(insert_dict)
    
  def saveXML(self):
    print('Storing new xml elements into the database')
    for insert_dict in self.insert_dict_list:
      insert_string = ''' INSERT INTO emergency_message 
                                 (message_id,
                                  time_stamp,
                                  message_type,
                                  region_area,
                                  canceled_time_stamp,
                                  message) 
                          VALUES ('{messageId}',
                                  '{timestamp}',
                                  '{message_type}',
                                  '{regionArea}',
                                  '{canceledTimestamp}',
                                  '{message}'
                                 )  '''.format(**insert_dict)
      try:cur.execute(insert_string)
      except:print('duplicate entry')
    conn.commit()
    #cur.close()
    #conn.close()
  def extract(self):
    self.setOptions()
    self.login()
    self.getResponse()
    self.parseResponse()
    self.getDownloadLink()
    self.download()
    self.parseXML()
    self.storeXML()
    self.saveXML()

#extractor = Extractor()
#extractor.extract()
