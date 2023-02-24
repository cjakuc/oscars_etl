oscars_etl

# Overview

# Running locally
This requires an AWS account with an S3 bucket with an AWS access key with read permissions on that bucket.
### Setup environment variables
Create a .env file in the root directory with the following secrets:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- BUCKET_NAME
### Build Docker container
`docker build . -t oscars-etl`
If running on WSL `sudo docker build . -t oscars-etl`
### Run Docker container
`docker run --rm -d -v ${pwd}:/oscars_etl --name oscars-container oscars-etl`
If running on WSL:
`docker run --rm -d -t -v ~/oscars_etl:/oscars_etl --name oscars-container oscars-etl`
### Access running container
`docker exec -it oscars-container /bin/bash`
### Run main.py from within the container
`python3 etl/main.py`
