import { useLocation, useNavigate } from "react-router-dom";
import { React, useState } from "react";
import axios from "axios";
import Validate, { url } from "../../../Global";
import { Card, Form, Button } from "react-bootstrap";
import InvalidClient from "../invalid_client";
import { formatDate } from "./render_events";

const EventsActions = () => {
  const location = useLocation();
  const history = useNavigate();
  const event_data = location.state.event_data;

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

  const remove_event = () => {
    axios({
      method: "delete",
      url: url + "/api/event/" + event_data["id"] + "/",
      headers: { BEARER_TOKEN: localStorage.getItem("auth_token") },
    })
      // eslint-disable-next-line no-unused-vars
      .then((res) => {
        console.log("Event deleted");
        history(-1);
      })
      // eslint-disable-next-line no-unused-vars
      .catch((res) => {
        console.log("Couldn't delete event");
      });
  };

  const edit_event = () => {
    axios({
      method: "put",
      url: url + "/api/event/" + event_data["id"],
      headers: { BEARER_TOKEN: localStorage.getItem("auth_token") },
      data: { ...formState },
    })
      // eslint-disable-next-line no-unused-vars
      .then((res) => {
        console.log("Job info was edited");
        history(-1);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  if (Validate()) {
    return (
      <div className="actions-single-member">
        <div className="single-member-box">
          <Card style={{ width: "18rem" }} className="member-card">
            <Card.Img variant="top" src={event_data["banner"]} />
            <Card.Body>
              <Card.Title>{event_data["title"]}</Card.Title>
              <Card.Text>{event_data["description"]}</Card.Text>
              <Card.Text>{event_data["location"]}</Card.Text>
              {formatDate(event_data["startdate"], event_data["enddate"])}
              <Button
                variant="primary"
                onClick={() => {
                  window.open(event_data["facebooklink"]);
                }}
                className="linkedin-button"
              >
                LinkedIn
              </Button>
              <Button
                variant="primary"
                onClick={() => {
                  window.open(event_data["locationlink"]);
                }}
              >
                Location
              </Button>
              <Button
                variant="primary"
                className="padding-top-button-render-events"
                onClick={() => {
                  remove_event();
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
              <Form.Label>Title</Form.Label>
              <Form.Control
                type="text"
                placeholder="title"
                name="title"
                onChange={handleInputChange}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicText">
              <Form.Label>Start Date</Form.Label>
              <Form.Control
                type="text"
                placeholder="startdate"
                name="startdate"
                onChange={handleInputChange}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicText">
              <Form.Label>End Date</Form.Label>
              <Form.Control
                type="text"
                placeholder="enddate"
                name="enddate"
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
              <Form.Label>Location</Form.Label>
              <Form.Control
                type="text"
                placeholder="location"
                name="location"
                onChange={handleInputChange}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicText">
              <Form.Label>Location Link</Form.Label>
              <Form.Control
                type="text"
                placeholder="locationlink"
                name="locationlink"
                onChange={handleInputChange}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicText">
              <Form.Label>Banner</Form.Label>
              <Form.Control
                type="text"
                placeholder="banner"
                name="banner"
                onChange={handleInputChange}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicText">
              <Form.Label>Facebook Link</Form.Label>
              <Form.Control
                type="text"
                placeholder="facebooklink"
                name="facebooklink"
                onChange={handleInputChange}
              />
            </Form.Group>

            <Button
              variant="primary"
              type="button"
              onClick={() => {
                edit_event();
              }}
            >
              Edit event
            </Button>
          </Form>
        </div>
      </div>
    );
  } else {
    return <InvalidClient />;
  }
};

export default EventsActions;
