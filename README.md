# auto-twitter-reset
Send automatic password reset emails to Twitter Accounts.

## Installation Instructions
```sh
git clone https://github.com/ayushanand18/auto-twitter-reset.git
cd auto-twitter-reset
cd api
docker build --tag twitter-reset .
docker run -d -p 5000:5000 twitter-reset
```

## Pre-requisites
* git
* docker
