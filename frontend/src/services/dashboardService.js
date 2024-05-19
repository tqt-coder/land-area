import axios from "axios";
//REACT_APP_{varname}, process.env.{var_name}
const url = 'http://127.0.0.1:5000'
const DashBoardService = {
  /**
   * calc area from BE
   * 
   */
  calcArea: async (__code) => {
    try {
      const response = await axios.get(`${url}/get_area?ward_code=${__code}`);
      let xData = JSON.parse(response.data[0][0]);
      console.log(xData)
      let arr = Object.values(xData);
      arr.shift();
      console.log('dashboard: ' , arr);
      return arr; // Return the data from the response
    } catch (error) {
      console.error("Error calling other API:", error);
      throw error; // Re-throw the error to propagate it to the caller
    }
  }
};

export default DashBoardService;
