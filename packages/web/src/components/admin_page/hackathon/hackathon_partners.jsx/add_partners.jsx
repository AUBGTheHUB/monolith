import axios from "axios";
import { useNavigate } from "react-router-dom";
import { React, useState } from "react";
import { Form, Button } from "react-bootstrap";
import Validate from "../../../../Global";
import { url } from "../../../../Global";
import InvalidClient from "../../invalid_client";

const AddPartners = () => {
  const history = useNavigate();

  const [formState, setFormState] = useState({
    profilepicture: "",
    company: "",
    sociallink: "",
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
      url: url + "/api/partners/",
      headers: { BEARER_TOKEN: localStorage.getItem("auth_token") },
      data: { ...formState },
    })
      // eslint-disable-next-line no-unused-vars
      .then((res) => {
        console.log("New Partner has been added");
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
            <Form.Label>Company</Form.Label>
            <Form.Control
              type="text"
              placeholder="company name"
              name="company"
              onChange={handleInputChange}
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicText">
            <Form.Label>Logo</Form.Label>
            <Form.Control
              type="text"
              placeholder="logo"
              name="profilepicture"
              onChange={handleInputChange}
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicText">
            <Form.Label>Social Link</Form.Label>
            <Form.Control
              type="text"
              placeholder="social link"
              name="sociallink"
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
            Add new partner
          </Button>
        </Form>
      </div>
    );
  } else {
    return <InvalidClient />;
  }
};

export default AddPartners;
