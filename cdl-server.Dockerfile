FROM python:3.11.0-slim-bullseye

RUN pip install fastapi uvicorn starlette pydantic

COPY server.py .

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]