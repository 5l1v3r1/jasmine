FROM python:3.6
RUN adduser --disabled-login jasmine
WORKDIR /home/jasmine
COPY . .
# debian系的
COPY ./sources.list /etc/apt/
RUN apt-get update &&apt-get install libssl-dev
RUN pip install -r requirements.txt
RUN chmod -R +x .
EXPOSE 5000:5000
ENTRYPOINT ["./boot.sh","run"]