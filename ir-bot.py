from jira import JIRA
import os

#################################################################################
# JIRA ticket creation
#################################################################################
#jira_api=JIRA(CONFIG_OBJECT['jira_site_url'],basic_auth=(CONFIG_OBJECT['email'], CONFIG_OBJECT['apiToken']))
#Use it with #from config import CONFIG_OBJECT
# or just set env vars as I did for this test (this will be a slack bot, so secrets will be stored in AWS where the lambda running the code will be)
#email = os.environ.get('email')
#apiToken = os.environ.get('apiToken')

#Create the following env variables 
jira_api=JIRA(os.environ['jira_site_url'],basic_auth=(os.environ['email'], os.environ['apiToken']))
project_name = os.environ['project_name']

def create_issue ():
    ticket=jira_api.create_issue(project=project_name,
                        #summary="Fire - Everything's fine!",
                        #description= "This Issue has been created by the Incident Response Bot, following the orders of a Incident Responder",
                        summary='[Created by IR-bot] ' + summary_to_add,
                        description=description_to_add,
                        priority={'name': 'High'},
                        labels=['ongoing-inc'],
                        issuetype={'name': 'Task'})

#################################################################################
# Search the active incident issue
#######################
def active_inc ():
    active_inc_list = jira_api.search_issues('project={} and labels IN ("ongoing-inc")'.format(project_name))
    if len(active_inc_list) ==0:
        return "No active Inc"
    else:
        ongoing_inc_list=[]
        for index, active_inc in enumerate(active_inc_list):
            active_inc = str(active_inc)
            ongoing_inc_list.append(active_inc)
        return ongoing_inc_list

#################################################################################
# Update issue
#######################

def update_inc():
    current_inc = inc_to_update
    #current_inc = active_inc()
    #print(current_inc)
    jira_api.add_comment(current_inc, comment_to_add)

#################################################################################
# Close issue (or move it to not-ongoing and change label)
# 1. Change label to sth like "pending-close"
# 2. Gather all comments within the issue
# 3. Create a table with comments, who and timestamp (the who should be taken from the slack participant, not from the jira issue, as we will use a svc-account)
#################################################################################

def close_active_inc():
    current_inc = inc_to_close
    #current_inc = active_inc()
    issue = jira_api.issue(current_inc)
    issue.update(fields={"labels": ["pending-manual-close"]})
    comments =  issue.fields.comment.comments
    list_of_rows = ['||*Timestamp*||*Who*||*Action/Comment*||\n']
    for c in comments:
        timestamp = c.created
        who = c.author.displayName
        comment = c.body
        row = ('| {} | {} | {} |\n').format(timestamp,who,comment)
        list_of_rows.append(row)
        list_of_rows_to_str = ' '.join([str(elem) for elem in list_of_rows])
    jira_api.add_comment(current_inc, list_of_rows_to_str)

###############################################################################################################################################################
# As list_of_active_inc needs to be presented when option 3 and 4 is choosen (for updating/closing a specific incident), I'm creating a separate function to 
# reutilize this small code block
##########################################
def print_active_inc_as_elements():
    list=active_inc()
    for inc in list:
        print(inc)

print("Hello, I'm the very first attempt for an IR bot. Choose your action:")
print("1. Create an Incident")
print("2. Find ongoing Incident")
print("3. Update Incident - add comments")
print("4. Close")
choice = input ("1, 2, 3 or 4? ")
print (choice)
if choice == "1":
    summary_to_add = input("Enter Summary:")
    description_to_add = input("Enter Description:")
    create_issue()
    print("Incident Has been created!")
elif choice == "2":
    print_active_inc_as_elements()
elif choice == "3":
    print("Please select the active inc that you want to update from the following list: ")
    print_active_inc_as_elements()
    inc_to_update = input("INC:")
    comment_to_add = input("Enter comment to add: ")
    update_inc()
elif choice == "4":
    print("Please select the active inc that you want to close from the following list: ")
    print_active_inc_as_elements()
    inc_to_close = input("INC:")
    close_active_inc()
else:
    print('Im not that smart yet')





