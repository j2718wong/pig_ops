FROM python:3.12

WORKDIR /pig_ops

COPY requirements.txt /pig_ops/requirements.txt
COPY ./webroot/. /pig_ops/.

# Set the environment variable
ENV PYTHONUNBUFFERED=1
ENV IN_A_DOCKER_CONTAINER=Yes

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /pig_ops/requirements.txt

EXPOSE 5000


CMD ["python3", "pig_ops_web.py"]
