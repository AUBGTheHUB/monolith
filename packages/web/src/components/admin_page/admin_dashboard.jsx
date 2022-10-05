import React from 'react';
import './admin.css';
import Dash from './dash_page';
import InvalidClient from './invalid_client';
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
