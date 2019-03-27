FROM python:3.7-alpine
WORKDIR /travelapp
COPY . /travelapp
RUN pip install -U -r requirements.txt
EXPOSE 8080
CMD ["python", "travelapp1.py"]
