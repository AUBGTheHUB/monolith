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
             <Card.Img
            className="dashboard-card-images-padding"
            variant="top"
            src={"https://drive.google.com/uc?export=view&id=1OafJ1dNdwLbypt4OqmmEiFEZnJmcwp2L"}
          />
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
            <Card.Img 
            className="dashboard-card-images-padding"
            variant="top"
            src={"https://drive.google.com/uc?export=view&id=1on8RJ0iH4II83qFq0LtwnAtx_hv2WQKg"}
            />
            <Card.Title>Events</Card.Title>
            <Card.Text>Add, edit or remove old and upcoming events.</Card.Text>
            <Button variant="primary">See current events</Button>
          </Card.Body>
        </Card>
        <Card style={{ width: "18rem" }} className="card-dash">
          <Card.Body>
            <Card.Img
            className="dashboard-card-images-padding"
            variant="top"
            src={"https://drive.google.com/uc?export=view&id=18_NX1g-0shWxds7aydq_vdak8phAo8Ou"}
            />
            <Card.Title>Articles</Card.Title>
            <Card.Text>
              Upload articles written by members of the club.{" "}
            </Card.Text>
            <Button variant="primary">See current articles</Button>
          </Card.Body>
        </Card>
        <Card style={{ width: "18rem" }} className="card-dash">
          <Card.Body>
            <Card.Img
            variant="top"
            className="dashboard-card-images-padding"
            src={"https://drive.google.com/uc?export=view&id=1CYATMxyuXaPFJT9ZuUeqSCcFQpa0iGbw"}
          />
            <Card.Title>Jobs</Card.Title>
            <Card.Text>
              Add or remove job positions provided by our sponsors.
            </Card.Text>
            <Button variant="primary">See current job positions</Button>
          </Card.Body>
        </Card>
      </div>
    </div>
  );
};

export default Dash;
