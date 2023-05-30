FROM python:3.10.6-alpine
WORKDIR /fastapi_app
COPY . .
RUN pip install -r requirements.txt --no-cache-dir
ENV PYTHONPATH "${PYTHONPATH}:/fastapi_app"
RUN chmod +x start.sh
ENTRYPOINT ["./start.sh"]
CMD ["python", "app/main.py"]