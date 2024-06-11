import axios from "axios";
import Cookies from 'js-cookie';

//REACT_APP_{varname}, process.env.{var_name}
const baseURL = 'http://52.231.138.94:5000'
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
      const response = await instance.get(`${baseURL}/get_area?ward=${_wardName}&&district=${_districtName}&&province=${_cityName}`);
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
