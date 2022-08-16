import React from "react";
import { useState } from "react";
import axios from "axios";
import "./admin.css";
import { Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import Dash from "./dash_page";
import url from "../../Global";

const Dashboard = () => {
  const [validated, setValidated] = useState(false);
  const validate = () => {
    axios({
      method: "post",
      url: url + "/api/validate",
      headers: { BEARER_TOKEN: localStorage.getItem("auth_token") },
    })
      .then((res) => {
        setValidated(true);
      })
      .catch((err) => {
        console.log(err);
        setValidated(false);
      });
  };

  const history = useNavigate()
  validate();

  if (validated) {
    return <Dash validated={validated}/>;
  } else {
    return (
      <div className="client-not-validated">
        <div>
          <h3>Client is not validated</h3>
          <Button onClick={()=>{
            history('/admin/')
          }}>Return to login page</Button>
        </div>
      </div>
    );
  }
};

export default Dashboard;
