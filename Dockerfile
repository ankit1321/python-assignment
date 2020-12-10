FROM python:3.7.1

ADD main.py .

COPY requirements.txt .

COPY ./known_images ./known_images


RUN pip install --upgrade pip

RUN pip install cmake

RUN pip install -r requirements.txt

CMD [ "python" , "./main.py" ]