import React from 'react'; // eslint-disable-line no-unused-vars
import { useState } from 'react'; // eslint-disable-line no-unused-vars
import axios from 'axios'; // eslint-disable-line no-unused-vars
import './admin.css'; // eslint-disable-line no-unused-vars
import { Button } from 'react-bootstrap'; // eslint-disable-line no-unused-vars
import { useNavigate } from 'react-router-dom'; // eslint-disable-line no-unused-vars
import Dash from './dash_page'; // eslint-disable-line no-unused-vars
import InvalidClient from './invalid_client'; // eslint-disable-line no-unused-vars
import Validate from '../../Global';

// redundant page

const Dashboard = () => {
  if (Validate()) {
    return <Dash />;
  } else {
    return <InvalidClient />;
  }
};

export default Dashboard;
