# GitHub API Demo

This is a simple Flask app showing how to use a few different methods in the GitHub API. It does the following:

1. Listens for webhooks at /webhooks/
2. For repository actions, returns a string like `"Repository %s was %s!" % (repo, action)` in the response body. The variable `repo` is the name of the repository passed by the webhook and `action` is one of possible actions in a [Repository Event hook](https://developer.github.com/v3/activity/events/types/#repositoryevent).
3. If `action` is `deleted` it will create an issue in a designated repository.
4. If the incomming request does not contain a JSON file, or not a POST request, a message will be sent with the response.

## Installation and usage

This is a Flask app written in Python 3.6.4. You'll need a python environment with `pip` installed to work with this repository. Once you have that follow the steps below.

1. Run `pip install -r requirements.txt` (or `pip3` depending on your installation).
2. [Create a personal access token](https://github.com/settings/tokens/new) for the GitHub API. Grant at least the `public_repo` scope. 
3. Set your API key as an environment variable `GH_KEY`. On a UNIX-like system run `echo "export GH_KEY=<key>"" >> ~/.profile` where `<key>` is your access token.
3. [Create a webhook](https://github.com/organizations/InternationalUnderground/settings/hooks) for a GitHub Organization you own:
  * Set "Content type" to `application/json`
  * Set a Secret. Generate a random string or use a password generator and paste it in the "Secret" field. **Keep your secret safe and rotate it if it is ever exposed publicly.**
  * For "Which events would you like to trigger this webhook?": Select "Let me select individual events" and choose only "Repositories".
4. Set the secret as an environment variable `GH_SECRET`.
2. Copy `settings.yml.sample` to `settings.yml` and fill in the values for each key.
  * `target_repo`, the repository that will receive the new issue
  * `notify_delete`, users to tag in new issues created when a repo is deleted
  * `notify_else` (optional), users to tag on other events.

### Serve the application locally

1. Install `ngrok` to forward local servers to a public web address.
2. Activate your python environment and run `gunicorn github-api-demo:app` and 
3. Go to `127.0.0.1:8000` in a web browser where you should see "Hello World."
4. Start `ngrok` with `ngrok http 8000`.
3. Set the Payload URL for the Webhook to the `ngrok` address at the `/webhook/` endpoint.
4. Create, delete, archive, unarchive, privatize, or publicize a repository in your organization. The app will return `200` for all webhooks.
5. Delete a repository in your organization and you will see a new issue in the repo you set as `target_repo`.
5. Check webhook delivery was successful by going to this page: https://github.com/organizations/<org>/settings/hooks/ (replace <org> with your organization's name) and choosing the webhook you created in step 3.

## Production deployment

This application can be deployed in any environment with Python installed at 3.6 or higher and a properly configured webserver. Below are instructions for deploying to Heroku.

### Things you'll need:

1. A Heroku account. ([Get one for free](https://signup.heroku.com/).)
2. The Heorku CLI installed on your computer.

### Setup the application

1. Create a Heroku app by running `heroku create`
2. Set environment variables for `GH_KEY` and `GH_SECRET` with `heroku config:set`, for example: `heroku config:set GH_KEY=<key>`. You can verify these by going to the settings page for your app on the Heroku dashboard.
2. Push the app to Heroku to initiailze a build: `git push heroku master`
3. Change the Paylod URL to your Heroku app at the `/webhook/` endpoint
4. Create, delete, archive, unarchive, privatize, or publicize a repository in your organization. The Heroku app will return `200` for all webhooks.
5. Delete a repository in your organization and you will see a new issue in the repo you set as `target_repo`.

If you don't have another repository to delete, but still want to test the delivery and issue creation, you can resend a webhook you sent earlier. The app will create another issue.

## Troubleshooting

### 403: Forbidden Errors

This application sends status code 403 when the secret set in GitHub doesn't match the secret stored in your environment.

Solution: Change the "Secret" on the webhook to match what you set in the environment.

### 405: Method Not Allowed

This indicates the document sent to the `/webhook/` endpoint was not a `POST` request. It's unlikely you'll see this from a Webhook delivery. You may see it if you're attempting to use a tool like `curl` or Postman to test the app without sending webhooks.

Solution: Send a webhook from GitHub

### 415: Unsupported Media Type

The application expects the payload to have a `content-type` of `application/json`.

Solution: Go to your Webhook Settings and verify the Content type setting for your webhook is `application/json`.