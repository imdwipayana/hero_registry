# Hero Registry

A full-stack hero database built with FastAPI + SQLModel + HTML/CSS/JS.

## Project structure

```
hero_app/
├── main.py            ← FastAPI + SQLModel backend
├── requirements.txt   ← Python dependencies
├── heroes.db          ← SQLite database (auto-created on first run)
└── static/
    └── index.html     ← Frontend UI
```

## Setup & run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the server
```bash
uvicorn main:app --reload
```

### 3. Open the app
Visit http://localhost:8000 in your browser.

## API endpoints

| Method | Path             | Description         |
|--------|------------------|---------------------|
| GET    | /heroes          | List all heroes     |
| POST   | /heroes          | Create a new hero   |
| DELETE | /heroes/{id}     | Delete a hero by id |

Interactive API docs are available at http://localhost:8000/docs
