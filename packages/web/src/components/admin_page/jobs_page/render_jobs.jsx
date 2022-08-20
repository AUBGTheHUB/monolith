import React from 'react';
import { Card, Button } from 'react-bootstrap';
import Validate from '../../../Global';
import { useNavigate } from 'react-router-dom';
import InvalidClient from '../invalid_client';
import axios from 'axios';
import { useState } from 'react';
import { useEffect } from 'react';
import { url } from '../../../Global';

const RenderJobs = () => {
  const history = useNavigate();
  const [jobs, setJobs] = useState([{}]);

  const getJobs = () => {
    axios({
      method: 'get',
      url: url + '/api/job'
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

  if (Validate()) {
    return (
      <div className="members-box-add-button">
        <Button
          variant="primary"
          onClick={() => {
            history('/admin/dashboard/jobs/add', {});
          }}>
          Add Member
        </Button>
        <div className="members-box">
          {jobs.map((job, index) => (
            <Card style={{ width: '18rem' }} key={index} className="member-card">
              <Card.Body>
                <Card.Title>{job['position']}</Card.Title>
                <Card.Text>{'Company: ' + job['company']}</Card.Text>
                <Button
                  variant="primary"
                  onClick={() => {
                    window.open(job['link']);
                  }}
                  className="linkedin-button">
                  LinkedIn
                </Button>
                <Button
                  variant="primary"
                  onClick={() => {
                    history('/admin/dashboard/jobs/actions', {
                      state: {
                        job_data: job
                      }
                    });
                    console.log(job['id']);
                  }}>
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

export default RenderJobs;
