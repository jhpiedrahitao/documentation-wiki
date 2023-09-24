FROM python:3.10
RUN mkdir /documentation-wiki
COPY . /documentation-wiki
WORKDIR /documentation-wiki
RUN pip install -r requirements.txt
CMD ./launch.sh