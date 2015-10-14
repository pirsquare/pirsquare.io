## Code for Personal Blog
Blog at [http://pirsquare.io](http://pirsquare.io)


## Requirements
Required Python Dependencies:
```shell
pip install pelican markdown awscli
```

## Setting Up
Once you have installed the required dependencies, run commands below
```shell
cd /opt

# Clone project
git clone https://github.com/pirsquare/pirsquare.io.git
git clone git@github.com:pirsquare/pirsquare.io.git
```

## Development
```shell
# In pelican root directory, update output directory for local testing
pelican content -o output -s pelicanconf.py

# Open html pages inside output directory
```

## Deploy
```shell
# Configure aws cli with access key and secret key.
# For region, use `ap-southeast-1` since we are using S3 in Singapore.
aws configure

# In pelican root directory, update the output directory.
pelican content -o output -s publishconf.py

# In pelican root directory, run following command to sync output directory.
# "audiencepi.com" here is the the S3 bucket name
aws s3 sync output s3://pirsquare.io --delete --acl "public-read" \
--cache-control "public, max-age=43200"
```
