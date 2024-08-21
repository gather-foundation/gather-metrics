##############################
## Dockerfile template for Web Projects
## This template is designed to generate 3 possible images: base, main, and test.
## base: the first image that includes all the dependencies, probably a bulky image.
## main: a minimal docker image with only the necessary files to run the web project.
## test: a fork of the base image that includes the test data and scripts, used to test the web project after each modification.
##############################

# MAIN_TAG must be defined before the first FROM to be able to pull from this value.
ARG MAIN_TAG

##############################
# Base image
##############################

## Change source as needed (e.g., node:latest, python:3.9, etc.)
FROM node:18.15 as base

## To avoid messing with internal docker files, we will copy everything and work in a subfolder
WORKDIR /app/

## Copy all required files/folders to compile/run the program
COPY --chmod=0755 package*.json ./

## Install your project's dependencies
RUN npm install

## Copy the remaining source code
COPY . .

## Build your web project if necessary (uncomment and adjust the command as needed)
# RUN npm run build

##############################
# Main image
##############################

## If only a part of the base image is needed, a tiny docker can be created from the base and copy the necessary files
FROM base as main

# Arguments needed for the labelling, provided from the docker build command
ARG BUILD_DATE
ARG BUILD_VERSION
ARG VCS_REF
ARG CI_PROJECT_NAME
ARG MAIN_TAG

# LABELS as per http://label-schema.org/rc1/
LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.version=$BUILD_VERSION
LABEL org.label-schema.build-date=$BUILD_DATE
LABEL org.label-schema.vcs-ref=$VCS_REF
LABEL org.label-schema.name=$CI_PROJECT_NAME

## Change following labels as pertinent, this is only informative.
LABEL org.label-schema.maintainer="Person McPersonFace"
LABEL org.label-schema.email="person@face.com"
LABEL org.label-schema.description="This image does awesome things and it's called My Web App."
LABEL org.label-schema.usage="http://docs.example.com/v1.2/usage"
LABEL org.label-schema.vcs-url="https://github.com/example/example-web-project"
LABEL org.label-schema.docker.cmd="docker run --rm -p 3000:3000 ${MAIN_TAG}"

# Expose the port your web project listens on (adjust the port number as needed)
EXPOSE 3000

# Define the command to start your web project (adjust the command as needed)
ENTRYPOINT [ "npm", "start" ]

##############################
# Test image
##############################

## In order to test, we can create a new image from main with additional test data and executables (or debugging)
# hadolint ignore=DL3006
FROM "$MAIN_TAG" as test

## Install any required dependencies for the test
# Uncomment and adjust the command to install test dependencies if needed
# RUN npm install --only=dev

## Automatically run the test so there is no additional arguments required
# Replace 'npm test' with the command to run your project's tests (e.g., 'python -m unittest', etc.)
RUN [ "npm", "test" ]
