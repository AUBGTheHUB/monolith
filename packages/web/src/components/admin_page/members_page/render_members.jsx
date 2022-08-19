import React from "react";
import { Card, Button } from "react-bootstrap";
import Validate from "../../../Global";
import { useNavigate } from "react-router-dom";
import InvalidClient from "../invalid_client";

const RenderMembers = (members) => {
  const history = useNavigate();

  if (Validate()) {
    return (
      <div className="members-box-add-button">
        <Button
          variant="primary"
          onClick={() => {
            history("/admin/dashboard/members/add", {
              state: {
                // we do not need it anymore -- id is generated in mongo automatically
              },
            });
          }}
        >
          Add Member
        </Button>
        <div className="members-box">
          {members.members.map((person, index) => (
            <Card
              style={{ width: "18rem" }}
              key={index}
              className="member-card"
            >
              <Card.Img variant="top" src={person["profilepicture"]} />
              <Card.Body>
                <Card.Title>
                  {person["firstname"] + " " + person["lastname"]}
                </Card.Title>
                <Card.Text>{"Position: " + person["position"]}</Card.Text>
                <Card.Text>{"Department: " + person["department"]}</Card.Text>
                <Button
                  variant="primary"
                  onClick={() => {
                    window.open(person["sociallink"]);
                  }}
                  className="linkedin-button"
                >
                  LinkedIn
                </Button>
                <Button
                  variant="primary"
                  onClick={() => {
                    history("/admin/dashboard/members/actions", {
                      state: {
                        member_data: person,
                      },
                    });
                    console.log(person["id"]);
                  }}
                >
                  Actions
                </Button>
              </Card.Body>
            </Card>
          ))}
        </div>
      </div>
    );
  } else {
    <InvalidClient />;
  }
};

export default RenderMembers;
