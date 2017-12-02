# cookiecutter-django-herokuapp

A [cookiecutter](https://github.com/audreyr/cookiecutter) template for Django 1.10 / Python 3 only, that is *really* optimized for running on twelve-factor-app platforms (like Heroku or DigitalOcean).

[![Build status](https://travis-ci.org/dulacp/cookiecutter-django-herokuapp.svg?branch=master)](https://travis-ci.org/dulacp/cookiecutter-django-herokuapp?branch=master)


## Concept

I tried to be minimalistic, I mean no choice has been made concerning : 
- **the css library**, specify which one you want in the bower.json file
- **external django apps**, I don't see the point to choose this for you ;)

In fact the only choice made here is deploying on a [Twelve-Factor App Platform](http://12factor.net/).


## Requirements

This cookiecutter template uses features that exists only in cookiecutter 0.9.0 or higher.


## Features
---------

- Python 3 only, sorry guys but I had to move on...
- For [Django 1.10](https://docs.djangoproject.com/en/1.10/)
- Heroku optimized stack
- Gulp tasks to build the static files and support livereload
- Static served by `whitenoise` from the django app (advice to setup a cache instance above like CloudFlare)
- Instructions on how to configure the Amazon S3 bucket
- Instructions on how to deploy the app in less than 5 minutes


## Q&A

#### Why using `waitress` as the production server
> Gunicorn is actually designed to be used behing a buffering reverse proxy (e.g. nginx). In other words, without this buffering reverse proxy you expose your production server to a *slow network* attacks. If you want to dig on this particular topic, read the great article of @etianen *[Don't use Gunicorn to host your Django sites on Heroku](http://blog.etianen.com/blog/2014/01/19/gunicorn-heroku-django/)*


## Usage

First, get cookiecutter.

```sh
$ pip install cookiecutter
```

Now run it against this repo.

```sh
$ cookiecutter https://github.com/dulacp/cookiecutter-django-herokuapp.git
```

You'll be prompted for some questions, answer them, then it will create a Django project for you.


## Static handling

### Live reloading and Sass CSS compilation

You can take advantage of live reloading and Sass / Compass CSS compilation with the included Gulp tasks.

Make sure that [nodejs](http://nodejs.org/download/) is installed. Then in the project root run :

```sh
$ npm install
```

Now you just need :

```sh
$ gulp launch
```

Now your turn !
