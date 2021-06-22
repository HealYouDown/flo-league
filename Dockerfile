# Base Image
FROM alpine:latest

# Install dependencies
RUN apk add python3 python3-dev py3-pip build-base musl-dev libc-dev

# Upgrade pip
RUN pip3 install --upgrade pip

# Copy content
COPY ./app /flo_league/app
COPY ./main.py /flo_league/
COPY ./requirements.txt /flo_league/
COPY ./update_players.py /flo_league/

# Install dependencies
RUN pip3 install --ignore-installed six -r /flo_league/requirements.txt

# Fill database with players
RUN python3 /flo_league/update_players.py

# Delete packages that were only used to build pip-packages
RUN apk del python3-dev build-base musl-dev libc-dev

# Open Port 5000
EXPOSE 5000

# Run App
CMD [ "python3", "/flo_league/main.py" ]

# docker run -p 8080:5000 -e FLASK_ENV=production flo-league