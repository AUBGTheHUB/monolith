import React from "react";
import {
  Routes,
  Route, 
} from 'react-router-dom'
import LandingHome from "./components/spa/landing_home_page";
import LandingAdminPage from "./components/admin_page/landing_admin_page"

function App() {
  return (
    <Routes>
    <Route path="/" element={<LandingHome/>}/>
    <Route path="/admin" element={<LandingAdminPage/>}/>
    </Routes>
  );
}

export default App;
