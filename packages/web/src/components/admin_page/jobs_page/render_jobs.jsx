import React from "react";
import { Card, Button } from "react-bootstrap";
import Validate from "../../../Global";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useState } from "react";
import { useEffect } from "react";
import { url } from "../../../Global";
import InvalidClient from "../invalid_client";

const RenderJobs = () => {
  const history = useNavigate();
  const [jobs, setJobs] = useState([{}]);

  const getJobs = () => {
    axios({
      method: "get",
      url: url + "/api/job",
    })
      .then((res) => {
        setJobs(res.data.data.data);
        console.log(res.data.data.data);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  useEffect(() => {
    getJobs();
  }, []);

  const renderMap = () => {
    if (jobs) {
      return (
        <div className="members-box">
          {jobs.map((job, index) => (
            <Card
              style={{ width: "18rem" }}
              key={index}
              className="member-card"
            >
              <Card.Img variant="top" src={job["logo"]} />
              <Card.Body>
                <Card.Title>{job["position"]}</Card.Title>
                <Card.Text>{job["company"]}</Card.Text>
                <Card.Text>{job["description"]}</Card.Text>
                <Button
                  variant="primary"
                  onClick={() => {
                    window.open(job["link"]);
                  }}
                  className="linkedin-button"
                >
                  LinkedIn
                </Button>
                <Button
                  variant="primary"
                  onClick={() => {
                    history("/admin/dashboard/jobs/actions", {
                      state: {
                        job_data: job,
                      },
                    });
                    console.log(job["id"]);
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

  if (Validate()) {
    return (
      <div className="members-box-add-button">
        <Button
          variant="primary"
          onClick={() => {
            history("/admin/dashboard/jobs/add", {});
          }}
        >
          Add Job
        </Button>
        {renderMap()}
      </div>
    );
  } else {
    <InvalidClient />;
  }
};

export default RenderJobs;
