# QuantifiedSelf App V2

## 📌 Overview

QuantifiedSelf App V2 is a self-tracking application that allows users to monitor their daily habits, activities, and life parameters. It enables users to create multiple trackers, log their progress, visualize trends, and receive reminders for their self-tracking goals. The app is built using a Flask backend, Vue.js frontend, SQLite for data storage, and Redis for caching and background jobs.

## 📝 Features

### 🌟 Core Features

- **User Authentication**: Secure login system using Flask Security and Token-Based Authentication.
- **Tracker Management**: Create, edit, delete, and view different types of trackers.
- **Data Logging**: Log values based on tracker types (Numerical, Multiple Choice, Time Duration, Boolean).
- **Dashboard**: View all trackers with last logged values and access logging view.
- **Trend Analysis**: Graphical representation of logged data and trendlines.
- **Data Export**: Export logs and tracker data as CSV.
- **Automated Reminders**: Daily reminder jobs through Google Chat.
- **Monthly Reports**: Auto-generated monthly progress reports sent via email. (Simulated using Mailhog)
- **Performance Optimization**: Redis caching to improve response time and efficiency.

### 🚀 Additional Features

- **Import Jobs**: Batch import tracker data.
- **PDF Reports**: Generate well-structured reports in both HTML and PDF formats.
- **Responsive UI**: Unified and mobile-friendly design.

## 🏗️ Tech Stack

- **Frontend**: Vue.js, Jinja2
- **Backend**: Flask (Python)
- **Database**: SQLite
- **Caching & Jobs**: Redis & Celery
- **Styling**: Bootstrap

## 🔧 Installation & Setup (Linux Environment Only)

### Prerequisites

- Linux-based system or WSL (for Windows users)
- Python & pip installed
- Redis installed (in-memory database)

### Steps to Run the App

1. Install `pip` (if not installed):
   ```bash
   sudo apt-get install python3-pip
   ```
2. Install Redis:
   ```bash
   sudo apt-get update
   sudo apt-get install redis
   ```
3. Run the `local_setup.sh` file to install all required dependencies:
   ```bash
   chmod +x local_setup.sh
   ./local_setup.sh
   ```
4. Start Redis for caching:
   ```bash
   sudo systemctl start redis-server
   ```
5. Install and run MailHog (Fake SMTP Email Server):
   ```bash
   sudo apt-get install golang-go
   go install github.com/mailhog/MailHog@latest
   MailHog &
   ```
6. Start Celery Beat for handling scheduled background tasks:
   ```bash
   chmod +x local_beat.sh
   ./local_beat.sh
   ```
7. Start Celery workers to process backend tasks:
   ```bash
   chmod +x local_workers.sh
   ./local_workers.sh
   ```
8. Finally, start the Flask server:
   ```bash
   chmod +x local_run.sh
   ./local_run.sh
   ```

## 📊 Example Use Cases

### 📈 Temperature Tracker

- **Use Case**: Track daily body temperature (useful for health monitoring)
- **Tracker Type**: Numerical
- **Example Logs**:
  ```json
  {
    "timestamp": "2022-05-26T11:42:00.73+05:30",
    "tracker": "Temperature",
    "value": 98.3,
    "note": "I was feeling okay"
  }
  ```

### 🏃 Running Tracker

- **Use Case**: Track daily running distance
- **Tracker Type**: Numerical
- **Example Logs**:
  ```json
  {
    "timestamp": "2022-05-27T10:42:00.73+05:30",
    "tracker": "Running",
    "value": 5,
    "note": "It was a good run. Felt a little tired but okay."
  }
  ```

## 📹 Demo

<Placeholder>

## 📂 Project Structure

<details>
<summary>Click to expand</summary>

```
.
├── api.yaml
├── application
│   ├── config.py
│   ├── controllers.py
│   ├── database.py
│   ├── models.py
│   ├── tasks.py
│   └── workers.py
├── celerybeat-schedule
├── db_directory
│   └── database.sqlite3
├── local_beat.sh
├── local_run.sh
├── local_setup.sh
├── local_workers.sh
├── main.py
├── readme.md
├── report
│   ├── firasans-bold.otf
│   ├── firasans-italic.otf
│   ├── firasans-light.otf
│   ├── firasans-lightitalic.otf
│   ├── firasans-regular.otf
│   ├── heading.svg
│   ├── internal-links.svg
│   ├── multi-columns.svg
│   ├── report-cover.jpg
│   ├── report.css
│   ├── report.html
│   ├── style.svg
│   ├── table-content.svg
│   └── thumbnail.png
├── report.pdf
├── requirements.txt
├── static
│   ├── bootstrap
│   │   ├── css
│   │   │   └── bootstrap.min.css
│   │   └── js
│   │       └── bootstrap.min.js
│   ├── css
│   │   └── styles.css
│   ├── fonts
│   │   ├── FontAwesome.otf
│   │   ├── FontAwesome.otf:Zone.Identifier
│   │   ├── font-awesome.min.css
│   │   ├── fontawesome-webfont.eot
│   │   ├── fontawesome-webfont.eot:Zone.Identifier
│   │   ├── fontawesome-webfont.svg
│   │   ├── fontawesome-webfont.svg:Zone.Identifier
│   │   ├── fontawesome-webfont.ttf
│   │   ├── fontawesome-webfont.ttf:Zone.Identifier
│   │   ├── fontawesome-webfont.woff
│   │   ├── fontawesome-webfont.woff2
│   │   ├── fontawesome-webfont.woff2:Zone.Identifier
│   │   └── fontawesome-webfont.woff:Zone.Identifier
│   ├── img
│   │   ├── computer.webp
│   │   └── computer.webp:Zone.Identifier
│   ├── js
│   │   ├── bs-init.js
│   │   ├── createLog.js
│   │   ├── createTracker.js
│   │   ├── home.js
│   │   ├── login.js
│   │   ├── signup.js
│   │   ├── summary.js
│   │   ├── updateLog.js
│   │   └── updateTracker.js
│   └── vue
│       ├── vue.js
│       ├── vue.js:Zone.Identifier
│       ├── vue.min.js
│       └── vue.min.js:Zone.Identifier
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

</details>

## 📜 Copyright Notice

This project was created as part of my coursework at the [Indian Institute of Technology, Madras](https://www.iitm.ac.in/) for my undergraduate degree.

**Copyright Notice**
This code is copyrighted by Sonu (c) 2022.

While this code is publicly available on GitHub, it is intended for viewing and learning purposes only. Use of this code in any other form, including modification, distribution, or incorporation into other projects, is prohibited without explicit permission from the copyright holder.

## 🎓 Special Thanks

A special thanks to my instructor [Thejesh GN (ತೇಜೇಶ್ ಜಿ.ಎನ್)](https://github.com/thejeshgn) for his invaluable guidance throughout the course. This project was made possible due to his mentorship. I am also grateful to him for helping me achieve the [Best MAD2 Project Award in May Term 2022](https://study.iitm.ac.in/student-achievements/projects/MAD2%20Project/2022/May%20Term%202022).

## 📞 Contact

For any inquiries, please contact [Sonu](mailto:smalik2811@gmail.com).
