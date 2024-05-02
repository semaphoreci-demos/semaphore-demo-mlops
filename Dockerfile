FROM python:3.12-slim
WORKDIR /usr/src/app
RUN groupadd -r appuser && useradd -r -g appuser appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p src/models
COPY src src
COPY models models

RUN chown -R appuser:appuser /usr/src/app
USER appuser

EXPOSE 8501
ENV MODEL_FILE "/usr/src/app/models/model.pkl"
CMD ["streamlit", "run", "--server.address", "0.0.0.0", "--server.port", "8501", "src/app.py"]
