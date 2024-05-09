import axios from "axios";

const LocationService = {
  /**
   * Get all provinces in Viet Name
   * @returns {Promise<{idProvince: string, name: string, id: string}[]>}
   */
  getProvincesOrCities: async () => {
    const { data } = await axios.get("/provinces");
    console.log(data);
    return data;
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
