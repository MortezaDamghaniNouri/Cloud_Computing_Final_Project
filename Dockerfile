#publicly available docker image "python" on docker hub will be pulled

FROM python

#creating directory cloud_computing in container (linux machine)

RUN mkdir c:\home\cloud_computing

#copying Script.py from local directory to container's cloud_computing folder

COPY Script.py /home/cloud_computing/Script.py

#making the container to be up and running always

ENTRYPOINT ["tail", "-f", "/dev/null"]