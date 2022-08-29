import React from "react";
import { Form, Button } from "react-bootstrap";
import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import Validate, { url } from "../../../Global";
import InvalidClient from "../invalid_client";

const AddMember = () => {
  const history = useNavigate();

  const [formState, setFormState] = useState({
    firstname: "",
    lastname: "",
    department: "",
    position: "",
    sociallink: "",
    profilepicture: "",
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

  const addNewMember = () => {
    axios({
      method: "post",
      url: url + "/api/member/",
      headers: { BEARER_TOKEN: localStorage.getItem("auth_token") },
      data: { ...formState },
    })
      // eslint-disable-next-line no-unused-vars
      .then((res) => {
        console.log("New member was added");
        history(-1);
      })
      .catch((err) => {
        alert(err["response"]["data"]["data"]["data"]);
      });
  };

  if (Validate()) {
    return (
      <div className="add-member-main-div">
        <Form>
          <Form.Group className="mb-3" controlId="formBasicText">
            <Form.Label>First Name</Form.Label>
            <Form.Control
              type="text"
              placeholder="firstname"
              name="firstname"
              onChange={handleInputChange}
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicText">
            <Form.Label>Last Name</Form.Label>
            <Form.Control
              type="text"
              placeholder="lastname"
              name="lastname"
              onChange={handleInputChange}
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicText">
            <Form.Label>Department</Form.Label>
            <Form.Control
              type="text"
              placeholder="department"
              name="department"
              onChange={handleInputChange}
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicText">
            <Form.Label>Position</Form.Label>
            <Form.Control
              type="text"
              placeholder="position"
              name="position"
              onChange={handleInputChange}
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicText">
            <Form.Label>LinkedIn Link</Form.Label>
            <Form.Control
              type="text"
              placeholder="sociallink"
              name="sociallink"
              onChange={handleInputChange}
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicText">
            <Form.Label>Drive Profile Picture</Form.Label>
            <Form.Control
              type="text"
              placeholder="profilepicture"
              name="profilepicture"
              onChange={handleInputChange}
            />
          </Form.Group>
          <Button
            variant="primary"
            type="button"
            onClick={() => {
              addNewMember();
            }}
          >
            Add new member
          </Button>
        </Form>
      </div>
    );
  } else {
    return <InvalidClient />;
  }
};

export default AddMember;
