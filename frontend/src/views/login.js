import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { login, register } from "../services/authService"; // Assuming you have a register service
import { Helmet } from 'react-helmet';
import "../assets/demo/login.css";

const Login = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [category, setCategory] = useState("");
  const [isSignUpMode, setIsSignUpMode] = useState(false);
  
  // Registration state variables
  const [regEmail, setRegEmail] = useState("");
  const [regPassword, setRegPassword] = useState("");
  const [userName, setUserName] = useState("");

  // Function to handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (isSignUpMode) {
      // Registration form submission
      try {
        const response = await register(regEmail, regPassword, userName);
        setCategory(response.type || "error")
        setError(response.message || "Registration failed");
        if (response.status === 200) {
            setIsSignUpMode(false);
        } else {
            setIsSignUpMode(true);
        }
        setTimeout(() => {
          setError("");
        }, 2000);
    } catch (error) {
        setError("Internal Server Error");
        setCategory("error")
        // Clear error message after 10 seconds
        setTimeout(() => {
          setError("");
        }, 10000);
      }
    } else {
      // Login form submission
      try {
        const response = await login(email, password);
        if (response.status === 200) {
          navigate("/admin/map"); // Redirect after successful login
        } else {
          if (response.status === 403) {
            setError(response.message || "Please login");
            setCategory(response.type || "error")
          } else {
            setCategory(response.type || "error")
            setError(response.message || "Invalid email or password");
          }
          // Clear error message after 10 seconds
          setTimeout(() => {
            setError("");
          }, 2000);
        }
      } catch (error) {
        setError("Internal Server Error");
        setCategory("error")
        // Clear error message after 10 seconds
        setTimeout(() => {
          setError("");
        }, 1000);
      }
    }
  };

  // Function to toggle between sign-in and sign-up modes
  const toggleMode = () => {
    setIsSignUpMode((prevMode) => !prevMode);
  };

  return (
    <>
      <Helmet>
        <script src="https://kit.fontawesome.com/64d58efce2.js" crossorigin="anonymous"></script>
      </Helmet>
      <div className={`container ${isSignUpMode ? "sign-up-mode" : ""}`}>
        {error && <p className={`alert alert-${category}` }>{error}</p>}
        <div className="forms-container">
          <div className="signin-signup">
            <form
              id={isSignUpMode ? "register-form" : "login-form"}
              className={`${isSignUpMode ? "sign-up-form" : "sign-in-form"}`}
              onSubmit={handleSubmit}
            >
              <h2 className="title">{isSignUpMode ? "Sign Up" : "Sign In"}</h2>
              {isSignUpMode && (
                <div className="input-field">
                  <i className="fas fa-user"></i>
                  <input
                    type="text"
                    placeholder="UserName"
                    value={userName}
                    onChange={(e) => setUserName(e.target.value)}
                    required
                  />
                </div>
              )}
              <div className="input-field">
                <i className="fas fa-envelope"></i>
                <input
                  type="email"
                  placeholder="Email"
                  value={isSignUpMode ? regEmail : email}
                  onChange={(e) => isSignUpMode ? setRegEmail(e.target.value) : setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="input-field">
                <i className="fas fa-lock"></i>
                <input
                  type="password"
                  placeholder="Password"
                  value={isSignUpMode ? regPassword : password}
                  onChange={(e) => isSignUpMode ? setRegPassword(e.target.value) : setPassword(e.target.value)}
                  required
                />
              </div>
              <input
                type="submit"
                value={isSignUpMode ? "Sign Up" : "Login"}
                className="btn solid"
              />
              {!isSignUpMode && (
                // <a href="{{ url_for('forgot') }}" className="forgot-password-link">
                //   Forgot Password?
                // </a>
                 <Link to="/admin/forgot" className="forgot-password-link">Forgot Password?</Link>
              )}
              <p className="social-text">Or Sign in with social platforms</p>
              <div className="social-media">
                <a href="#" className="social-icon">
                  <i className="fab fa-facebook-f"></i>
                </a>
                <a href="#" className="social-icon">
                  <i className="fab fa-twitter"></i>
                </a>
                <a href="#" className="social-icon">
                  <i className="fab fa-google"></i>
                </a>
                <a href="#" className="social-icon">
                  <i className="fab fa-linkedin-in"></i>
                </a>
              </div>
            </form>
          </div>
        </div>
        <div className="panels-container">
          <div className="panel left-panel">
            <div className="content">
              <h3>Create an account</h3>
              <p></p>
              <button className="btn transparent" id="sign-up-btn" onClick={toggleMode}>
                Sign Up
              </button>
            </div>
            <img src="/assets/img/log.svg" className="image" alt="" />
          </div>
          <div className="panel right-panel">
            <div className="content">
              <h3>Already have an account?</h3>
              <p></p>
              <button className="btn transparent" id="sign-in-btn" onClick={toggleMode}>
                Sign In
              </button>
            </div>
            <img src="assets/img/register.svg" className="image" alt="" />
          </div>
        </div>
      </div>
    </>
  );
};

export default Login;
