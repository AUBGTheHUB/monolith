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
import BackBtn from './components/admin_page/back_button';

const BackBtnAdmin = () => (
    <Routes>
        <Route path="members" element={<BackBtnAdd Component={RenderMembers} />} />
        <Route path="members/actions" element={<BackBtnAdd Component={MemberActions} />} />
        <Route path="members/add" element={<BackBtnAdd Component={AddMember} />} />
        <Route path="jobs" element={<BackBtnAdd Component={RenderJobs} />} />
        <Route path="jobs/actions" element={<BackBtnAdd Component={JobActions} />} />
        <Route path="mentors" element={<BackBtnAdd Component={RenderMentors} />} />
        <Route path="mentors/add" element={<BackBtnAdd Component={AddMentors} />} />
        <Route path="mentors/actions" element={<BackBtnAdd Component={MentorsActions} />} />
        <Route path="jury" element={<BackBtnAdd Component={RenderJury} />} />
        <Route path="jury/add" element={<AddJury />} />
        <Route path="jury/actions" element={<BackBtnAdd Component={JuryActions} />} />
        <Route path="sponsors" element={<BackBtnAdd Component={RenderSponsors} />} />
        <Route path="sponsors/add" element={<BackBtnAdd Component={AddSponsors} />} />
        <Route path="sponsors/actions" element={<BackBtnAdd Component={SponsorsActions} />} />
        <Route path="partners" element={<BackBtnAdd Component={RenderPartners} />} />
        <Route path="partners/add" element={<BackBtnAdd Component={AddPartners} />} />
        <Route path="partners/actions" element={<BackBtnAdd Component={PartnersActions} />} />
        <Route path="hackathon/teams" element={<BackBtnAdd Component={RenderTeams} />} />
        <Route path="hackathon/teams/members" element={<BackBtnAdd Component={RenderTeamMembers} />} />
        <Route path="hackathon/teams/members/actions" element={<BackBtnAdd Component={TeamMemberActions} />} />
        <Route path="hackathon/teams/members/add" element={<BackBtnAdd Component={AddTeamMember} />} />
        <Route path="hackathon/teams/add" element={<BackBtnAdd Component={AddNewTeam} />} />
        <Route path="hackathon/noteamparticipants/add" element={<BackBtnAdd Component={AddNoTeamParticipant} />} />
        <Route path="hackathon/teams/actions" element={<BackBtnAdd Component={TeamActions} />} />
        <Route path="hackathon/noteamparticipants" element={<BackBtnAdd Component={RenderNoTeamParticipants} />} />
        <Route
            path="hackathon/noteamparticipants/actions"
            element={<BackBtnAdd Component={NoTeamParticipantsActions} />}
        />
        <Route path="jobs" element={<BackBtnAdd Component={RenderJobs} />} />
        <Route path="jobs/actions" element={<BackBtnAdd Component={JobActions} />} />
        <Route path="jobs/add" element={<BackBtnAdd Component={AddJobs} />} />
        <Route path="s3" element={<BackBtnAdd Component={S3Panel} />} />
        <Route path="s3/objects" element={<BackBtnAdd Component={RenderStorageObjects} />} />
        <Route path="shortener" element={<BackBtnAdd Component={UrlsTable} />} />
        <Route path="fswitches" element={<BackBtnAdd Component={RenderSwitches} />} />
    </Routes>
);
const BackBtnAdd = ({ Component }) => {
    return (
        <div>
            <BackBtn />
            <Component />
        </div>
    );
};
export default BackBtnAdmin;
