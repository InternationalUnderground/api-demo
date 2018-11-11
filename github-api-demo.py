from flask import Flask, request, abort
from github import Github
from yaml import load, dump
import os
import hashlib
import hmac

app = Flask(__name__)

def get_config_var(key):
  config = os.environ.get(key)
  return str(config)

def get_yaml_var(key):
  stream = open('settings.yml', 'r')
  settings = load(stream.read())
  config_var = settings['github'][key]
  return config_var

def request_verify(request):
  if request.method != 'POST':
    abort(405)
  if request.content_type != 'application/json':
    abort(415)
  
def webhook_verify(request):
  signature = request.headers['X-Hub-Signature'].split('=')
  key = get_config_var('GH_SECRET')
  body = request.data
  hashed = hmac.new(key.encode('utf-8'), body, hashlib.sha1)
  digest = hashed.hexdigest()
  if hmac.compare_digest(signature[1], digest) != True:
    return abort(403)
  else:
    return True

def prepare_issue(repo):
  repo_name = repo['repository']['full_name']
  action = repo['action']
  notify_on_delete = get_yaml_var('notify_delete')
  issue_body = "Repository %s was %s! cc: %s" % (repo_name, action, notify_on_delete)
  return issue_body

api_key = get_config_var('GH_KEY')
g = Github(api_key)

@app.route("/webhook/", methods=['POST','GET'])
def post_comment_on_delete():
  request_verify(request)
  webhook_verify(request)
  hook = request.get_json(silent =True)
  if hook['action'] == 'deleted':
    issue_body = prepare_issue(hook)
    target_repo = g.get_repo(get_yaml_var('target_repo'))
    target_repo.create_issue(title='Repository deleted', body=issue_body)
    return str(issue_body[0])
  else:
    abort(501) # request is valid there's just nothing to do unless the action is `deleted`
