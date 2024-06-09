import axios from "axios";
const url = "http://52.231.219.61";

const login = async (email, password) => {
  try {
    const response = await axios.post(`${url}/login`, { email, password });
    const rsq = response.data;
    return rsq;
  } catch (error) {
    console.error("Error logging in:", error);
    throw error; // Re-throw the error to propagate it to the caller
  }
};

const register = async (email, password, username) => {
  try {
    // Make a POST request to your login endpoint with email and password
    const response = await axios.post(`${url}/register`, {
      email,
      password,
      username,
    });
    // Assuming the response contains a token or user data, you can access it like this:
    const rsq = response.data;
    // Return any relevant data from the response
    return rsq;
  } catch (error) {
    console.error("Error register :", error);
    throw error; // Re-throw the error to propagate it to the caller
  }
};

const forgotPassword = async (email) => {
    try {
      // Make a POST request to your login endpoint with email and password
      const response = await axios.post(`${url}/forgot`, {
        email
      });
      // Assuming the response contains a token or user data, you can access it like this:
      const rsq = response.data;
      // Return any relevant data from the response
      return rsq;
    } catch (error) {
      console.error("Error forgotPassword :", error);
      throw error; // Re-throw the error to propagate it to the caller
    }
  };

  const logoutFeature = async () => {
    try {
      // Make a POST request to your login endpoint with email and password
      const response = await axios.get(`${url}/logout`);
      // Assuming the response contains a token or user data, you can access it like this:
      const rsq = response.data;
      // Return any relevant data from the response
      return rsq;
    } catch (error) {
      console.error("Error logout :", error);
      throw error; // Re-throw the error to propagate it to the caller
    }
  };
export { login, register, forgotPassword, logoutFeature };
