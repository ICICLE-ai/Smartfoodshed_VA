FROM node:latest as build-stage
RUN NODE_ENV=development npm i
WORKDIR /app
COPY package*.json ./
RUN npm --force install
COPY ./ .
RUN npm run build

FROM nginx as production-stage
RUN mkdir /app
COPY --from=build-stage /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf
