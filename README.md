
# Universal Monitor


## What is the Universal Monitor

This project was created because I like keeping up to date with news and events that come out without needing to have multiple tabs open or constantly having to refresh. This program takes in a Url, an xPath value and Twilio API data to create a central program to monitor updates. Some use cases could be official city news, school updates, price changes, or changes in schedules. 

### Install and run
```bash
$ git clone https://github.com/MarwanKabir/Universal-Monitor.git
$ cd clone Universal-Monitor
$ python -m venv monitor_env
$ source monitor_env/bin/activate
$ pip install -r requirements.txt
```

In the data folder, add in your Twilio Auth, SID, phone number, and the phone number it should be sent to. 

Commands
 - create task_id url xpath_value should_send_sms, check_delay
	 - Creates a task
 - run task_id
	 - runs a task
 - delete task_id
	 - Deletes a task
 -  list
	 - lists all the tasks

task_id -> name of tasks
url -> url that should be checked
xpath_value -> xpath of what you want to check
should_send_sms -> true or false if you want to be sent texts
check_delay -> how often should checks happen

### Example News Monitor
Monitor any important updates from the state

```bash
$ python app.py create stateNewsMonitor https://coronavirus.health.ny.gov/home "/html/body/div[3]/div/main/div/div/div[3]/div/div/div[1]/div/div[1]" true 3
$ python app.py run stateNewsMonitor
```

This checks the website every 3 seconds and checks when the "Last Updated" time was to see if there is anything new.

### Results
![picture](https://i.imgur.com/frgIR0e.png)
![enter image description here](https://i.imgur.com/Mux1q2j.png)

### Example Time Monitor
Monitor any important updates from the state

```bash
$ python app.py create time_website_monitor https://time.is/ "/html/body[@id='bdy']/div[@id='mainwrapper']/div[@id='time_section']/div[2]/div[@id='clock0_bg']" true 3
$ python app.py run time_website_monitor
```

This checks the website every 3 seconds and updates if the time changes. This is a very simple example but this is to demonstrate websites that change frequently.

![enter image description here](https://i.imgur.com/adphb29.png)
![enter image description here](https://i.imgur.com/fW2sGf8.png)

	
### How it's made


## UniversalWorker

The UniversalWorker is responsible for running tasks. It will navigate to the specific website of a task and continuously check for updates. If it finds a new update it will send a SMS if that feature is enabled.

## WorkerTask

This is used to store Task specific information such as website, xpath value, SMS configurations and how often the task to update. It also has a method to check if there is a wrong configuration like wanting to send a SMS text without a API key.

**Note:** This does not work if the website requires JavaScript to load what you are looking for updates on. Use a xPath addon to find xpaths.
