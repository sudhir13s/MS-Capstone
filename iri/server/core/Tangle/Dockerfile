FROM python:3.6

WORKDIR /app

COPY requirements.txt requirements.txt

ENV READTHEDOCS=True
#RUN pip install -U six wheel setuptools
#RUN pip install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 wxPython
RUN pip install -r requirements.txt

COPY ../../.. .

EXPOSE 5005:5005

CMD [ "python", "-u", "./tangle_api.py" ]
