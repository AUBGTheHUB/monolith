import React from "react";
import { Form, Button } from "react-bootstrap";
import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useLocation } from "react-router-dom";

const AddMember = () => {
  const history = useNavigate();
  const location = useLocation();
  let new_member_id = parseInt(location.state.new_member_id) + 1
  new_member_id = new_member_id.toString();

  const [formState, setFormState] = useState({
    memberid: new_member_id,
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
      url: "http://127.0.0.1:8000/api/member/",
      headers: { BEARER_TOKEN: localStorage.getItem("auth_token") },
      data: { ...formState },
    })
      .then((res) => {
        console.log("New member was added");
        history(-1);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <div className="add-member-main-div">
      <Form>
        <Form.Group className="mb-3" controlId="formBasicText">
          <Form.Label>Member ID</Form.Label>
          <Form.Control
            type="text"
            placeholder="last memberid++"
            name="memberid"
            value={new_member_id}
            readOnly
          />
        </Form.Group>
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
};

export default AddMember;
