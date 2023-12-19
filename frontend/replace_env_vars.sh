#!/bin/bash
# Taken from https://moreillon.medium.com/environment-variables-for-containerized-vue-js-applications-f0aa943cb962
# Enviornment variables are located in .env file

# Workdir
ROOT_DIR=/app;

# Go through all files that Vue writes the environ variables at runtime
for file in $ROOT_DIR/js/*.js* $ROOT_DIR/index.html $ROOT_DIR/precache-manifest*.js; do
  # Use sed to replace the placeholder (VAR_#) with the environ var.
  sed -i 's|VAR_1|'${BACKEND_URL}'|g' $file;
  sed -i 's|VAR_2|'${CLOUD_URL}'|g' $file;
  sed -i 's|VAR_3|'${COOKIE_DOMAIN}'|g' $file;
done;

# Continue with nginx execution
exec "$@"
