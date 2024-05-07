# incident-response_bot
First attempt of an Incident response bot that Automatically creates and manages jira inc.

## Prerequisites
1. Create an Atlassian account, create a jira project and an API token

## How to use it
1. Clone this repo
2. Create a python 3 Virtual environment:

```
virtualenv -p python3 ir_bot
```

3. Install requirements.txt (jira)

```
pip install -r requirements.txt
```

4. Define the following 3 environmental variables

```
export project_name='{project_name_here}'
export apiToken=''
export jira_site_url='https://{insert_your_project_name_here}.atlassian.net'
```

5. Run it

```
python ir-bot.py
```

## To-Do
- [ ] Make it a Slackbot
- [ ] Run Bandit to scan the code
- [ ] Add Demo
- [ ] Dockerize it
