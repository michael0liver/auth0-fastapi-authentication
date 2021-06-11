# Auth0 + Python + FastAPI Example API

This project shows a minimal example of using Auth0 to secure a Python FastAPI application.

## Installation

In order to run the example you will need the following installed:

- [Python](https://www.python.org) - This project is configured for version **3.9**.
- [poetry](https://github.com/python-poetry/poetry) - For depdedency management.

Install depdndencies with poetry

```bash
poetry install
```

## Auth0 Setup

You will need to configure some stuff in Auth0 before proceeding.

### Create an API

In the [APIs](https://manage.auth0.com/#/apis) section of the Auth0 dashboard, click Create API. Provide a name and an identifier for your API. You will use the identifier as an audience later, when you are configuring environment variables. Leave the Signing Algorithm as RS256.

### Define permissions

You can define allowed permissions in the Permissions tab of the Auth0 Dashboard's APIs section.

Create the following permissions:

- `read:messages`
- `create:messages`

### Create an Application

In the [Applications](https://manage.auth0.com/#/applications) section of the Auth0 dashboard, click Create Application. Provide a name for your Application and select the Single Page Web Applications as the type.

Once your Application is created head to the Settings tab, take note of the Domain and Client ID fields as you will be using this later in environment variables.

Head to the Application URLs section.

Allowed Callback URLs:
`http://localhost:8000/docs/oauth2-redirect`

Head to the APIs tab and

## Environment Variables

To run this project, you will need to add the following environment variables to your `.env` file:

`APP_AUTH0_DOMAIN`

Your Auth0 domain.

For example: `APP_AUTH0_DOMAIN=example.auth0.com`

`APP_AUTH0_API_AUDIENCE`

The audience of your API.

For example: `APP_AUTH0_API_AUDIENCE=your-api-audience`

`APP_AUTH0_APPLICATION_CLIENT_ID`

The Client ID of your application, this is used by Swagger UI to perform the OAuth2 Flow.

For example: `APP_AUTH0_APPLICATION_CLIENT_ID=your-app-client-id`

## Run Locally

Clone the project

```bash
  git clone https://link-to-project
```

Go to the project directory

```bash
  cd my-project
```

## Scripts

Inspired by GitHub's [Scripts to Rule Them All](https://github.com/github/scripts-to-rule-them-all).

### scripts/develop

[`scripts/develop`](scripts/develop) is used to start the development server.

By default is starts the server on port **8000** with auto-reload enabled.

### scripts/format

[`scripts/format`](scripts/format) is used to auto format the code.

### scripts/install

[`scripts/install`](scripts/install) is used to install dependencies in a virtual environment.

### scripts/lint

[`scripts/lint`](scripts/lint) is used to run the code linting checks.
