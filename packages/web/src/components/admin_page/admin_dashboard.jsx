import React from "react";
import { useState } from "react";
import axios from "axios";
import "./admin.css";
import { Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import Dash from "./dash_page";
import InvalidClient from "./invalid_client";
import Validate from "../../Global";

const Dashboard = () => {
  if (Validate()) {
    return <Dash />;
  } else {
    return <InvalidClient />;
  }
};

export default Dashboard;
