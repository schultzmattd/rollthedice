This project is largely based on the tutorial available [here](https://robertorocha.info/setting-up-a-selenium-web-scraper-on-aws-lambda-with-python/), which was in turn based on this [repo](https://github.com/21buttons/pychromeless)

## Setup to run locally

Note, these instructions assume you're going to run this locally from `rollthedice/action_network`

### Install python dependencies
`pip3 install -r requirements.txt`  

### Install chromedriver
#### MacOS
`brew cask install chromedriver`
#### Otherwise
Binary available [here](https://sites.google.com/a/chromium.org/chromedriver/downloads). Make sure that it is in your PATH

### Get headless-chromium binary
`curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-37/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip`  
Make this available at a folder at `rollthedice/action_network/bin`


### For debugging

- Build docker image as normal  
`make docker-build`
- Launch container with:  
`docker run --entrypoint "/bin/bash" -v <git checkout>rollthedice/action_network/src/:/var/task/src/ -ti action_network_lambda`
- Export relevant environment variables at prompt
```
export PYTHONPATH=$PYTHONPATH:/var/task/src:/var/task/lib
export PATH=$PATH:/var/task/bin
```
- Run script with PDB  
`python3 -m pdb src/rollthedice/action_network/action_network_daemon.py`