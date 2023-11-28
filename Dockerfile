FROM python:3

# Change to use your own input file
ENV INPUT_FILE=input.txt

# Cannot clone private gitlab repo without setting up access key as a secret
# For simplicity, will copy files locally instead
# ENV GIT_REPO_URL=https://github.com/your-github-repo.git

WORKDIR /app

COPY requirements.txt app
COPY src app/src
COPY $INPUT_FILE app


RUN pip install -r requirements.txt

CMD python src/main.py $INPUT_FILE
