import axios from "axios";


const LocationService = {
  /**
   * Get all provinces in Viet Name
   * @returns {Promise<{idProvince: string, name: string, id: string}[]>}
   */
  getProvincesOrCities: async () => {
    // const { data } = await axios.get("/provinces");
    try {
      // Make a GET request to another API endpoint
      const response = await axios.get("http://127.0.0.1:5000/provinces");
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
    const { data } = await axios.get(
      `/district?idProvince=${provinceIdOrCityId}`
    );
    return data;
  },

  /**
   *
   * @param {string} districtIdOrCommuneId
   * @returns {Promise<{idDistrict: string, idCommune: string, name: string, id: string}[]>}
   */
  getWardsOrCommunes: async (districtIdOrCommuneId) => {
    const { data } = await axios.get(
      `/commune?idDistrict=${districtIdOrCommuneId}`
    );
    return data;
  },
};

export default LocationService;
