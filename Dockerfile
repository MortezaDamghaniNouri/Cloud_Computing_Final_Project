#publicly available docker image "python" on docker hub will be pulled

FROM python

#creating directory cloud_computing in container (linux machine)

RUN mkdir c:\home\cloud_computing

RUN mkdir c:\home\cloud_computing\Output

#installing numpy library in the container

RUN pip install numpy

#copying Script.py from local directory to container's cloud_computing folder

COPY Script.py /home/cloud_computing/Script.py

COPY numbers.txt /home/cloud_computing/numbers.txt

COPY words.txt /home/cloud_computing/words.txt

#making the container to be up and running always

ENTRYPOINT ["tail", "-f", "/dev/null"]