FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install --upgrade pip wheel "poetry==2.2.0"

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

# Установка зависимостей БЕЗ установки корневого проекта
RUN poetry install --no-root
# --no-interaction --no-root
# RUN poetry install

COPY . .

EXPOSE 8000

# CMD ["python", "main.py"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
