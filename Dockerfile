FROM python:3.12

WORKDIR /pig_ops

COPY requirements.txt /pig_ops/requirements.txt
COPY ./webroot /pig_ops/webroot

# Set the environment variable
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /pig_ops/requirements.txt

EXPOSE 5000

CD /pig_ops/webroot

CMD ["python3", "pig_ops_web.py"]
