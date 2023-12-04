FROM python:3

# Change to copy a differenet input file to the container
ENV INPUT_FILE=input.txt

# Cannot clone private gitlab repo without setting up access key as a secret
# For simplicity, will copy files locally instead
# ENV GIT_REPO_URL=https://github.com/your-github-repo.git

RUN mkdir app

COPY requirements.txt app
COPY src app/src
COPY $INPUT_FILE app/input.txt

WORKDIR /app
RUN pip install -r requirements.txt
