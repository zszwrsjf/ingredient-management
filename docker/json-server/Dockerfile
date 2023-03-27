# the latest LTS (Long Term Support) version of Node.js
FROM node:16

WORKDIR /app/json-server
RUN npm install -g json-server
EXPOSE 3000
COPY db.json* ./