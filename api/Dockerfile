FROM ubuntu:20.04
WORKDIR /python-docker
COPY requirements.txt requirements.txt
COPY . .
RUN apt update && apt upgrade && apt-get install -y wget gnupg apt-transport-https
COPY linux_signing_key.pub linux_signing_key.pub
RUN apt-key add linux_signing_key.pub
RUN echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list
RUN export DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Madrid 
RUN echo "Preparing geographic area ..."
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils
RUN apt install -y python3-pip
RUN pip3 install -r requirements.txt
RUN apt-get update 
RUN apt install -yq google-chrome-stable && rm -rf /var/lib/apt/lists/*
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]