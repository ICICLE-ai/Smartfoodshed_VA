# Smartfoodshed Visual Analytics VC1 (Version 1)
Visual analytics system built for smart food shed, especially for PPOD and Cold Chain data

## Deployments
Note: There are two versions, described below links for both.
### Version 1
* [Repository](https://github.com/ICICLE-ai/Smartfoodshed_VA_VC1)  
* [Frontend GUI](https://vaapifrontend.pods.icicle.tapis.io/)  
* [Backend API](https://vaapibackend.pods.icicle.tapis.io/)
* [Frontend Image](https://hub.docker.com/r/notchristiangarcia/vaapi-v1-f/)  
* [Backend Image](https://hub.docker.com/r/notchristiangarcia/vaapi-v1-b/)

### Version 2
* [Repository](https://github.com/ICICLE-ai/Smartfoodshed_VA_Flow)  
* [Frontend GUI](https://vaapi.pods.icicle.tapis.io/)  
* [Backend API](https://vaapiback.pods.icicle.tapis.io/)
* [Frontend Image](https://hub.docker.com/r/tuyamei/va-frontend/)  
* [Backend Image](https://hub.docker.com/r/tuyamei/va-backend/)

# Developer Docs
## Local Deployment (with docker)
There is a [Makefile](https://github.com/ICICLE-ai/Smartfoodshed_VA_VC1/blob/main/Makefile) in the root of this repostory and it provides utilities for docker local deployment.
1. You must ensure `docker`, `docker-compose`, and `make` are installed.
2. Run `make` while your current directory is the repo root.
    - This should descibe the make targets available and their purpose, the Makefile is simple, read it to understand exactly what actions are being taken.
3. To deploy, you can run `make down up`
    - Note that `up` also runs `build`, building images and then deploying the stack via a docker-compose file.
4. You can adjust urls, credentials, and ports in the [docker-compose.yml file](https://github.com/ICICLE-ai/Smartfoodshed_VA_VC1/blob/main/docker-compose.yml) via environment variables and compose variables.

## CI/CD Information
V1 and V2 Repos have github actions for CI/CD, these are defined in `repo:.github/workflows/<action name>.yml`. Currently (February 2023), when there is a new commit to to `main` branch, the action will build required images and deploy them to the Tapis Pods Service. [More words on how it works in the actual yaml files located here.](https://github.com/ICICLE-ai/Smartfoodshed_VA_VC1/blob/main/.github/workflows/main-build-push-deploy-images.yml)
   
## Local Deployment (without docker)
git clone the repo

cd Smartfoodshed_VA/new_gui/frontend

please use nodejs version 16.
npm install --legacy-peer-deps

## how to run 
### backend 
cd Smartfoodshed_VA/new_gui/backend
python app.py 

### frontend 
cd Smartfoodshed_VA/new_gui/frontend
npm run serve

open localhost:8080 in your broswer
