
import json

class Worker_Task:
  def __init__(self, task_id, url, xpath_value, should_send_sms, check_delay):
    self.task_id = task_id
    self.url = url
    self.xpath_value = xpath_value
    self.should_send_sms = should_send_sms
    self.check_delay = check_delay

  def is_valid_task(self):
    with open('data/keys.json') as key_file: 
      data = json.loads(key_file.read()) 
      if (self.should_send_sms == True and (data['twilio_account_sid'] != None and data['twilio_auth_token'] != None and data['twilio_phone_number'] != None and data['send_phone_number'] != None)):
        return True 
      elif self.should_send_sms == False:
        return True
      else:
        return False
    return False
         

    




