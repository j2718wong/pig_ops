FROM python:3.12

WORKDIR /pig_ops

COPY requirements.txt /pig_ops/requirements.txt
COPY ./webroot /pig_ops/webroot

# Set the environment variable
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /pig_ops/requirements.txt

EXPOSE 5000

CMD ["python3", "webroot/pig_ops_web.py"]
