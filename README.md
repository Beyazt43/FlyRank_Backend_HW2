# Task API

A small CRUD API for managing a to-do list, built with FastAPI. Tasks are stored in a Docker Database

## How to run

1. Clone this repo and move into it:
   ```bash
   git clone <https://github.com/Beyazt43/FlyRank_Backend_HW1>
   cd <repo-folder>
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv

   # Windows PowerShell
   .\venv\Scripts\Activate.ps1

   # Mac/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the server:
   ```bash
   docker compose up
   ```

5. Visit `http://localhost:8000/docs` for interactive Swagger UI, or use curl / your browser directly against `http://localhost:8000`.

## Endpoints

| Method | Path | Description | Status codes |
|--------|------|-------------|---------------|
| GET | `/` | API info | 200 |
| GET | `/health` | Health check | 200 |
| GET | `/hello` | Greeting | 200 |
| GET | `/tasks` | List all tasks | 200 |
| GET | `/tasks/{id}` | Get one task | 200, 404 |
| POST | `/tasks` | Create a task | 201, 400 |
| PUT | `/tasks/{id}` | Update a task | 200, 400, 404 |
| DELETE | `/tasks/{id}` | Delete a task | 204, 404 |

## Example request

```
$ curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Do the homework"}'

output:

POST /tasks HTTP/1.1" 201 Created
content-type: application/json

{"id":4,"title":"Do the homework","done":false}
```


## Notes on validation behavior

- `POST`/`PUT` with a completely missing `title` field returns FastAPI's built-in `422 Unprocessable Content` (Pydantic's automatic schema validation).
- `POST`/`PUT` with an empty or whitespace-only `title` (e.g. `{"title": ""}`) returns a custom `400 Bad Request` from application-level validation.
- This two-layer behavior is standard for FastAPI and intentional — both cases are handled, just at different layers.

## Storage

Tasks are stored in PostgreSQL, running in Docker with a persistent volume. Data survives container restarts and app restarts — see "Persistence proof" below.

The project still includes an `InMemoryTaskRepository` implementation (in `repository.py`) from an earlier stage of the project, kept as a reference to show the repository pattern in practice — but it is no longer used by the running app. `main.py` currently instantiates `PostgresTaskRepository`.


## Persistence proof

To confirm data survives a full restart:

1. Created a new task via `POST /tasks` while the stack was running.
2. Confirmed it appeared in `GET /tasks`.
3. Ran `docker compose down` (stops and removes both containers, but not the volume).
4. Ran `docker compose up -d` to bring the whole stack back.
5. Ran `GET /tasks` again — the task was still present, confirming the Postgres volume persisted data independently of the container lifecycle.

## Architecture note

The switch from in-memory storage to Postgres only required changes to `repository.py` (adding `PostgresTaskRepository`) and one line in `main.py` (which repository class gets instantiated). `service.py` and all routes in `main.py` were untouched — proving the repository pattern's separation of concerns.
