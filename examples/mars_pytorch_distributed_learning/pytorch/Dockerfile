FROM pytorch/pytorch:latest

RUN pip install vineyard

WORKDIR /var
ADD lstm.py /var/lstm.py

ENTRYPOINT ["python", "/var/lstm.py"]