import React from "react";
import { Form, Button } from "react-bootstrap";
import "./admin.css";
import {useState} from "react";
import { hasSelectionSupport } from "@testing-library/user-event/dist/utils";

const LandingAdminPage = () => {
  const [user, setUser] = useState("");
  const [pwd, setPwd] = useState("");
  const [success, setSuccess] = useState(false);

  const handleInputChange = (e) => hasSelectionSupport(e.target.value);

  const handleSubmit = (event) => {
    let admin = {
        username: user,
        password: pwd
    }

    axios.post("http://127.0.0.1:8000/api/login", admin)
    .then((res)=>{
        console.log(res.status);
        setSuccess(true)
    })
    .catch((err)=>{
        console.log(err)
        setSuccess(false)
    })
  }

  return (
    <div className="login-page">
      <h3>Welcome to the Admin Page</h3>
      <Form>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>User</Form.Label>
          <Form.Control type="email" placeholder="Enter default user" value={user} onChange={handleInputChange} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control type="password" placeholder="Password" value={pwd} onChange={handleInputChange}/>
        </Form.Group>
        <Button variant="primary" type="submit" onClick={()=>{
            handleSubmit()
            if(success === true){
                console.log("logged in");
            }
        }}>
          Submit
        </Button>
      </Form>
    </div>
  );
};

export default LandingAdminPage;
