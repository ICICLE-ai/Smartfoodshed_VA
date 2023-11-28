FROM node:lts-slim as build-stage
WORKDIR /app
COPY package*.json ./
COPY ./ .
RUN npm run build

FROM nginx as production-stage
RUN mkdir /app
COPY --from=build-stage /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf

COPY ./replace_env_vars.sh /docker-entrypoint.d/replace_env_vars.sh
RUN chmod +x /docker-entrypoint.d/replace_env_vars.sh
