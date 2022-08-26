import Validate from "../../../Global";
import InvalidClient from "../invalid_client";
import { url } from "../../../Global";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { React, useState } from "react";
import { Form, Button } from "react-bootstrap";

const AddJobs = () => {
  const history = useNavigate();

  const [formState, setFormState] = useState({
    logo: "",
    company: "",
    position: "",
    link: "",
    description: "",
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

  const addNewJob = () => {
    axios({
      method: "post",
      url: url + "/api/job/",
      headers: { BEARER_TOKEN: localStorage.getItem("auth_token") },
      data: { ...formState },
    })
      // eslint-disable-next-line no-unused-vars
      .then((res) => {
        console.log("New job was added");
        history(-1);
      })
      .catch((err) => {
        alert(err["response"]["data"]["message"]);
        console.log(err);
      });
  };

  if (Validate()) {
    return (
      <div className="add-member-main-div">
        <Form>
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
            <Form.Label>Company</Form.Label>
            <Form.Control
              type="text"
              placeholder="company"
              name="company"
              onChange={handleInputChange}
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicText">
            <Form.Label>Description</Form.Label>
            <Form.Control
              type="text"
              placeholder="description"
              name="description"
              onChange={handleInputChange}
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicText">
            <Form.Label>Logo</Form.Label>
            <Form.Control
              type="text"
              placeholder="logo"
              name="logo"
              onChange={handleInputChange}
            />
          </Form.Group>
          <Button
            variant="primary"
            type="button"
            onClick={() => {
              addNewJob();
            }}
          >
            Add new job
          </Button>
        </Form>
      </div>
    );
  } else {
    return <InvalidClient />;
  }
};

export default AddJobs;
