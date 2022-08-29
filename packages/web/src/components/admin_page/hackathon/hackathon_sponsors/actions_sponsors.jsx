import { useLocation, useNavigate } from "react-router-dom";
import { React, useState } from "react";
import axios from "axios";
import { Card, Form, Button } from "react-bootstrap";
import InvalidClient from "../../invalid_client";
import Validate, { url } from "../../../../Global";

const SponsorsActions = () => {
  const location = useLocation();
  const history = useNavigate();
  const sponsor_data = location.state.sponsor_data;

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

  const remove_sponsor = () => {
    axios({
      method: "delete",
      url: url + "/api/sponsors/" + sponsor_data["id"] + "/",
      headers: { BEARER_TOKEN: localStorage.getItem("auth_token") },
    })
      // eslint-disable-next-line no-unused-vars
      .then((res) => {
        console.log("Sponsor has been deleted");
        history(-1);
      })
      .catch((err) => {
        alert(err["request"]["response"]["data"]);
      });
  };

  const edit_sponsor = () => {
    axios({
      method: "put",
      url: url + "/api/sponsors/" + sponsor_data["id"],
      headers: { BEARER_TOKEN: localStorage.getItem("auth_token") },
      data: { ...formState },
    })
      // eslint-disable-next-line no-unused-vars
      .then((res) => {
        console.log("Mentor info has been edited");
        history(-1);
      })
      .catch((err) => {
        alert(err["response"]["data"]["data"]["data"]);
      });
  };

  if (Validate()) {
    return (
      <div className="actions-single-member">
        <div className="single-member-box">
          <Card style={{ width: "18rem" }} className="member-card">
            <Card.Img variant="top" src={sponsor_data["profilepicture"]} />
            <Card.Body>
              <Card.Title>{sponsor_data["profilepicture"]}</Card.Title>
              <Button
                variant="primary"
                onClick={() => {
                  window.open(sponsor_data["sociallink"]);
                }}
                className="linkedin-button"
              >
                Social Link
              </Button>
              <Button
                variant="primary"
                onClick={() => {
                  remove_sponsor();
                }}
              >
                Remove
              </Button>
            </Card.Body>
          </Card>
        </div>

        <div className="member-form-edit">
          <Form>
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
                edit_sponsor();
              }}
            >
              Edit Sponsor
            </Button>
          </Form>
        </div>
      </div>
    );
  } else {
    return <InvalidClient />;
  }
};

export default SponsorsActions;
