# Dockerfile
FROM python:3.7-buster



# copy source and install dependencies
RUN mkdir -p /opt/app
COPY ./requirements/ /opt/app/requirements/
WORKDIR /opt/app
RUN pip install -r requirements/dev.txt

ADD . /opt/app
ADD ./scripts /scripts

RUN chmod +x /scripts/start.sh

# start server
EXPOSE 8000
STOPSIGNAL SIGTERM
CMD ["/scripts/start.sh"]