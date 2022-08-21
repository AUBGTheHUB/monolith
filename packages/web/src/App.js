import React from 'react';
import { Routes, Route } from 'react-router-dom';
import LandingHome from './components/spa/landing_home_page';
import LandingAdminPage from './components/admin_page/landing_admin_page';
import Dashboard from './components/admin_page/admin_dashboard';
import Members from './components/admin_page/members_page/members';
import MemberActions from './components/admin_page/members_page/single_member';
import AddMember from './components/admin_page/members_page/new_member';
import RenderJobs from './components/admin_page/jobs_page/render_jobs';
import JobActions from './components/admin_page/jobs_page/actions_jobs';
import AddJobs from './components/admin_page/jobs_page/add_jobs';

function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingHome />} />
      <Route path="/admin" element={<LandingAdminPage />} />
      <Route path="/admin/dashboard" element={<Dashboard />} />
      <Route path="/admin/dashboard/members" element={<Members />} />
      <Route path="/admin/dashboard/members/actions" element={<MemberActions />} />
      <Route path="/admin/dashboard/members/add" element={<AddMember />} />
      <Route path="/admin/dashboard/jobs" element={<RenderJobs />} />
      <Route path="/admin/dashboard/jobs/actions" element={<JobActions/>} />
      <Route path="/admin/dashboard/jobs/add" element={<AddJobs/>} />
    </Routes>
  );
}

export default App;
