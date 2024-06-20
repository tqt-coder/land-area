import axios from "axios";
import Cookies from 'js-cookie';

// Set the base URL for the axios instance
const baseURL = 'http://127.0.0.1:5000';

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
  calcArea: async (_province, _district, _ward, navigate) => {
    try {
      // Ensure the request is a POST request and pass the body correctly
      const response = await instance.post('/get_area', {
        province : _province,
        district : _district,
        ward: _ward
      });

      console.log(response);

      if (response.data.status !== 200 && response.data.status !== 403) {
        alert(response.data.message);
        navigate("/admin/map");
      }
      if (response.data.status === 403) {
        alert("Please login");
        navigate("/login");
      }

      let xData = response.data.area;
      let arr;
      if (xData) {
        arr = Object.values(xData);
        arr.shift();
      }

      let obj = {
        'arr': arr,
        'url': response.data.image_url
      };

      console.log('dashboard: ', obj);
      return obj; // Return the data from the response
    } catch (error) {
      console.error("Error calling other API:", error);
      throw error; // Re-throw the error to propagate it to the caller
    }
  }
};

export default DashBoardService;
