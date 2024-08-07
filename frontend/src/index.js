import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Login from './views/login'; // Ensure the correct path to your Login component
import AdminLayout from "layouts/Admin/Admin.js";

import ThemeContextWrapper from "./components/ThemeWrapper/ThemeWrapper";
import BackgroundColorWrapper from "./components/BackgroundColorWrapper/BackgroundColorWrapper";
import ForgotPassword from "views/forgetPassword";

ReactDOM.render(
  <ThemeContextWrapper>
    <BackgroundColorWrapper>
      <BrowserRouter>
        <Routes>
          <Route path="/admin/login" element={<Login />} />
          <Route path="/admin/forgot" element={<ForgotPassword />} />
          <Route path="/admin/*" element={<AdminLayout />} />
          <Route path="*" element={<Navigate to="/admin/login" replace />}
          />
        </Routes>
      </BrowserRouter>
    </BackgroundColorWrapper>
  </ThemeContextWrapper>,
  document.getElementById("root")
);
