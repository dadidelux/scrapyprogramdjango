# scrapyprogramdjango
an assignment to implement scrapy in django framework

# Scrapy and Django Project

## Description
A web scraping project using Scrapy to scrape data and Django to manage and display the scraped data.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Contributing](#contributing)
4. [License](#license)

## Installation

### Prerequisites
- Python 3.x
- PostgreSQL

### Steps
1. Clone the repository: `git clone https://github.com/dadidelux/scrapyprogramdjango.git`
2. Navigate to the project directory: `cd scrapyprogramdjango`
3. Install virtualenv: `python3 -m venv scrapy-django-venv`
4. Activate the virtual environment: 
   - On Windows: `.\scrapy-django-venv\Scripts\activate`
   - On Unix or MacOS: `source scrapy-django-venv/bin/activate`
5. Install the requirements: `pip install -r requirements.txt`
6. Setup the database: `python manage.py migrate`

## Usage

### Running the Scrapy Spider
1. Activate your virtual environment if it's not already activated:
   - On Windows: `.\scrapy-django-venv\Scripts\activate`
   - On Unix or MacOS: `source scrapy-django-venv/bin/activate`
2. Navigate to the Django project directory where `manage.py` is located: `cd myproject`
3. Run the spider using the Django management command: `python manage.py run_spider`


### Running the Django Server
1. Navigate back to the Django project directory: `cd ../../`
2. Run the server: `python manage.py runserver`
3. Open a web browser and visit: `http://127.0.0.1:8000/`
