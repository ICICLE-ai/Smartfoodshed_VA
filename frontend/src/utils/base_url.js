import * as  https from 'https'
import axios from 'axios'
// import { Https, HttpRequestOptions, Method } from 'node-https';

// const https = new Https();

// Production backend url: "https://vaapibackend.pods.icicle.tapis.io/"
// Develop backend url: "https://vaapibackend.pods.icicle.develop.tapis.io/"
// Local development backend url: "http://localhost:5000/"
export const base_request_url = "http://localhost:5000/"
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