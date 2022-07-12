FROM python:3

RUN mkdir -p /opt/src/store
WORKDIR /opt/src/store

COPY store/customer.py ./customer.py
COPY store/configuration.py ./configuration.py
COPY store/models.py ./models.py
COPY store/role_check.py ./role_check.py
COPY store/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENV PYTHONPATH="/opt/src/store"

ENTRYPOINT ["python", "./customer.py"]
