import React from "react";
import { Card, Button } from "react-bootstrap";
import Validate from "../../../Global";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useState } from "react";
import { useEffect } from "react";
import InvalidClient from "../invalid_client";
import { url } from "../../../Global";

const months = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

const getPos = (string, subString, index) => {
  return string.split(subString, index).join(subString).length;
};

const formatDate = (start, end) => {
  if (start == undefined) {
    return null;
  }

  let startDatetime = new Date(start);

  let endDatetime = new Date(end);

  let formatStartDate =
    startDatetime.getDay() +
    " " +
    months[startDatetime.getMonth()] +
    " at " +
    startDatetime.getHours() +
    ":" +
    startDatetime.getMinutes();

  let formatEndDate =
    formatStartDate.slice(0, getPos(formatStartDate, " ", 2)) ==
    endDatetime.getDay() + " " + months[endDatetime.getMonth()]
      ? endDatetime.getHours() + ":" + endDatetime.getMinutes()
      : endDatetime.getDay() +
        " " +
        months[endDatetime.getMonth()] +
        " at " +
        endDatetime.getHours() +
        ":" +
        endDatetime.getMinutes();

  console.log(formatStartDate);
  return <Card.Text>{formatStartDate + " until " + formatEndDate}</Card.Text>;
};

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
        // maybe should be handled?
      });
  };

  useEffect(() => {
    getJobs();
  }, []);

  const renderMap = () => {
    if (events) {
      return (
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
                {formatDate(event["startdate"], event["enddate"])}
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
                  className="padding-top-button-render-events"
                  onClick={() => {
                    history("/admin/dashboard/events/actions", {
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
      );
    }
  };

  // eslint-disable-next-line no-unused-vars

  if (Validate()) {
    return (
      <div className="members-box-add-button">
        <Button
          variant="primary"
          onClick={() => {
            history("/admin/dashboard/events/add", {});
          }}
        >
          Add Event
        </Button>
        {renderMap()}
      </div>
    );
  } else {
    <InvalidClient />;
  }
};

export { formatDate };
export default RenderEvents;
