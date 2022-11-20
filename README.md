# Junkie-Django-Api
A REST API developed using Django Rest Framework, which uses AWS Dynamodb as its schemaless database. We will add an Admin dashboard to interact with the API, as a superuser.
We use pynamodb, for its ORM, to write models and interface to Dynamodb database.


![GitHub](https://img.shields.io/github/license/JunkieLabs/junkie-django-api)
![](https://img.shields.io/badge/Python-3.7-red)
![](https://img.shields.io/badge/Django-3.2-green)
![](https://img.shields.io/badge/Database-Dynamodb-orange)
<!-- ![](https://img.shields.io/badge/Deployment-LambdaFunction-yellow) -->


<br>

# Index

- **[Installation Instructions](#installation-instructions)**<br>
- **[Setup Django RESTapi project](#setup-django-restapi-project)**<br>
   - **[Folder Structure](#folder-structure)**<br>
- **[Setup Dynamodb](#setup-dynamodb)**<br>  
- **[Deploying on Lambda-function](#deploying-on-lambda-function)**<br>
  - **[Setup AWS resources](#setup-aws-resources)**
  - **[Zappa Deployment](#zappa-deployment)**
- **[Further Help](#further-help)**<br>
- **[License](#license)**<br>

<br>

# Installation Instructions #

First setup your python virtual environment and activate it.

```ps
python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt
```



<br>

# Setup Django RESTapi project #

## Folder Structure

```
project
│   README.md
│   manage.py
|   .env.example
|   .env.local
│   .env.dev
│   .env.prod
│
└───junkie_django_api
   │   __init__.py
   │   asgi.py
   │   settings.py
   │   env.py
   |   urls.py
   │   wsgi.py
   └───apps
      |
      └───productionLine/     
      |
      └───products/   # django-app
      |
      └───contactUs/  # django-app
```
<br>

# Setup Multiple Environments

We have setup multiple environments.

In our present case as AWS provides downloadable version of dynamodb which can be used for development purposes on local machine. Which further elliminates the requirement of connecting to a cloud hosted database to test our backend bussiness logic.

So, we have setup an addditional environment called `local environment`, which uses AWS's downloadable Dynamodb server, installed and run on our local machine.

We have setup separate environments for locally run Dynamodb development environment(`.env.local`), cloud hosted Dynamodb development environment(`.env.dev`) and production environment(`.env.prod`).

<br>



1. Similarly `.env.prod` file.
   - Since, we are using Zappa to deploy our production ready code base, we wll fix many of the production environment variables inside the auto generated [zappa_settings.json](#todo)


Next import these environment variables inside django [`settings.py`](django_dynamodb_lambda_function\settings.py) file.

<br/>




# **Setup Dynamodb**
---

  You can download [AWS CLI](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Tools.CLI.html#Tools.CLI.DownloadingAndRunning) and configure your AWS credentials. Make sure to use different IAM roles for production environment and development environments, for security concerns.

```ps
> aws configure 
    AWS Access Key ID : "your-access-key-id"
    AWS SECRET ACCESS KEY : "your-secret-key"
```
<br>

- ## *Setup for Local machine*
>AWS provides downladable version of dynamodb, allowing a developer to experiment without any fear to mess something up. Use [this link](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html) to setup **[Dynamodb](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html)** on your local machine.

To start a **dynamodb server on your local machine**:

1. Put in following command in your powershell

```ps
> cd path\to\aws\dynamodb_local_latest

> java -D"java.library.path=./DynamoDBLocal_lib" -jar DynamoDBLocal.jar -dbPath path\to\write\database_file folder
```

By default the dynamodb-server runs at http://localhost:8000

To run the **django local environment**. Provide the relevant environment variable from console or run:
```ps
> $env:ENV = "local"
> python manage.py runserver 8080

or 
> python manage.py runserver 8080 --env local/dev/prod
```
<br/>

- ## *Setup for Dynamodb web service*
 Follow the instructions provided on [AWS website](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SettingUp.DynamoWebService.html).


or you can setup the variables to be fixed dynamically inside [**Zappa settings file**](zappa_settings_example.json).


<br />

## Using [**Pynamodb**](https://pynamodb.readthedocs.io/en/latest/index.html)
---

"PynamoDB is a Pythonic interface to Amazon’s DynamoDB. By using simple, yet powerful abstractions over the DynamoDB API..."

 If you are familiar with django's style of **ORM(Object Relational Mapper)** model, serialiser and class definition of views you can readily setup your RESTapi backend using [pynamodb API](https://pynamodb.readthedocs.io/en/latest/api.html).

<br />

# Deploying on Lambda-function
---
## Setup AWS resources
---
Setup AWS account and confgure IAM roles, policies and permission so as to allow zappa to manage AWS resources for your API deployment.

References:
1. [How to create a serverless service in 15 minutes](https://blog.lawrencemcdaniel.com/serve-a-django-app-from-an-aws-lambda-function/)
2. [Creating a role to delegate permissions to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html)

you can check the AWS resources required for zappa deployment inside [zappa_settings_example.json](zappa_settings_example.json) file

<br>

## Zappa Deployment
---
Finally we deploy our RESTApi using [Zappa](https://github.com/zappa/Zappa).

1. Pay per usage
2. Round the clock availability, Zero charges for hosting.
3. minimal initial manual setup required
4. Built-in logging system

<br>

Setup steps:

```ps
> zappa init # configure zappa_settings.json so generated to get access to AWS assets through separate IAMM role
> zappa deploy dev # for development server
> zappa deploy prod # for production environment
> zappa update <dev/prod> # to update changes in your code base
> zappa undeploy <dev/prod> # to remove the deployment
```


<br>

# Further Help

This project is an open-source initiative by Junkie Labs team.

For any questions or suggestions send a mail to junkielabs.dev@gmail.com or chat with the core-team on gitter.

<br>

[![Gitter](https://badges.gitter.im/nubar-api/Junkie-Django-Api.svg)](https://gitter.im/nubar-api/Junkie-Django-Api?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

<br>

# License

[MIT License](https://github.com/JunkieLabs/junkie-django-api/blob/main/LICENSE).


<br>

