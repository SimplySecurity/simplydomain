# NOTE: Only use this when you want to build image locally
#       else use `docker pull simplysecurity\simplydomain:{VERSION}`
#       all image versions can be found at:

# -----BUILD ENTRY-----

# image base
FROM python:alpine3.6

# author
MAINTAINER Killswitch-GUI
ADD VERSION .
LABEL description="Dockerfile base for SimplyDomain."

RUN apk add --no-cache bash git g++ make && \
git clone --branch master https://github.com/SimplySecurity/SimplyDomain.git && \
cd SimplyDomain && \
pip3 install -r setup/requirements.txt
ENV HOME=/SimplyDomain

# set working startup dir
WORKDIR "/SimplyDomain"
ENTRYPOINT ["python", "SimplyDomain.py"]

# -----END OF BUILD-----
