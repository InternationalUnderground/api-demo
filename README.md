# GitHub API Demo

This is a simple Flask app showing how to use a few different methods in the GitHub API. It does the following:

1. Listens for webhooks at /webhooks/
2. For repository actions, returns a string like `"Repository %s was %s!" % (repo, action)` in the response body. The variable `repo` is the name of the repository passed by the webhook and `action` is one of possible actions in a [Repository Event hook](https://developer.github.com/v3/activity/events/types/#repositoryevent).
3. If `action` is `deleted` it will create an issue in a designated repository.
4. If the incomming request does not contain a JSON file, or not a POST request, a message will be sent with the response.

## Installation and usage

This is a Flask app written in Python 3.6.4. You'll need a python environment with `pip` installed to work with this repository. Once you have that follow the steps below.

1. Run `pip install -r requirements.txt` (or `pip3` depending on your installation).
2. Create a personal API key
2. Copy `settings.yml.sample` to `settings.yml` and fill in the values for each key.
2. Run `gunicorn github-api-demo:app` and go to `127.0.0.1:8000` in a web browser where you should see "Hello World."
3. Create a webhook in a GitHub Organization:
  * You can use [ngrok](https://ngrok.io) to get a public url to use for testing webhook delivery. Use the `ngrok` URL with the `/webhooks/` endpoint for the Payload URL.
  * Select the "Let me select individual events" option and choose only "Repositories". 
4. Create, delete, archive, unarchive, privatize, or publicize a repository in your organization.
5. Check webhook delivery was successful by going to this page: https://github.com/organizations/<org>/settings/hooks/ (replace <org> with your organization's name) and choosing the webhook you created in step 3.

## Todo

* Offload configuration to a settings file not committed to version control

  *[x] Create settings.yml file
  *[x] GitHub API Key read from yml
  *[x] GitHub-Hookshot user agent read from yml
  *[x] Comment target repository read from yml
  *[x] Users to notify read from yml

* Enable production [deployment on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python)

  *[x] `gunicorn` installed
  *[ ] Deploy to Heroku
  *[ ] Document Heroku deployment
