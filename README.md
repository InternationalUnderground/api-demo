# GitHub API Demo

This is a simple Flask app that listens for webhooks and files an issue when an Organization's repository is deleted.

1. Listens for webhooks at /webhooks/
2. If the webhook describes a repository deletion it will create an issue in a designated repository.
3. Returns appopriate errors if the webhook does not validate.

## Installation and usage

This is a [Flask app](http://flask.pocoo.org/). You'll need a [Python3 environment](http://flask.pocoo.org/docs/1.0/installation/) to run this application. Once you have that follow the steps below.

1. Run `pip install -r requirements.txt` in the project's root directory.
2. [Create a personal access token](https://github.com/settings/tokens/new) for the GitHub API. Grant at least the `public_repo` scope.
3. Set your API key as an environment variable `GH_KEY`. On a UNIX-like system run `echo "export GH_KEY=<key>"" >> ~/.profile` where `<key>` is your access token.
4. [Create a webhook](https://github.com/organizations/InternationalUnderground/settings/hooks) for a GitHub Organization you own:
  * Set "Content type" to `application/json`
  * Set a Secret. Generate a long, random string and paste it in the "Secret" field. **Keep your secret safe and rotate it if it is ever exposed publicly.**
  * For "Which events would you like to trigger this webhook?": Select "Let me select individual events" and choose only "Repositories".
5. Set the same secret string as an environment variable named `GH_SECRET`.
6. Copy `settings.yml.sample` to `settings.yml` and fill in the values for each key.
  * `target_repo`, the repository that will receive the new issue
  * `notify_delete`, users to tag in new issues created when a repo is deleted
  * `notify_else` (optional), users to tag on other events.

### Serve the application locally

1. Install `ngrok` to forward local servers to a public web address.
2. Activate your python environment and run `gunicorn github-api-demo:app` and 
3. Start `ngrok` with `ngrok http 8000`.
4. Set the Payload URL for the Webhook to the `ngrok` address at the `/webhook/` endpoint.
5. Delete a repository in your organization and you will see a new issue in the repo you set as `target_repo`.
6. To check webhook delivery success or failure, go to this page: https://github.com/organizations/<org>/settings/hooks/ (replace `<org>` with your organization's name) and choose the webhook matching your `ngrok` address.

## Production deployment

This application can be deployed in any environment with Python installed at 3.6 or higher and a properly configured webserver. Below are instructions for deploying to Heroku.

### Things you'll need:

1. A Heroku account. ([Get one for free](https://signup.heroku.com/).)
2. The Heorku CLI installed on your computer.

### Setup the application

1. Create a Heroku app by running `heroku create`
2. Set environment variables for `GH_KEY` and `GH_SECRET` with `heroku config:set`, for example: `heroku config:set GH_KEY=<key>`. You can verify these by going to the settings page for your app on the Heroku dashboard.
3. Push the app to Heroku to initiailze a build: `git push heroku master`
4. Change the Paylod URL to your Heroku app at the `/webhook/` endpoint
5. Delete a repository in your organization and you will see a new issue in the repo you set as `target_repo`.

If you don't have another repository to delete, but still want to test the delivery and issue creation, you can resend a webhook you sent earlier. The app will create another issue.

## Troubleshooting

### 501: Not Implemented

The repository webhook will sent on any of the following actions: Create, delete, archive, unarchive, privatize, or publicize. Since we only have logic to handle `deleted` actions, we return 501 for the rest. 

Solution: Delete a repository to see status 200. This will also post a new issue to `target_repo`. Alternatively, re-send a webhook from a previous repository deletion.

### 403: Forbidden

This application sends status code 403 when the secret set in GitHub doesn't match the secret stored in your environment.

Solution: Change the "Secret" on the webhook to match what you set in the environment.

### 405: Method Not Allowed

This indicates the document sent to the `/webhook/` endpoint was not a `POST` request. It's unlikely you'll see this from a Webhook delivery. You may see it if you're attempting to use a tool like `curl` or Postman to test the app without sending webhooks.

Solution: Send a webhook from GitHub

### 415: Unsupported Media Type

The application expects the payload to have a `content-type` of `application/json`.

Solution: Go to your Webhook Settings and verify the Content type setting for your webhook is `application/json`.

### Other 4/5xx errors

Check your webhook settings. This application is written to only accept and process [Organization webhooks](https://developer.github.com/v3/orgs/hooks/) for [Repository Events](https://developer.github.com/v3/activity/events/types/#repositoryevent). If you're seeing 4xx errors, it's probably because the data sent by the webhook can't be processed.

These docs are written with Heroku in mind. But Flask apps can be deployed in [a wide variety of production environments](http://flask.pocoo.org/docs/1.0/deploying/#deployment), so if you can't or don't want to use Heroku, you may see other 400 or 500 errors as you work out the correct implementation details. Check your environment variables, settings.yml file, and your server logs. If you're using Heroku and seeing generic 500 errors, check with `heroku logs --tail`. Feel free to file an issue detailing the error for more support.

## Attribution

This application uses [Flask](http://flask.pocoo.com), the [PyGitHub project](https://pygithub.readthedocs.io/en/latest/introduction.html) available on PyPI, and the [Green Unicorn (`gunicorn`)](https://gunicorn.org/) WSGI server.

See [LICENSE](https://github.com/InternationalUnderground/api-demo/blob/master/LICENSE) for more information about these open source projects.