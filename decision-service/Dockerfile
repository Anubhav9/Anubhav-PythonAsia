FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 2212
CMD ["python3","app.py"]