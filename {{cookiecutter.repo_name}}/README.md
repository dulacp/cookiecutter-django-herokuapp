# {{ cookiecutter.project_name }}

> Don't hesitate to put a little quote from an unknown person here.

{{ cookiecutter.description }}


## Infos utiles

- Version Python : 3.4.x
- Version Django : 1.9.x


## Local install

First create the virtualenv with the right python version

```sh
$ mkvirtualenv {{ cookiecutter.repo_name }} --python=$(which python3)
$ workon {{ cookiecutter.repo_name }}
```

Install the dependencies

```sh
$ pip install -r reqs/dev.txt
$ npm install
```

Create the local database

```sh
$ createdb {{ cookiecutter.repo_name }}
$ ./manage.py migrate
```

Now you just need to launch the watcher for the style files, and it will run the django dev server too :

```sh
$ gulp launch
```

> If you want a specific port, you can use the `--port` option : `$ gulp launch --port 8005`


## Deploy the beast

### Prepare the static server

#### create a new user

```sh
$ aws iam create-user --user-name {{ cookiecutter.aws_s3_user_name }}
```

**output**
```json
{
    "User": {
        "UserName": "{{ cookiecutter.aws_s3_user_name }}", 
        "Path": "/", 
        "CreateDate": "2015-01-22T14:10:08.058Z", 
        "UserId": "<user_id>", 
        "Arn": "arn:aws:iam::<user_arn_id>:user/{{ cookiecutter.aws_s3_user_name }}"
    }
}
```

#### give the user some access keys

```sh
$ aws iam create-access-key --user-name {{ cookiecutter.aws_s3_user_name }}
```

**output**
```json
{
    "AccessKey": {
        "UserName": "{{ cookiecutter.aws_s3_user_name }}", 
        "Status": "Active", 
        "CreateDate": "2015-01-22T14:18:56.237Z", 
        "SecretAccessKey": "<secret_key>", 
        "AccessKeyId": "<access_key>"
    }
}
```

Write down the `<secret_key>` and `<access_key>` values, so that we can give the values to the heroku app.

#### create the aws bucket

```sh
$ aws s3 mb s3://{{ cookiecutter.aws_s3_bucket_name }} --region eu-west-1
```

#### give the bucket content public read

```sh
$ aws s3api put-bucket-policy --bucket {{ cookiecutter.aws_s3_bucket_name }} --policy '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowPublicRead",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": "s3:GetObject",
            "Resource": [
                "arn:aws:s3:::{{ cookiecutter.aws_s3_bucket_name }}/media/*",
                "arn:aws:s3:::{{ cookiecutter.aws_s3_bucket_name }}/static/*"
            ]
        }
    ]
}'
```

#### give the user access to the created bucket

```sh
$ aws iam put-user-policy --user-name {{ cookiecutter.aws_s3_user_name }} --policy-name AmazonS3FullAccess-{{ cookiecutter.aws_s3_user_name }} --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetBucketLocation",
                "s3:ListBucketMultipartUploads"
            ],
            "Resource": "arn:aws:s3:::{{ cookiecutter.aws_s3_bucket_name }}",
            "Condition": {}
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:AbortMultipartUpload",
                "s3:DeleteObject",
                "s3:DeleteObjectVersion",
                "s3:GetObject",
                "s3:GetObjectAcl",
                "s3:GetObjectVersion",
                "s3:GetObjectVersionAcl",
                "s3:PutObject",
                "s3:PutObjectAcl",
                "s3:PutObjectAclVersion"
            ],
            "Resource": "arn:aws:s3:::{{ cookiecutter.aws_s3_bucket_name }}/*",
            "Condition": {}
        }
    ]
}'
```


### Deploy the app

> We need to specify the buildpack to use otherwise heroku won't know which one to choose, due to the fact that both `package.json` and `requirements.txt` files exist.

Lancer les commandes dans l'ordre ci-dessous:

```sh
$ git init
$ heroku create --region eu {{ cookiecutter.heroku_app_name }}
$ heroku config:add BUILDPACK_URL=git://github.com/heroku/heroku-buildpack-python.git
$ heroku addons:create heroku-postgresql:hobby-dev
$ heroku addons:create newrelic:wayne
$ heroku config:set DJANGO_SETTINGS_MODULE="{{ cookiecutter.repo_name }}.settings.prod"
$ heroku config:set SECRET_KEY=`openssl rand -base64 32`
$ heroku config:set LOCAL_SERVER=0
$ heroku config:set AWS_STORAGE_BUCKET_NAME={{ cookiecutter.aws_s3_bucket_name }} AWS_S3_ACCESS_KEY_ID="<access_key>" AWS_S3_SECRET_ACCESS_KEY="<secret_key>"
$ git push heroku master
$ heroku run python manage.py migrate
$ heroku run python manage.py createsuperuser
$ heroku open
```

And you're done !


## Cheatsheet

I've defined some shortcuts in the `Makefile`, feel free to explore those or add yours.

_**d**eploy to **p**roduction_
```sh
$ make dp
```

_**d**eploy & **m**igrate to **p**roduction_
```sh
$ make dmp
```

_**c**ollectstatic to **p**roduction_
```sh
$ make cp
```


## Contact

[Pierre Dulac](http://github.com/dulaccc)  
[@dulaccc](https://twitter.com/dulaccc)
