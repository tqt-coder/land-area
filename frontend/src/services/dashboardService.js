import axios from "axios";
import Cookies from 'js-cookie';

//REACT_APP_{varname}, process.env.{var_name}
const baseURL = 'http://127.0.0.1'
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
  calcArea: async (__code, navigate) => {
    try {
      const response = await instance.get(`${baseURL}/get_area?ward_code=${__code}`);
      if(response.status !== 200){
        alert("Please login");
        navigate("/login"); 
      }
      let xData = JSON.parse(response.data[0][0]);
      console.log(xData)
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
