FROM node:lts-alpine

WORKDIR /app

COPY package.json yarn.lock ./
RUN yarn install

COPY . .
RUN yarn build

EXPOSE 8000

CMD [ "node", "build/server.js" ]
