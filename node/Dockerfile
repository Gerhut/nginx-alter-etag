FROM node

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

ENV PORT 80
CMD [ "node", "." ]
