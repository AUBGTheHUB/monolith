import { useLocation, useNavigate } from 'react-router-dom';
import { React, useState } from 'react';
import axios from 'axios';
import Validate, { url } from '../../../Global';
import { Card, Form, Button } from 'react-bootstrap';
import InvalidClient from '../invalid_client';

const JobActions = () => {
  const location = useLocation();
  const history = useNavigate();
  const job_data = location.state.job_data;

  const [formState, setFormState] = useState({
    logo: '',
    company: '',
    position: '',
    link: '',
    description: ''
  });

  const handleInputChange = (e) => {
    const target = e.target;
    const value = target.value;
    const name = target.name;

    setFormState({
      ...formState,
      [name]: value
    });
  };

  const remove_job = () => {
    axios({
      method: 'delete',
      url: url + '/api/job/' + job_data['id'] + '/',
      headers: { BEARER_TOKEN: localStorage.getItem('auth_token') }
    })
      // eslint-disable-next-line no-unused-vars
      .then((res) => {
        console.log('Job was deleted');
        history(-1);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const edit_job = () => {
    axios({
      method: 'put',
      url: url + '/api/job/' + job_data['id'],
      headers: { BEARER_TOKEN: localStorage.getItem('auth_token') },
      data: { ...formState }
    })
      // eslint-disable-next-line no-unused-vars
      .then((res) => {
        console.log('Job info was edited');
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
          <Card style={{ width: '18rem' }} className="member-card">
            <Card.Img variant="top" src={job_data['logo']} />
            <Card.Body>
              <Card.Title>{job_data['position']}</Card.Title>
              <Card.Text>{'Company: ' + job_data['company']}</Card.Text>
              <Card.Text>{job_data['description']}</Card.Text>
              <Button
                variant="primary"
                onClick={() => {
                  window.open(job_data['link']);
                }}
                className="linkedin-button"
              >
                LinkedIn
              </Button>
              <Button
                variant="primary"
                onClick={() => {
                  remove_job();
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
              <Form.Label>Position</Form.Label>
              <Form.Control
                type="text"
                placeholder="position"
                name="position"
                onChange={handleInputChange}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicText">
              <Form.Label>Company</Form.Label>
              <Form.Control
                type="text"
                placeholder="company"
                name="company"
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
              <Form.Label>Logo</Form.Label>
              <Form.Control
                type="text"
                placeholder="logo"
                name="logo"
                onChange={handleInputChange}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicText">
              <Form.Label>Link</Form.Label>
              <Form.Control
                type="text"
                placeholder="link"
                name="link"
                onChange={handleInputChange}
              />
            </Form.Group>
            <Button
              variant="primary"
              type="button"
              onClick={() => {
                edit_job();
              }}
            >
              Edit job
            </Button>
          </Form>
        </div>
      </div>
    );
  } else {
    return <InvalidClient />;
  }
};

export default JobActions;
