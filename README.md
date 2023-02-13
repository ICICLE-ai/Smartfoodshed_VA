# Smartfoodshed Visual Analytics VC1 (Version 1)
Visual analytics system built for smart food shed, especially for PPOD and Cold Chain data
## Description 
Our system offers a dynamic and engaging way to explore graph data. It is equipped with three main views, the **Graph View**, **Table View**, and **Map View**, providing a comprehensive and multi-perspective analysis of the data. 

![Main View](https://github.com/ICICLE-ai/Smartfoodshed_VA_VC1/blob/main/frontend/src/assets/mainView.png?raw=true)

* The **Graph View** is designed to provide an intuitive understanding of the relationships and patterns within the graph data. 
* The **Table View** and **Map View** offer alternative ways to view the data, providing different insights and perspectives. 
  
The system also allows for bi-directional interaction between the Graph View and the other two views, enabling users to seamlessly switch between the different perspectives and gain a deeper understanding of the data.


## Deployments
Note: There are two versions, described below links for both. We currently focus on the Version 1. 
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

<!-- # Developer Docs -->
### Local Deployment (with docker)
There is a [Makefile](https://github.com/ICICLE-ai/Smartfoodshed_VA_VC1/blob/main/Makefile) in the root of this repostory and it provides utilities for docker local deployment.
1. You must ensure `docker`, `docker-compose`, and `make` are installed.
2. Run `make` while your current directory is the repo root.
    - This should descibe the make targets available and their purpose, the Makefile is simple, read it to understand exactly what actions are being taken.
3. To deploy, you can run `make down up`
    - Note that `up` also runs `build`, building images and then deploying the stack via a docker-compose file.
4. You can adjust urls, credentials, and ports in the [docker-compose.yml file](https://github.com/ICICLE-ai/Smartfoodshed_VA_VC1/blob/main/docker-compose.yml) via environment variables and compose variables.

### CI/CD Information
V1 and V2 Repos have github actions for CI/CD, these are defined in `repo:.github/workflows/<action name>.yml`. Currently (February 2023), when there is a new commit to to `main` branch, the action will build required images and deploy them to the Tapis Pods Service. [More words on how it works in the actual yaml files located here.](https://github.com/ICICLE-ai/Smartfoodshed_VA_VC1/blob/main/.github/workflows/main-build-push-deploy-images.yml)
   
### Local Deployment (without docker)
* 📍 [Recommend to install Nodejs version 16]

```
> git clone the repo

> cd Smartfoodshed_VA/new_gui/frontend

> npm install --legacy-peer-deps
```

### Local Running 

#### Running Backend 
💡 Make sure you have the Neo4j Running in your local environment. And edit the app.py to your local setting 
```python
G1 = Graph("bolt://localhost:7687", auth=("YOUR_USERNAME", "YOUR_PASSWORD"), name="YOUR_DBNAME")
app.run()
```
Then running the following in your teminal: 
```
> cd Smartfoodshed_VA/new_gui/backend
> python app.py 
```
#### Frontend 
```
> cd Smartfoodshed_VA/new_gui/frontend
> npm run serve
# open localhost:8080 in your broswer
```
## Usage 
### 1. Table Exploration 
Easily switch between different tabs to view different sheets of the tabular data.
![Sheet Selector](https://github.com/ICICLE-ai/Smartfoodshed_VA_VC1/blob/main/frontend/src/assets/sheetSelector.png?raw=true)
### 2. Query from Table to Graph 
The Table View allows you to filter the data using keywords. Simply select the rows of interest and hit the 'Retrieve' button at the bottom. The corresponding entities in the graph will then be highlighted and displayed in the Graph View on the right.
![Table Query](https://github.com/ICICLE-ai/Smartfoodshed_VA_VC1/blob/main/frontend/src/assets/tableQuery_AdobeExpress.gif?raw=true)
### 3. Relation Expander
Explore Relationships: By clicking on each node, the distribution of its various relation types will be displayed in a pie chart. You can click on a relation type of your choice to expand the graph for further analysis.
![Relation Expander](https://github.com/ICICLE-ai/Smartfoodshed_VA_VC1/blob/main/frontend/src/assets/relationExpand_AdobeExpress.gif?raw=true)

Our system also gives users the flexibility to specify the number of entities to be displayed, using a slider bar. The default value is set to 5 entities.
![Relation Expander with Customized Thresholds](https://github.com/ICICLE-ai/Smartfoodshed_VA_VC1/blob/main/frontend/src/assets/relationExpandWithThreshold_AdobeExpress.gif?raw=true)


## Code
Project Structure: The project is divided into two main components, the front-end and the back-end. 
![Project Structure](https://github.com/ICICLE-ai/Smartfoodshed_VA_VC1/blob/main/frontend/src/assets/code_structure.png?raw=true)
* The front-end consists of three VUE files, each representing one of the three main views. 
* The back-end is composed of two main modules, app.py and helper.py. 
  * app.py is responsible for handling the incoming GET/POST requests from the front-end.
  * helper.py includes various querying functions and auxiliary helper functions.