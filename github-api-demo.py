from flask import Flask, request, abort
from github import Github
from yaml import load, dump
import os

app = Flask(__name__)

def get_yaml_setting(key):
  stream = open('settings.yml', 'r')
  settings = load(stream.read())
  return str(settings['github'][key])

def is_github_request(data, ua_string):
  if 'repository' and 'action' in data:
    if ua_string == get_yaml_setting('user_agent'):
      return True
  else:
    return False

def prepare_issue(repo):
  repo_name = repo['repository']['full_name']
  action = repo['action']
  issue_body = "Repository %s was %s!" % (repo_name, action)
  is_deleted = True if action == "deleted" else False
  return (issue_body, is_deleted)

api_key = get_yaml_setting('api_key')
g = Github(api_key)

@app.route("/")
def hello():
  return "Hello World"

@app.route("/webhook/", methods=['POST','GET'])
def post_comment_on_delete():
  if request.method == 'POST':
    if request.is_json:
      hook = request.get_json(silent =True)
      if is_github_request(hook, request.user_agent.string):
        issue_body = prepare_issue(hook)
      else:
        abort(403)
      if issue_body[1] == True:
        notify_on_delete = get_yaml_setting('notify_delete')
        target_repo = g.get_repo(get_yaml_setting('target_repo'))
        target_repo.create_issue(title='Repository deleted', body="%s cc:%s" % (issue_body[0], notify_on_delete))
        return str(issue_body[0])
      else:
        notify_else = get_yaml_setting('notify_else')
        return "%s cc: %s" % (issue_body[0], notify_else)
    else:
      return "Not a JSON object. Nothing to do!"
  else:
    return "Not a POST"
