# the latest LTS (Long Term Support) version of Node.js
FROM node:16

WORKDIR /app/react

COPY package.json ./
COPY package-lock.json ./

RUN npm ci

EXPOSE 3000