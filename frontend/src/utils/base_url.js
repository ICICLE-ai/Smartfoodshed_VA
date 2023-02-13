import * as  https from 'https'
import axios from 'axios'
// import { Https, HttpRequestOptions, Method } from 'node-https';

// const https = new Https();

// export const base_request_url = "https://vaapi.pods.tacc.develop.tapis.io/"
// export const base_request_url = "https://vaapi.pods.icicle.develop.tapis.io/"
// export const base_request_url = "http://127.0.0.1:5000/"
// This is prod pod deployment url -> "https://vaapibackend.pods.icicle.tapis.io/"
// export const base_request_url
// console.log('The value of PORT is:', process.env);
export var base_request_url
if (process.env['NODE_ENV']=="production"){
  base_request_url = "https://vaapibackend.pods.icicle.tapis.io/" // Set VA_BACKEND_URL in environment variables
}else if(process.env['NODE_ENV']=='development'){
  base_request_url = "http://127.0.0.1:5000/"
}
export const apiClient = axios.create({
    baseURL: base_request_url,
    withCredentials: false,
    httpsAgent: new https.Agent({
      rejectUnauthorized: false,
    }),
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  })
  
// export const base_request_url = "https://vaapi.develop.tapis.io/"


// const agent = new https.Agent({  
//     rejectUnauthorized: false
//   });