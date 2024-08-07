import axios from "axios";
import { useNavigate } from "react-router-dom";
import Cookies from "js-cookie";

// Base URL of your Flask API
const baseURL = "http://127.0.0.1:5000";

// Create a new Axios instance with base URL
const instance = axios.create({
  baseURL,
  withCredentials: true, // Ensure that cookies are sent with requests
  headers: {
    "Content-Type": "application/json",
  },
});

// Add an interceptor to attach the token cookie to the headers of each request
instance.interceptors.request.use(
  (config) => {
    const token = Cookies.get("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

const LocationService = {
  downloadImage: async (_province, _district, _ward, _ward_code, navigate) => {
    try {
      const response = await instance.post(`${baseURL}/download_img`, {
        province : _province,
        district : _district,
        ward: _ward,
        wardCode: _ward_code
      });
      console.log(response)
      if(response.data.status === 500){
        alert(response.data.message);
      }else{
        if(response.data.status !== 200){
          alert("Please login");
          navigate("/login"); 
        }
      }
      console.log(response);
      return response.data; // Return the data from the response
    } catch (error) {
      // Handle any errors that occur during the API call
      console.error("Error calling /provinces endpoint:", error);
      alert("Please login");
      navigate("/admin/login");
    }
  },
  inferenceImage: async (_province, _district, _ward, _ward_code,navigate) => {
    try {
      const response = await instance.post('/get_inference', {
        province : _province,
        district : _district,
        ward: _ward,
        wardCode: _ward_code
      });
      console.log(response)
      if(response.data.status === 500){
        alert(response.data.message);
      }else{
        if(response.data.status !== 200){
          alert("Please login");
          navigate("/login"); 
        }
      }
      console.log(response);
      return response.data; // Return the data from the response
    } catch (error) {
      // Handle any errors that occur during the API call
      console.error("Error calling /provinces endpoint:", error);
      alert("Please login");
      // navigate("/login");
    }
  },
  getProvincesOrCities: async (navigate) => {
    try {
      // Make a GET request to the /provinces endpoint
      const response = await instance.get("/provinces");
      console.log(response);
      return response.data; // Return the data from the response
    } catch (error) {
      // Handle any errors that occur during the API call
      console.error("Error calling /provinces endpoint:", error);
      alert("Please login");
      navigate("/login");
    }
  },

  /**
   * Get districts or cities for a given province
   * @param {string} provinceIdOrCityId
   * @returns {Promise<{idProvince: string, idDistrict: string, name: string, id: string}[]>}
   */
  getDistrictsOrCities: async (provinceIdOrCityId, navigate) => {
    try {
      const response = await instance.get(
        `/districts?province_code=${provinceIdOrCityId}`
      );
      console.log(response);
      return response.data; // Return the data from the response
    } catch (error) {
      console.error("Error calling /districts endpoint:", error);
      alert("Please login");
      navigate("/login");
    }
  },

  /**
   * Get wards or communes for a given district
   * @param {string} districtIdOrCommuneId
   * @returns {Promise<{idDistrict: string, idCommune: string, name: string, id: string}[]>}
   */
  getWardsOrCommunes: async (districtIdOrCommuneId, navigate) => {
    try {
      const response = await instance.get(
        `/wards?district_code=${districtIdOrCommuneId}`
      );
      console.log(response);
      return response.data;
    } catch (error) {
      console.error("Error calling /wards endpoint:", error);
      alert("Please login");
      navigate("/login");
    }
  },
};

// Intercept the response to check for 403 status
instance.interceptors.response.use(
  (response) => {
    if (response && response.status === 403) {
      // Redirect to login page
      const navigate = useNavigate();
      navigate("/admin/login");
    }
    return response;
  },
  (error) => {
    if (error.response) {
      // Redirect to login page
      const navigate = useNavigate();
      navigate("/admin/login");
    }
    return Promise.reject(error);
  }
);

export default LocationService;
