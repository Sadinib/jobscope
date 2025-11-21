JobScope

A complete job search platform API that scrapes job listings in real-time and matches candidates with relevant opportunities.

## Features

- JWT Authentication & User Profiles
- Multi-source Job Scraping (Computrabajo, Indeed)
- Smart Job Matching Algorithm
- FastAPI Backend with Auto-docs
- Celery Background Tasks
- Hybrid Database (PostgreSQL + MongoDB)

## Tech Stack

- **Backend**: FastAPI, Python
- **Database**: PostgreSQL, MongoDB
- **Async Tasks**: Celery
- **Scraping**: Requests, Selenium
- **Auth**: JWT, bcrypt
- **Deploy**: Railway

## Quick Start

1. Clone repo & install dependencies
2. Set up environment variables
3. Run: `python run_api.py`
4. Access: http://localhost:8000/docs

## API Endpoints

- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /jobs` - Browse job listings
- `POST /tasks/scrape` - Trigger job scraping
- `PUT /users/profile` - Update user profile