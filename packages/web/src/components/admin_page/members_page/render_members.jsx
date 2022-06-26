import React from "react";
import { Card, Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

const RenderMembers = (members) => {
  // console.log(members.members[0]["firstname"]);
  const history = useNavigate();
  // console.log(members.members[members.members.length-1]["memberid"]);
  return (
    <div className="members-box-add-button">
      <Button
        variant="primary"
        onClick={() => {
          history("/admin/dashboard/members/add", {
            state: {
              new_member_id:
                members.members[members.members.length - 1]["memberid"],
            },
          });
        }}
      >
        Add Member
      </Button>
      <div className="members-box">
        {members.members.map((person, index) => (
          <Card style={{ width: "18rem" }} key={index} className="member-card">
            <Card.Img
              variant="top"
              src={members.members[index]["profilepicture"]}
            />
            <Card.Body>
              <Card.Title>
                {members.members[index]["firstname"] +
                  " " +
                  members.members[index]["lastname"]}
              </Card.Title>
              <Card.Text>
                {"Position: " + members.members[index]["position"]}
              </Card.Text>
              <Card.Text>
                {"Department: " + members.members[index]["department"]}
              </Card.Text>
              <Button
                variant="primary"
                onClick={() => {
                  window.open(members.members[index]["sociallink"]);
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
                      member_data: members.members[index],
                      memberid: members.members[index]["memberid"],
                    },
                  });
                  console.log(members.members[index]["memberid"]);
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
  // return <h1>Hello, {members.members[0]["firstname"]}!</h1>
};

export default RenderMembers;
