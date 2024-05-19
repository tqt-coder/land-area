import axios from "axios";
//REACT_APP_{varname}, process.env.{var_name}
const url = 'http://127.0.0.1:5000'
const LocationService = {
  /**
   * Get all provinces in Viet Name
   * @returns {Promise<{idProvince: string, name: string, id: string}[]>}
   */
  getProvincesOrCities: async () => {
    // const { data } = await axios.get("/provinces");
    try {
      // Make a GET request to another API endpoint
      const response = await axios.get(`${url}/provinces`);
      console.log(response);
      return response.data; // Return the data from the response
    } catch (error) {
      // Handle any errors that occur during the API call
      console.error("Error calling other API:", error);
      throw error; // Re-throw the error to propagate it to the caller
    }
  },
  /**
   *
   * @param {string} provinceIdOrCityId
   * @returns {Promise<{idProvince: string, idDistrict: string, name: string, id: string}[]>}
   */
  getDistrictsOrCities: async (provinceIdOrCityId) => {
    try {
      const response = await axios.get(`${url}/districts?province_code=${provinceIdOrCityId}`);
      console.log(response);
      return response.data; // Return the data from the response
    } catch (error) {
      // Handle any errors that occur during the API call
      console.error("Error calling other API:", error);
      throw error; // Re-throw the error to propagate it to the caller
    }
  },

  /**
   *
   * @param {string} districtIdOrCommuneId
   * @returns {Promise<{idDistrict: string, idCommune: string, name: string, id: string}[]>}
   */
  getWardsOrCommunes: async (districtIdOrCommuneId) => {
    try {
      const response = await axios.get(`${url}/wards?district_code=${districtIdOrCommuneId}`);
      console.log(response);
      return response.data; // Return the data from the response
    } catch (error) {
      // Handle any errors that occur during the API call
      console.error("Error calling other API:", error);
      throw error; // Re-throw the error to propagate it to the caller
    }
  },
};

export default LocationService;
