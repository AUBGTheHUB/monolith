import axios from "axios";
import { useNavigate } from "react-router-dom";
import { React, useState } from "react";
import { Form, Button } from "react-bootstrap";
import Validate from "../../../../Global";
import { url } from "../../../../Global";
import InvalidClient from "../../invalid_client";

const AddJury = () => {
  const history = useNavigate();

  const [formState, setFormState] = useState({
    firstname: "",
    company: "",
    position: "",
    sociallink: "",
    lastname: "",
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

  const addNewJob = () => {
    axios({
      method: "post",
      url: url + "/api/jury/",
      headers: { BEARER_TOKEN: localStorage.getItem("auth_token") },
      data: { ...formState },
    })
      // eslint-disable-next-line no-unused-vars
      .then((res) => {
        console.log("New Jury has been added");
        history(-1);
      })
      .catch((err) => {
        alert(err["response"]["data"]["data"]["data"]);
        console.log(err);
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
            <Form.Label>Company</Form.Label>
            <Form.Control
              type="text"
              placeholder="company"
              name="company"
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
            <Form.Label>Social Link</Form.Label>
            <Form.Control
              type="text"
              placeholder="Facebook/LinkedIn post/profile"
              name="sociallink"
              onChange={handleInputChange}
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicText">
            <Form.Label>Profile Picture</Form.Label>
            <Form.Control
              type="text"
              placeholder="gdrive link"
              name="profilepicture"
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
            Add new jury
          </Button>
        </Form>
      </div>
    );
  } else {
    return <InvalidClient />;
  }
};

export default AddJury;
