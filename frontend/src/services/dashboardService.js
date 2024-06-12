import axios from "axios";
import Cookies from 'js-cookie';

//REACT_APP_{varname}, process.env.{var_name}
const baseURL = 'http://127.0.0.1:5000'
const instance = axios.create({
  baseURL,
  withCredentials: true, // Ensure that cookies are sent with requests
  headers: {
    'Content-Type': 'application/json',
  }
});

// Add an interceptor to attach the token cookie to the headers of each request
instance.interceptors.request.use(config => {
  const token = Cookies.get('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

const DashBoardService = {
  calcArea: async (_wardName, _districtName, _cityName, navigate) => {
    try {
      console.log(_wardName,_districtName,_cityName)
      // const response = await instance.get(`${baseURL}/get_area?ward=${_wardName}&&district=${_districtName}&&province=${_cityName}`);
      let response;
      response = {
        "data": {
            "area": {
                "0": 0.18556904254568,
                "1": 1.0268744593557197,
                "2": 0.28219992161095997,
                "3": 0.12838858597807998,
                "4": 0.2586378928993999,
                "5": 6.1729021858694395,
                "6": 4.897991101496359
            },
            "status": 200
        },
        "status": 200,
        "statusText": "OK",
        "headers": {
            "content-length": "184",
            "content-type": "application/json"
        },
        "config": {
            "transitional": {
                "silentJSONParsing": true,
                "forcedJSONParsing": true,
                "clarifyTimeoutError": false
            },
            "adapter": [
                "xhr",
                "http"
            ],
            "transformRequest": [
                null
            ],
            "transformResponse": [
                null
            ],
            "timeout": 0,
            "xsrfCookieName": "XSRF-TOKEN",
            "xsrfHeaderName": "X-XSRF-TOKEN",
            "maxContentLength": -1,
            "maxBodyLength": -1,
            "env": {},
            "headers": {
                "Accept": "application/json, text/plain, */*",
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGdtYWlsLmNvbSIsImV4cCI6MTcxODIzOTA2N30.tEKouffO4catgGuhxeEx93MJHIt7t3wkteL42aCZQ7U"
            },
            "baseURL": "http://127.0.0.1:5000",
            "withCredentials": true,
            "method": "get",
            "url": "http://127.0.0.1:5000/get_area?ward=Má Lé&&district=Đồng Văn&&province=Hà Giang"
        },
        "request": {}
    }
      console.log(response)
      if(response.data.status !== 200){
        alert("Please login");
        navigate("/login"); 
      }
      let xData = response.data.area;
      let arr;
      if(xData){
        arr = Object.values(xData);
        arr.shift();
      }
      console.log('dashboard: ' , arr);
      return arr; // Return the data from the response
    } catch (error) {
      console.error("Error calling other API:", error);
      throw error; // Re-throw the error to propagate it to the caller
    }
  }
};

export default DashBoardService;
