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
import RenderEvents from './components/admin_page/events_page/render_events';
import AddEvent from './components/admin_page/events_page/add_event';
import EventActions from './components/admin_page/events_page/actions_events';
import RenderArticles from './components/admin_page/articles_page/render_articles';
import AddArticle from './components/admin_page/articles_page/add_article';
import ArticleActions from './components/admin_page/articles_page/actions_articles';

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
      <Route path="/admin/dashboard/events" element={<RenderEvents/>} />
      <Route path="/admin/dashboard/events/add" element={<AddEvent/>} />
      <Route path="/admin/dashboard/events/actions" element={<EventActions/>} />
      <Route path="/admin/dashboard/articles" element={<RenderArticles/>} />
      <Route path="/admin/dashboard/articles/add" element={<AddArticle/>} />
      <Route path="/admin/dashboard/articles/actions" element={<ArticleActions/> } />
    </Routes>
    );
}

export default App;
