import requests
from lxml import html
from .Worker_Task import Worker_Task
from twilio.rest import Client
from .headers import headers
import json
import time 

class UniversalMonitor:
  def __init__(self, task_id):
    self.task_id = task_id
    self.current_task = self.get_valid_task(task_id)
    if self.current_task == None:
      print('Not a valid Task')
      return
    elif self.current_task.is_valid_task() == False:
      print('No API Key, or missing values')
      return
    self.updated_xpath_value = None
    if self.current_task.should_send_sms:
      self.twilio_client, self.from_number, self.to_number = self.create_twilio_client()
    
  def create_twilio_client(self):
    with open('data/keys.json') as key_file: 
      data = json.loads(key_file.read()) 
      client = Client(data['twilio_account_sid'], data['twilio_auth_token'])
      return client, data['twilio_phone_number'], data['send_phone_number']
    return None, None, None

  def get_valid_task(self, task_id):
    with open('data/task.json') as key_file: 
      data = json.loads(key_file.read()) 
      for task in data['tasks']:
        current_task = Worker_Task(task['task_id'], task['url'], task['xpath_value'], task['should_send_sms'], task['check_delay'])
        if current_task.task_id == task_id:
          return current_task
    return None
  
  def find_by_xpath(self, element_source, xpath_expression):
    root = html.fromstring(element_source)
    return root.xpath(xpath_expression) 
  
  def send_text_message(self, newValue):
    message_body = "Task Id: %s - New Value: %s" % (self.task_id, newValue)
    message = self.twilio_client.messages.create(
      to="+1" + self.to_number, 
      from_="+1" + self.from_number,
      body=message_body
    )

  def start_task(self):
    print("Monitoring website for updates")
    while True:
      try:
        response = requests.get(self.current_task.url, headers = headers)
        xPathNode = self.find_by_xpath(response.text, self.current_task.xpath_value)
        if (len(xPathNode) != 0):
          xPathVal = xPathNode[0].text_content()
          if xPathVal != self.updated_xpath_value:
            self.updated_xpath_value = xPathVal
            self.send_text_message(xPathVal)
            print('Found New Value: ', xPathVal)
      except Exception as e:
        print('Error getting website: ', e)
      time.sleep(self.current_task.check_delay)    

