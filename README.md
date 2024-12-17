# Web Scraper System

A powerful, reliable, and flexible web scraping system for automated data collection.

## Features

- Task Management (creation, scheduling, monitoring)
- Proxy Pool Management
- Cookie Management
- Anti-scraping Mechanisms
- Task Scheduling and Execution
- Logging and Monitoring
- Performance Optimization
- Data Storage and Deduplication
- User Management and Access Control

## Installation

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
web_scraper/
├── app/
│   ├── api/            # API endpoints
│   ├── core/           # Core functionality
│   ├── models/         # Database models
│   ├── schemas/        # Pydantic schemas
│   └── services/       # Business logic
├── config/             # Configuration files
├── tests/              # Unit tests
└── requirements.txt    # Project dependencies
```

## Configuration

1. Create a `.env` file in the root directory
2. Add required environment variables:
```
DATABASE_URL=your_database_url
REDIS_URL=your_redis_url
SECRET_KEY=your_secret_key
```

## Usage

1. Start the Redis server
2. Start the Celery worker:
```bash
celery -A app.worker worker --loglevel=info
```
3. Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

## License

MIT License
