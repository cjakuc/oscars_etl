FROM ubuntu:latest

# Installing packages and dependencies
RUN apt-get update && apt-get install -y ca-certificates git pip

COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp

WORKDIR /oscars_etl

# Build container
# docker build . -t oscars-etl
# Pulls from current directory's Dockerfile, name's image oscars-etl
# I need to use sudo for this in WSL, unclear why; user is added to docker group

# Running container from image on WSL:
# docker run --rm -d -t -v ~/oscars_etl:/oscars_etl --name oscars-container oscars-etl
# removes container after it's done running
# runs detached
# # -t for pseudo-tty to keep container running because it sets input to be the terminal
# mounts ~/oscars_etl to /oscars_etl

# Running container from image on Mac:
# docker run --rm -d -v ${pwd}:/oscars_etl --name oscars-container oscars-etl

# Opening terminal in running container:
# docker exec -it oscars-container /bin/bash
# executes bash terminal in oscars-container
# -i for interactive
# -t for pseudo-tty to keep container running because it sets input to be the terminal