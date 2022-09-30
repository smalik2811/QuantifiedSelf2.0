# Local Setup
- Clone the project
- Run `setup.sh`

# Local Development Run
- `local_run.sh` It will start the flask app in `development`. Suited for local development

# Folder Structure

- `db_directory` has the sqlite DB.
- `application` is where our application code is
- `.gitignore` - ignore file
- `setup.sh` set up the virtualenv inside a local `.env` folder. Uses `pyproject.toml` and `poetry` to setup the project
- `local_run.sh`  Used to run the flask application in development mode
- `static` - default `static` files folder. It serves at '/static' path. More about it is [here](https://flask.palletsprojects.com/en/2.0.x/tutorial/static/).
- `static/bootstrap` We have already added the bootstrap files so it can be used
- `static/style.css` Custom CSS. You can edit it. Its empty currently
- `templates` - Default flask templates folder


```
├── api.yaml
├── application
│   ├── config.py
│   ├── controllers.py
│   ├── database.py
│   ├── __init__.py
│   ├── models.py
│   ├── __pycache__
│   │   ├── api.cpython-310.pyc
│   │   ├── api.cpython-38.pyc
│   │   ├── api.cpython-39.pyc
│   │   ├── config.cpython-310.pyc
│   │   ├── config.cpython-38.pyc
│   │   ├── config.cpython-39.pyc
│   │   ├── controllers.cpython-310.pyc
│   │   ├── controllers.cpython-38.pyc
│   │   ├── controllers.cpython-39.pyc
│   │   ├── database.cpython-310.pyc
│   │   ├── database.cpython-38.pyc
│   │   ├── database.cpython-39.pyc
│   │   ├── functions.cpython-310.pyc
│   │   ├── __init__.cpython-310.pyc
│   │   ├── __init__.cpython-38.pyc
│   │   ├── __init__.cpython-39.pyc
│   │   ├── models.cpython-310.pyc
│   │   ├── models.cpython-38.pyc
│   │   ├── models.cpython-39.pyc
│   │   ├── tasks.cpython-310.pyc
│   │   ├── tasks.cpython-38.pyc
│   │   ├── validation.cpython-310.pyc
│   │   ├── validation.cpython-38.pyc
│   │   ├── validation.cpython-39.pyc
│   │   ├── workers.cpython-310.pyc
│   │   └── workers.cpython-38.pyc
│   ├── tasks.py
│   ├── validation.py
│   └── workers.py
├── celerybeat-schedule
├── db_directory
│   └── database.sqlite3
├── local_beat.sh
├── local_run.sh
├── local_setup.sh
├── local_workers.sh
├── main.py
├── __pycache__
│   ├── main.cpython-310.pyc
│   └── main.cpython-38.pyc
├── readme.md
├── report
│   ├── firasans-bold.otf
│   ├── firasans-italic.otf
│   ├── firasans-lightitalic.otf
│   ├── firasans-light.otf
│   ├── firasans-regular.otf
│   ├── heading.svg
│   ├── internal-links.svg
│   ├── multi-columns.svg
│   ├── report-cover.jpg
│   ├── report.css
│   ├── report.html
│   ├── style.svg
│   ├── table-content.svg
│   └── thumbnail.png
├── requirements.txt
├── static
│   ├── bootstrap
│   │   ├── css
│   │   │   └── bootstrap.min.css
│   │   └── js
│   │       └── bootstrap.min.js
│   ├── css
│   │   └── styles.css
│   ├── fonts
│   │   ├── font-awesome.min.css
│   │   ├── FontAwesome.otf
│   │   ├── FontAwesome.otfZone.Identifier
│   │   ├── fontawesome-webfont.eot
│   │   ├── fontawesome-webfont.eotZone.Identifier
│   │   ├── fontawesome-webfont.svg
│   │   ├── fontawesome-webfont.svgZone.Identifier
│   │   ├── fontawesome-webfont.ttf
│   │   ├── fontawesome-webfont.ttfZone.Identifier
│   │   ├── fontawesome-webfont.woff
│   │   ├── fontawesome-webfont.woff2
│   │   ├── fontawesome-webfont.woff2Zone.Identifier
│   │   └── fontawesome-webfont.woffZone.Identifier
│   ├── img
│   │   ├── computer.webp
│   │   └── computer.webpZone.Identifier
│   ├── js
│   │   ├── bs-init.js
│   │   ├── createLog.js
│   │   ├── createTracker.js
│   │   ├── home.js
│   │   ├── login.js
│   │   ├── signup.js
│   │   ├── summary.js
│   │   ├── updateLog.js
│   │   └── updateTracker.js
│   └── vue
│       ├── vue.js
│       ├── vue.jsZone.Identifier
│       ├── vue.min.js
│       └── vue.min.jsZone.Identifier
├── temp
└── templates
    ├── createLog.html
    ├── createTracker.html
    ├── home.html
    ├── login.html
    ├── monthly_report.html
    ├── signup.html
    ├── summary.html
    ├── updateLog.html
    └── updateTracker.html

```