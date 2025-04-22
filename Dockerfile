FROM mcr.microsoft.com/azure-functions/python:4-python3.11

RUN apt-get update && apt-get install -y \
    curl gnupg unixodbc unixodbc-dev gcc g++ libssl-dev libffi-dev libpq-dev libsasl2-dev

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

COPY . /home/site/wwwroot
WORKDIR /home/site/wwwroot

RUN pip install -r requirements.txt
