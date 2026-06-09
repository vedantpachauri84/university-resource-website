# University Resource Website

A Django-based University Resource Website that helps students access notes, previous year papers, study resources, and AI-powered paper analysis.

## Features

* User Registration and Login
* User Profile Management
* Notes Management
* Previous Year Question Papers
* Resource Sharing
* Subject and Year Filtering
* AI-Powered Paper Analysis using Gemini API
* Responsive Bootstrap UI

## Tech Stack

* Python
* Django
* SQLite
* Bootstrap
* HTML/CSS
* Gemini API
* Git & GitHub

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Virtual Environment

Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create Environment File

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key
```

### Run Migrations

```bash
python manage.py migrate
```

### Start Server

```bash
python manage.py runserver
```

## AI Features

The website includes an AI assistant that:

* Analyzes uploaded question papers
* Identifies important topics
* Estimates difficulty level
* Provides exam preparation tips

## Future Improvements

* PostgreSQL Integration
* Full Text Search
* AI Question Answering
* Deployment on Cloud
* Download Analytics

## Author

Vedant Pachauri
B.Tech Student

