
# Use official jenkins base image
FROM jenkins/jenkins:lts

USER root

# Copy fixed script that includes fixed versionLT function
COPY scripts/fix_version.sh /usr/local/bin/fix_version.sh
RUN chmod +x /usr/local/bin/fix_version.sh

# Override or patch the version comparison logic here as required
# For demonstration, the script can be used or sourced by Jenkins startup scripts

USER jenkins

FROM node:20-alpine

USER node

RUN mkdir -p /home/node/app

WORKDIR /home/node/app

COPY --chown=node:node ./package.json ./

RUN npm install

COPY --chown=node:node ./ ./

CMD [ "npm", "run", "dev" ]
