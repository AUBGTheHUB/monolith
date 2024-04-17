import MemberActions from './components/admin_page/members_page/single_member';
import RenderJobs from './components/admin_page/jobs_page/render_jobs';
import JobActions from './components/admin_page/jobs_page/actions_jobs';
import AddJobs from './components/admin_page/jobs_page/add_jobs';
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
import RenderPartners from './components/admin_page/hackathon/hackathon_partners/render_partners';
import AddPartners from './components/admin_page/hackathon/hackathon_partners/add_partners';
import PartnersActions from './components/admin_page/hackathon/hackathon_partners/actions_partners';
import RenderSwitches from './components/admin_page/feature_switch_page/render_switch';
import S3Panel from './components/admin_page/s3_page/s3_landing';
import { RenderStorageObjects } from './components/admin_page/s3_page/render_objects';
import UrlsTable from './components/admin_page/url_shortener/table';
import { Routes, Route } from 'react-router-dom';
import BackBtn from './components/admin_page/back_button/back_button.jsx';
import { Hackteams } from './components/admin_page/hackathon/hackathon_teams/hackathon_teams.jsx';
import AddMember from './components/admin_page/members_page/new_member.jsx';

const adminRoutes = [
    {
        path: 'members',
        element: <RenderMembers />,
    },
    {
        path: 'members/actions',
        element: <MemberActions />,
    },
    {
        path: 'members/add',
        element: <AddMember />,
    },
    {
        path: 'jobs',
        element: <RenderJobs />,
    },
    {
        path: 'jobs/add',
        element: <AddJobs />,
    },
    {
        path: 'jobs/actions',
        element: <JobActions />,
    },
    {
        path: 'mentors',
        element: <RenderMentors />,
    },
    {
        path: 'mentors/actions',
        element: <MentorsActions />,
    },
    {
        path: 'mentors/add',
        element: <AddMentors />,
    },
    {
        path: 'jury',
        element: <RenderJury />,
    },
    {
        path: 'jury/add',
        element: <AddJury />,
    },
    {
        path: 'jury/actions',
        element: <JuryActions />,
    },
    {
        path: 'sponsors',
        element: <RenderSponsors />,
    },
    {
        path: 'sponsors/add',
        element: <AddSponsors />,
    },
    {
        path: 'sponsors/actions',
        element: <SponsorsActions />,
    },
    {
        path: 'partners',
        element: <RenderPartners />,
    },
    {
        path: 'partners/add',
        element: <AddPartners />,
    },
    {
        path: 'partners/actions',
        element: <PartnersActions />,
    },
    {
        path: 's3',
        element: <S3Panel />,
    },
    {
        path: 's3/objects',
        element: <RenderStorageObjects />,
    },
    {
        path: 'shortener',
        element: <UrlsTable />,
    },
    {
        path: 'fswitches',
        element: <RenderSwitches />,
    },
    {
        path: 'hackteams',
        element: <Hackteams />,
    },
];

const AdminRoutesWithBackButton = () => (
    <Routes>
        {adminRoutes.map(route => (
            <Route
                path={route.path}
                element={<AdminContainerWithButton component={route.element} path={route.path} />}
                key={route.path}
            />
        ))}
    </Routes>
);

const AdminContainerWithButton = ({ component, path }) => {
    return (
        <>
            <BackBtn positionButtonOnTop={path === 'shortener'} />
            {component}
        </>
    );
};

export default AdminRoutesWithBackButton;
