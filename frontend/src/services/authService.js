import axios from "axios";
const url = "http://127.0.0.1:5000";

const login = async (email, password) => {
  try {
    // Make a POST request to your login endpoint with email and password
    const response = await axios.post(`${url}/login`, { email, password });

    // Assuming the response contains a token or user data, you can access it like this:
    const rsq = response.data;
    // Optionally, you can store the token in local storage or a state management system

    // Return any relevant data from the response
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

export { login, register, forgotPassword };
