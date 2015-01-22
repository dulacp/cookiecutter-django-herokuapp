# cookiecutter-django-herokuapp

A [cookiecutter](https://github.com/audreyr/cookiecutter) template for Django that is *really* optimized for running on Heroku.

[[https://travis-ci.org/dulaccc/cookiecutter-django-herokuapp.svg?branch=master]](https://travis-ci.org/dulaccc/cookiecutter-django-herokuapp?branch=master)


## Concept

It tries to be minimalistic, I mean no choice are made for you concerning : 
- **the css library**, specify which one you want in the bower.json file
- **external django apps**, I don't see the point to choose for you ;)

In fact the only choice made here is deploying on Heroku, well in fact deploying on a [Twelve-Factor App Plateform](http://12factor.net/).


## Requirements

This cookiecutter template uses features that exists only in cookiecutter 0.9.0 or higher.


## Features
---------

- Python 3 only, sorry guys but I had to move on...
- For [Django 1.7](https://docs.djangoproject.com/en/1.7/)
- Procfile for deploying to Heroku
- Heroku optimized server
- Basic caching setup
- Gulp tasks to build the static files and support livereload
- Static served by an Amanzon S3 instance
- Sentry preconfigured for reporting issues (see the [sentry section](#how-to-use-a-cheap-sentry-instance) on how to setup your own instance)


## Q&A

#### Why using `waitress` as the production server
> Gunicorn is actually designed to be used behing a buffering reverse proxy (e.g. nginx). In other words, without this buffering reverse proxy you expose your production server to a *slow network* attacks. If you want to dig on this particular topic, read the great article of @etianen *[Don't use Gunicorn to host your Django sites on Heroku](http://blog.etianen.com/blog/2014/01/19/gunicorn-heroku-django/)*

#### How to use a cheap sentry instance
> Deploy yours ! Check out the [sentry](https://github.com/dulaccc/sentry) project and you'll get in less than 10 minutes a private instance of the Sentry exception logger server.


## Usage

First, get cookiecutter.

```sh
$ pip install cookiecutter
```

Now run it against this repo.

```sh
$ cookiecutter https://github.com/dulaccc/cookiecutter-django-herokuapp.git
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
