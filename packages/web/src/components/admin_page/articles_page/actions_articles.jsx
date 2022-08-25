import { useLocation, useNavigate } from "react-router-dom";
import { React, useState } from "react";
import axios from "axios";
import Validate, { url } from "../../../Global";
import { Card, Form, Button } from "react-bootstrap";
import InvalidClient from "../invalid_client";

const ArticleActions = () => {
  const location = useLocation();
  const history = useNavigate();
  const article_data = location.state.article_data;

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

  const remove_article = () => {
    axios({
      method: "delete",
      url: url + "/api/article/" + article_data["id"] + "/",
      headers: { BEARER_TOKEN: localStorage.getItem("auth_token") },
    })
      // eslint-disable-next-line no-unused-vars
      .then((res) => {
        console.log("Job was deleted");
        history(-1);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const edit_article = () => {
    axios({
      method: "put",
      url: url + "/api/article/" + article_data["id"],
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
            <Card.Img variant="top" src={article_data["banner"]} />
            <Card.Body>
              <Card.Title>{article_data["title"]}</Card.Title>
              <Card.Text>{"Written by: " + article_data["author"]}</Card.Text>
              <Button
                variant="primary"
                onClick={() => {
                  window.open(article_data["mediumLink"]);
                }}
                className="linkedin-button"
              >
                Medium
              </Button>
              <Button
                variant="primary"
                onClick={() => {
                  remove_article();
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
              <Form.Label>Author</Form.Label>
              <Form.Control
                type="text"
                placeholder="firstName + lastName"
                name="author"
                onChange={handleInputChange}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicText">
              <Form.Label>Banner</Form.Label>
              <Form.Control
                type="text"
                placeholder="gdrive url link"
                name="banner"
                onChange={handleInputChange}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicText">
              <Form.Label>Medium Link</Form.Label>
              <Form.Control
                type="text"
                placeholder="medium url link"
                name="mediumLink"
                onChange={handleInputChange}
              />
            </Form.Group>

            <Button
              variant="primary"
              type="button"
              onClick={() => {
                edit_article();
              }}
            >
              Edit Article
            </Button>
          </Form>
        </div>
      </div>
    );
  } else {
    return <InvalidClient />;
  }
};

export default ArticleActions;
