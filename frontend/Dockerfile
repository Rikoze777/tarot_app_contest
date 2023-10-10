FROM node:18.18-alpine3.17

WORKDIR /frontend

COPY . /frontend
RUN npm install
CMD ["npm", "run", "build"]