import * as  https from 'https'
import axios from 'axios'
// import { Https, HttpRequestOptions, Method } from 'node-https';

// const https = new Https();

export const base_request_url = "https://vaapi.pods.tacc.develop.tapis.io/"
export const apiClient = axios.create({
    baseURL: base_request_url, 
    withCredentials: false, 
    httpsAgent: new https.Agent({
      rejectUnauthorized: false,                                                            
    }),
    headers: {
      Accept: 'application/json', 
      'Content-Type': 'application/json'
    }
  })
  
// export const base_request_url = "https://vaapi.develop.tapis.io/"
// export const base_request_url = "http://127.0.0.1:5000/"

// const agent = new https.Agent({  
//     rejectUnauthorized: false
//   });