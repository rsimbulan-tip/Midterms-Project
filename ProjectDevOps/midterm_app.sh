#!/bin/bash
mkdir tempdir
mkdir tempdir/templates
cp midterm_app.py tempdir/.
cp -r templates/* tempdir/templates/.

echo "FROM python" >> tempdir/Dockerfile
echo "RUN pip install flask" >> tempdir/Dockerfile
echo "COPY ./templates /home/myapp/templates" >> tempdir/Dockerfile
echo "COPY midterm_app.py /home/myapp" >> tempdir/Dockerfile
echo "CMD python3 /home/myapp/midterm_app.py" >> tempdir/Dockerfile

cd tempdir
docker build -t midterm .
docker run -t -d -p 5000:5000 --name midtermrunning midterm
docker ps -a

