# interface-template


```
## in the frontend file, install 
* remove node_modules 
* remove package-lock.json
* npm cache clean --force
* npm install 

## run the model 
* cd flask-vue-template
* source /env/bin/activate
* pip install Flask==1.0.2 Flask-Cors==3.0.7
* cd server
* python app.py # run the server
* cd frontend
* npm run dev # run the client


#if you have the error ELIFECYCLE errno 1 failed at the attention@1.0.0 dev script , try 
unset HOST


