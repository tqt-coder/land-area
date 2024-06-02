import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { logoutFeature } from "../services/authService";
import Cookies from "js-cookie";

const Logout = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const handleLogout = async () => {
      try {
        const response = await logoutFeature();
        if (response.status === 200) {
          Cookies.set("token", "", { expires: 0 }); // Set cookie to expire in 1 day
          alert("You have been logged out.");
          navigate("/login"); // Redirect to the login page
        } else {
          alert("Logout failed. Please try again.");
        }
      } catch (error) {
        console.error("Error logging out:", error);
        alert("An error occurred. Please try again.");
      }
    };

    handleLogout();
  }, [navigate]);

  return (
    <div className="content">
      <h4 style={{ textAlign: "center" , marginTop: "100px"}}>Logging out...</h4>
    </div>
  );
};

export default Logout;
