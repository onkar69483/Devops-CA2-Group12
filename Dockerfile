# Use official jenkins base image
FROM jenkins/jenkins:lts

USER root

# Copy fixed script that includes fixed versionLT function
COPY scripts/fix_version.sh /usr/local/bin/fix_version.sh
RUN chmod +x /usr/local/bin/fix_version.sh

# Override or patch the version comparison logic here as required
# For demonstration, the script can be used or sourced by Jenkins startup scripts

USER jenkins
