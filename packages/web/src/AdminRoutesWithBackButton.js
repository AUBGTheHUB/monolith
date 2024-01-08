import MemberActions from './components/admin_page/members_page/single_member';
import AddMember from './components/admin_page/members_page/new_member';
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
import RenderTeams from './components/admin_page/hackathon/hackathon_teams/render_teams';
import RenderTeamMembers from './components/admin_page/hackathon/hackathon_team_members/render_hackathon_team_members';
import TeamActions from './components/admin_page/hackathon/hackathon_teams/actions_teams';
import RenderSwitches from './components/admin_page/feature_switch_page/render_switch';
import S3Panel from './components/admin_page/s3_page/s3_landing';
import { RenderStorageObjects } from './components/admin_page/s3_page/render_objects';
import TeamMemberActions from './components/admin_page/hackathon/hackathon_team_members/single_team_member.jsx';
import AddTeamMember from './components/admin_page/hackathon/hackathon_team_members/new_member';
import AddNewTeam from './components/admin_page/hackathon/hackathon_teams/new_team.jsx';
import RenderNoTeamParticipants from './components/admin_page/hackathon/hackathon_no_team_participants/render_no_team_participants';
import NoTeamParticipantsActions from './components/admin_page/hackathon/hackathon_no_team_participants/single_no_team_participant';
import AddNoTeamParticipant from './components/admin_page/hackathon/hackathon_no_team_participants/new_no_team_participant';
import UrlsTable from './components/admin_page/url_shortener/table';
import { Routes, Route } from 'react-router-dom';
import BackBtn from './components/admin_page/back_button/back_button.jsx';

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
        path: 'hackaton/teams',
        element: <RenderTeams />,
    },
    {
        path: 'hackaton/teams/actions',
        element: <TeamActions />,
    },
    {
        path: 'hackaton/teams/add',
        element: <AddNewTeam />,
    },
    {
        path: 'hackaton/teams/members',
        element: <RenderTeamMembers />,
    },
    {
        path: 'hackaton/teams/members/add',
        element: <AddTeamMember />,
    },
    {
        path: 'hackaton/teams/members/actions',
        element: <TeamMemberActions />,
    },
    {
        path: 'hackaton/noteamparticipants',
        element: <RenderNoTeamParticipants />,
    },
    {
        path: 'hackathon/noteamparticipants/add',
        element: <AddNoTeamParticipant />,
    },
    {
        path: 'hackathon/noteamparticipants/actions',
        element: <NoTeamParticipantsActions />,
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
