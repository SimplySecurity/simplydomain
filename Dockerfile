# NOTE: Only use this when you want to build image locally
#       else use `docker pull simplysecurity\simplydomain:{VERSION}`
#       all image versions can be found at:

# -----BUILD ENTRY-----

# image base
FROM python:3

# author
MAINTAINER Killswitch-GUI
ADD VERSION .
LABEL description="Dockerfile base for SimplyDomain."

RUN python3 -m pip install simplydomain

ENTRYPOINT ["simply_domain.py"]

# -----END OF BUILD-----
