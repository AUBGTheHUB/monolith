import React from "react";
import { Card, Button } from "react-bootstrap";
import Validate from "../../../Global";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useState } from "react";
import { useEffect } from "react";
import InvalidClient from "../invalid_client";
import { url } from "../../../Global";

const RenderEvents = () => {
  const history = useNavigate();
  const [events, setEvents] = useState([{}]);

  const getJobs = () => {
    axios({
      method: "get",
      url: url + "/api/event",
    })
      .then((res) => {
        setEvents(res.data.data.events);
        // console.log(res.data.data.events);
      })
      // eslint-disable-next-line no-unused-vars
      .catch((err) => {
        // console.log(err);
      });
  };

  useEffect(() => {
    getJobs();
  }, []);

  if (Validate()) {
    return (
      <div className="members-box-add-button">
        <Button
          variant="primary"
          onClick={() => {
            history("/admin/dashboard/jobs/add", {});
          }}
        >
          Add Event
        </Button>
        <div className="members-box">
          {events.map((event, index) => (
            <Card
              style={{ width: "18rem" }}
              key={index}
              className="member-card"
            >
              <Card.Img variant="top" src={event["banner"]} />
              <Card.Body>
                <Card.Title>{event["title"]}</Card.Title>
                <Card.Text>{event["description"]}</Card.Text>
                <Card.Text>{event["location"]}</Card.Text>
                <Card.Text>{event["startdate"]}</Card.Text>
                <Card.Text>{event["enddate"]}</Card.Text>
                <Button
                  variant="primary"
                  onClick={() => {
                    window.open(event["facebooklink"]);
                  }}
                  className="linkedin-button"
                >
                  LinkedIn
                </Button>
                <Button
                  variant="primary"
                  onClick={() => {
                    window.open(event["locationlink"]);
                  }}
                >
                  Location
                </Button>
                <Button
                  variant="primary"
                  onClick={() => {
                    history("/admin/dashboard/jobs/actions", {
                      state: {
                        event_data: event,
                      },
                    });
                    console.log(event["id"]);
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

export default RenderEvents;
