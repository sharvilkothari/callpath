FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY service/requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY callpath callpath
COPY service service
USER 65532:65532
CMD ["python", "-m", "uvicorn", "service.api:app", "--host", "0.0.0.0", "--port", "8000"]
