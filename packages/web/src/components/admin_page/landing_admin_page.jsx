import React from "react";
import { Form, Button } from "react-bootstrap";
import "./admin.css";
import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom"

const LandingAdminPage = () => {
  const history = useNavigate() 

  const [formState, setFormState] = useState({
    username: "",
    password: "",
  });

  const handleInputChange = (e) => {
    const target = e.target;
    const value = target.value;
    const name = target.name;

    setFormState({
      ...formState,
      [name]: value,
    });
  };

  const handleSubmit = (event) => {
    axios({
      method: "post",
      url: "http://127.0.0.1:8000/api/login",
      headers:{},
      data:{...formState}
    })
    .then((res) => {
      localStorage.setItem('auth_token', res.data.data.auth_token)
      history('/admin/dashboard')
    })
    .catch((err) => {
      // console.log({...formState});
      // console.log(err);
      console.log("Error logging in")
    })
  };

  return (
    <div className="login-page">
      <h3>Welcome to the Admin Page</h3>
      <Form>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>User</Form.Label>
          <Form.Control
            type="text"
            name="username"
            placeholder="Enter default user"
            onChange={handleInputChange}
          />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control
            name="password"
            type="password"
            onChange={handleInputChange}
          />
        </Form.Group>
        <Button
          variant="primary"
          type="button"
          onClick={() => {
            handleSubmit()
          }}
        >
          Submit
        </Button>
      </Form>
    </div>
  );
};

export default LandingAdminPage;
