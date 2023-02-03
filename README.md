# Smartfoodshed Visual Analytics VC1
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

## Deployment How-To
V1 and V2 Repos have github actions linked to them, these are defined in `repo:.github/workflows/<action name>.yml`. Currently (February 2023), when there is a new commit to to `main` branch, the action will build required images and deploy them to the Tapis Pods Service. More words on how it works in the actual yaml files.

## how to install 
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
