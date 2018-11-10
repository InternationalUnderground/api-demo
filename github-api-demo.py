from flask import Flask, request, abort
from github import Github
from yaml import load, dump
import os
import hashlib
import hmac

app = Flask(__name__)

def get_config_var(key):
  config_var = os.environ.get(key)

def get_yaml_var():
  stream = open('settings.yml', 'r')
  settings = load(stream.read())
  config_var = settings[key]
  return config_var

def is_github_request(request):
  signature = request.headers['X-Hub-Signature'].split('=')
  key = get_config_var('GH_SECRET')
  body = request.data
  hashed = hmac.new(key.encode('utf-8'), body, hashlib.sha1)
  digest = hashed.hexdigest()
  if hmac.compare_digest(signature[1], digest):
    return True
  else:
    return abort(403)

def prepare_issue(repo):
  repo_name = repo['repository']['full_name']
  action = repo['action']
  issue_body = "Repository %s was %s!" % (repo_name, action)
  is_deleted = True if action == "deleted" else False
  return (issue_body, is_deleted)

api_key = get_config_var('GH_KEY')
g = Github(api_key)

@app.route("/")
def hello():
  return "Hello World"

@app.route("/webhook/", methods=['POST','GET'])
def post_comment_on_delete():
  if request.method == 'POST':
    if request.is_json:
      hook = request.get_json(silent =True)
      if is_github_request(request):
        issue_body = prepare_issue(hook)
      else:
        abort(403)
      if issue_body[1] == True:
        notify_on_delete = get_yaml_var('notify_delete')
        target_repo = g.get_repo(get_yaml_var('target_repo'))
        target_repo.create_issue(title='Repository deleted', body="%s cc:%s" % (issue_body[0], notify_on_delete))
        return str(issue_body[0])
      else:
        notify_else = get_yaml_var('notify_else')
        return "%s cc: %s" % (issue_body[0], notify_else)
    else:
      return "Not a JSON object. Nothing to do!"
  else:
    return "Not a POST"
