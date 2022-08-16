import React from "react";
import { useLocation } from "react-router-dom";
import { Card, Button, Form } from "react-bootstrap";
import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {url} from "../../../Global";

const MemberActions = () => {
  const location = useLocation();
  const history = useNavigate();
  const member_data = location.state.member_data;
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

  // pushing useNavigate -1 otherwise the previously passed state does not get saved (hence auth token)

  const remove_member = () => {
    axios({
      method: "delete",
      url: url + "/api/member/" + member_data['id'] + "/",
      headers: { BEARER_TOKEN: localStorage.getItem("auth_token") },
    })
      .then((res) => {
        console.log("Member was deleted");
        history(-1);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const edit_member = () => {
    axios({
      method: "put",
      url: url + "/api/member/" + member_data["id"],
      headers: { BEARER_TOKEN: localStorage.getItem("auth_token") },
      data: { ...formState },
    })
      .then((res) => {
        console.log("Member info was edited");
        history(-1);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <div className="actions-single-member">
      <div className="single-member-box">
        <Card style={{ width: "18rem" }} className="member-card">
          <Card.Img variant="top" src={member_data["profilepicture"]} />
          <Card.Body>
            <Card.Title>
              {member_data["firstname"] + " " + member_data["lastname"]}
            </Card.Title>
            <Card.Text>{"Position: " + member_data["position"]}</Card.Text>
            <Card.Text>{"Department: " + member_data["department"]}</Card.Text>
            <Button
              variant="primary"
              onClick={() => {
                window.open(member_data["sociallink"]);
              }}
              className="linkedin-button"
            >
              LinkedIn
            </Button>
            <Button
              variant="primary"
              onClick={() => {
                remove_member();
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
              edit_member();
            }}
          >
            Edit member
          </Button>
        </Form>
      </div>
    </div>
  );
};

export default MemberActions;
