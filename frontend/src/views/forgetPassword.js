import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { forgotPassword } from "../services/authService";
import { Helmet } from "react-helmet";
import "../assets/demo/login.css";

const ForgotPassword = () => {
  const navigate = useNavigate();
  const [error, setError] = useState(""); // Destructuring both state and setter function
  const [category, setCategory] = useState(""); // Destructuring both state and setter function
  const [email, setEmail] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await forgotPassword(email);
      setCategory(response.type || "error");
      setError(response.message || "Something went wrong!!");
      setTimeout(() => {
        setError("");
        if (response.status === 200) {
          navigate("/admin/login");
        }
      }, 5000);
    } catch (error) {
      setError("Internal Server Error");
      setCategory("error");
      setTimeout(() => {
        setError("");
      }, 10000);
    }
  };

  return (
    <>
      <Helmet>
        <script
          src="https://kit.fontawesome.com/64d58efce2.js"
          crossorigin="anonymous"
        ></script>
      </Helmet>
      <div className="container">
        {error && <p className={`alert alert-${category}`}>{error}</p>}
        <div className="forms-container">
          <div className="signin-signup">
            <form onSubmit={handleSubmit} className="sign-in-form form-css">
              <h4 className="title">Please input your email</h4>
              <div className="input-field">
                <i className="fas fa-envelope"></i>
                <input
                  type="email"
                  placeholder="Email"
                  name="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <input type="submit" value="Submit" className="btn btn-danger" />
            </form>
          </div>
        </div>
        <div className="panels-container">
          <div className="panel left-panel">
            <div className="content">
              <form
                action="/admin/login"
                method="get"
                className="sign-in-form form-css"
              >
                <input
                  type="submit"
                  value="Sign In"
                  className="btn btn-danger"
                />
              </form>
            </div>
            <img src="/assets/img/log.svg" className="image" alt="" />
          </div>
        </div>
      </div>
    </>
  );
};

export default ForgotPassword;
