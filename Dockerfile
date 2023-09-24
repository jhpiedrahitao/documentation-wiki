FROM python:3.10
RUN mkdir /documentation-wiki
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
WORKDIR /documentation-wiki
#COPY . /documentation-wiki
CMD ./launch.sh