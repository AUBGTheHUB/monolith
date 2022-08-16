import React from "react";
import { Card, Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

const Dash = (validated) => {
  const history = useNavigate();
  console.log("First dashboard!");
  return (
    <div className="dash">
      <div className="dash-box">
        <Card style={{ width: "18rem" }} className="card-dash">
          <Card.Body>
            <Card.Title>Members</Card.Title>
            <Card.Text>Add, edit or remove members of the club.</Card.Text>
            <Button
              variant="primary"
              onClick={() => {
                history("/admin/dashboard/members", {
                  state: {
                    validated: validated,
                  },
                });
              }}
            >
              See current members
            </Button>
          </Card.Body>
        </Card>
        <Card style={{ width: "18rem" }} className="card-dash">
          <Card.Body>
            <Card.Title>Events</Card.Title>
            <Card.Text>Add, edit or remove old and upcoming events.</Card.Text>
            <Button variant="primary">See current events</Button>
          </Card.Body>
        </Card>
        <Card style={{ width: "18rem" }} className="card-dash">
          <Card.Body>
            <Card.Title>Articles</Card.Title>
            <Card.Text>
              Upload articles written by members of the club.{" "}
            </Card.Text>
            <Button variant="primary">See current articles</Button>
          </Card.Body>
        </Card>
        <Card style={{ width: "18rem" }} className="card-dash">
          <Card.Body>
            <Card.Title>Jobs</Card.Title>
            <Card.Text>
              Add or remove job positions provided by our sponsors.
            </Card.Text>
            <Button variant="primary">See current job positions</Button>
          </Card.Body>
        </Card>
        <Card style={{ width: "18rem" }} className="card-dash">
          <Card.Body>
            <Card.Title>Hackathon Mentors</Card.Title>
            <Card.Text>
              Add or remove mentors for the hackathon.
            </Card.Text>
            <Button variant="primary">See current job positions</Button>
          </Card.Body>
        </Card>
        <Card style={{ width: "18rem" }} className="card-dash">
          <Card.Body>
            <Card.Title>Hackathon Jury</Card.Title>
            <Card.Text>
              Add or remove jury for the hackathon.
            </Card.Text>
            <Button variant="primary">See current job positions</Button>
          </Card.Body>
        </Card>
        <Card style={{ width: "18rem" }} className="card-dash">
          <Card.Body>
            <Card.Title>Hackathon Sponsors</Card.Title>
            <Card.Text>
              Add or remove sponsors for the hackathon.
            </Card.Text>
            <Button variant="primary">See current job positions</Button>
          </Card.Body>
        </Card>
        <Card style={{ width: "18rem" }} className="card-dash">
          <Card.Body>
            <Card.Title>Hackathon Partners</Card.Title>
            <Card.Text>
              Add or remove partners for the hackathon.
            </Card.Text>
            <Button variant="primary">See current job positions</Button>
          </Card.Body>
        </Card>

      </div>
    </div>
  );
};

export default Dash;
