import React from 'react';
import { Card, Button } from 'react-bootstrap';
import Validate from '../../../Global';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useState } from 'react';
import { useEffect } from 'react';
import { url } from '../../../Global';
import InvalidClient from '../invalid_client';

const RenderArticles = () => {
  const history = useNavigate();
  const [articles, setArticles] = useState([{}]);

  const getArticles = () => {
    axios({
      method: 'get',
      url: url + '/api/article'
    })
      .then((res) => {
        setArticles(res.data.data.data);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  useEffect(() => {
    getArticles();
  }, []);

  const renderMap = () => {
    if (articles)
      return (
        <div className="members-box">
          {articles.map((article, index) => (
            <Card style={{ width: '18rem' }} key={index} className="member-card">
              <Card.Img variant="top" src={article['banner']} />
              <Card.Body>
                <Card.Title>{article['title']}</Card.Title>
                <Card.Text>{'Written by: ' + article['author']}</Card.Text>
                <Button
                  variant="primary"
                  onClick={() => {
                    window.open(article['mediumLink']);
                  }}
                  className="linkedin-button"
                >
                  Read on Medium
                </Button>
                <Button
                  variant="primary"
                  onClick={() => {
                    history('/admin/dashboard/articles/actions', {
                      state: {
                        article_data: article
                      }
                    });
                  }}
                >
                  Actions
                </Button>
              </Card.Body>
            </Card>
          ))}
        </div>
      );
  };

  if (Validate()) {
    return (
      <div className="members-box-add-button">
        <Button
          variant="primary"
          onClick={() => {
            history('/admin/dashboard/articles/add', {});
          }}
        >
          Add Article
        </Button>
        {renderMap()}
      </div>
    );
  } else {
    <InvalidClient />;
  }
};

export default RenderArticles;
