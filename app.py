from worker.UniversalMonitor import UniversalMonitor
import json
import sys

def add_task(task_id, url, xpath_value, should_send_sms, check_delay):
  task_json = {
    'task_id' : task_id,
    'url' : url,
    'xpath_value' : xpath_value,
    'should_send_sms' : should_send_sms,
    'check_delay' : check_delay,
  }
  with open('data/task.json', 'r') as task_file: 
    data = json.loads(task_file.read())
  data['tasks'].append(task_json)  
  with open('data/task.json', 'w') as out_file:
    json.dump(data, out_file)
  print('Added Task: ', task_id)

def delete_task(task_id):
  with open('data/task.json', 'r') as task_file: 
    data = json.loads(task_file.read())
  keep_tasks = []
  for task in data['tasks']:
    if task['task_id'] != task_id:
      keep_tasks.append(task)
  data['tasks'] = keep_tasks
  with open('data/task.json', 'w') as out_file:
    json.dump(data, out_file) 
  print('Deleted Task: ', task_id)

def list_all_tasks():
  with open('data/task.json', 'r') as task_file: 
    data = json.loads(task_file.read())
  for task in data['tasks']:
    print("-------------------------------------------------------------------")
    print("Name: %s \n Url: %s \n Xpath: %s \n Delay: %s \n Send Sms: %s \n" % (task['task_id'], task['url'], task['xpath_value'], task['check_delay'], task['should_send_sms']))

if __name__ == "__main__":
  try:  
    command = sys.argv[1]
    if command == "create":
      task_id, url, xpath_value, should_send_sms, check_delay = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]
      should_send_sms = should_send_sms.lower() == 'true'
      check_delay = int(check_delay)
      add_task(task_id, url, xpath_value, should_send_sms, check_delay)
    elif command == "run":
      task_id = sys.argv[2]
      runner = UniversalMonitor(task_id)
      runner.start_task()
    elif command == "delete":
      task_id = sys.argv[2]
      delete_task(task_id)
    elif command == "list":
      list_all_tasks()
  except Exception as e:
    print("Something went wrong: ", e)
