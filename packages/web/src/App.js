import React from 'react';
import { Routes, Route } from 'react-router-dom';
import LandingHome from './components/spa/landing_home_page';
import LandingAdminPage from './components/admin_page/landing_admin_page';
import Dashboard from './components/admin_page/admin_dashboard';
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
import RenderMentors from './components/admin_page/hackathon/hackathon_mentors/render_mentors';
import AddMentors from './components/admin_page/hackathon/hackathon_mentors/add_mentors';
import MentorsActions from './components/admin_page/hackathon/hackathon_mentors/actions_mentors';
import RenderMembers from './components/admin_page/members_page/render_members';
import RenderJury from './components/admin_page/hackathon/hackathon_jury/render_jury';
import AddJury from './components/admin_page/hackathon/hackathon_jury/add_jury';
import JuryActions from './components/admin_page/hackathon/hackathon_jury/actions_mentors';
import RenderSponsors from './components/admin_page/hackathon/hackathon_sponsors/render_sponsors';
import AddSponsors from './components/admin_page/hackathon/hackathon_sponsors/add_sponsors';
import SponsorsActions from './components/admin_page/hackathon/hackathon_sponsors/actions_sponsors';
import RenderPartners from './components/admin_page/hackathon/hackathon_partners.jsx/render_partners';
import AddPartners from './components/admin_page/hackathon/hackathon_partners.jsx/add_partners';
import PartnersActions from './components/admin_page/hackathon/hackathon_partners.jsx/actions_partners';

function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingHome />} />
      <Route path="/admin" element={<LandingAdminPage />} />
      <Route path="/admin/dashboard" element={<Dashboard />} />
      <Route path="/admin/dashboard/members" element={<RenderMembers />} />
      <Route path="/admin/dashboard/members/actions" element={<MemberActions />} />
      <Route path="/admin/dashboard/members/add" element={<AddMember />} />
      <Route path="/admin/dashboard/jobs" element={<RenderJobs />} />
      <Route path="/admin/dashboard/jobs/actions" element={<JobActions />} />
      <Route path="/admin/dashboard/jobs/add" element={<AddJobs />} />
      <Route path="/admin/dashboard/events" element={<RenderEvents />} />
      <Route path="/admin/dashboard/events/add" element={<AddEvent />} />
      <Route path="/admin/dashboard/events/actions" element={<EventActions />} />
      <Route path="/admin/dashboard/articles" element={<RenderArticles />} />
      <Route path="/admin/dashboard/articles/add" element={<AddArticle />} />
      <Route path="/admin/dashboard/articles/actions" element={<ArticleActions />} />
      <Route path="/admin/dashboard/mentors" element={<RenderMentors />} />
      <Route path="/admin/dashboard/mentors/add" element={<AddMentors />} />
      <Route path="/admin/dashboard/mentors/actions" element={<MentorsActions />} />
      <Route path="/admin/dashboard/jury" element={<RenderJury />} />
      <Route path="/admin/dashboard/jury/add" element={<AddJury />} />
      <Route path="/admin/dashboard/jury/actions" element={<JuryActions />} />
      <Route path="/admin/dashboard/sponsors" element={<RenderSponsors />} />
      <Route path="/admin/dashboard/sponsors/add" element={<AddSponsors />} />
      <Route path="/admin/dashboard/sponsors/actions" element={<SponsorsActions />} />
      <Route path="/admin/dashboard/partners" element={<RenderPartners />} />
      <Route path="/admin/dashboard/partners/add" element={<AddPartners />} />
      <Route path="/admin/dashboard/partners/actions" element={<PartnersActions />} />
    </Routes>
  );
}

export default App;
