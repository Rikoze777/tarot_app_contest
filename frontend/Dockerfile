FROM node:12.22-buster-slim

WORKDIR /frontend

COPY frontend/ /frontend
RUN npm install
RUN npm run build
CMD ["npm", "start"]