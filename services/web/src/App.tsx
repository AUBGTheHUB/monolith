import { Route, Routes } from 'react-router';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MainPage } from './website/MainPage/MainPage';
import { HackathonPage } from './website/HackathonPage/HackathonPage';
import { VerificationPage } from './website/VerificationPage/VerificationPage';
import { FormPage } from './website/RegistrationFormPage/RegistrationFormPage';
import { DashboardPage } from './website/AdminPanelPage/DashboardPage/DashboardPage';
import { MeetTheTeamPage } from './website/AdminPanelPage/DashboardPage/pages/MeetTheTeamPage/MeetTheTeamPage';
import { AddMemberPage } from './website/AdminPanelPage/DashboardPage/pages/MeetTheTeamPage/AddMemberPage';
import { EditMemberPage } from './website/AdminPanelPage/DashboardPage/pages/MeetTheTeamPage/EditMemberPage';

function App() {
    const queryClient = new QueryClient();

    return (
        <QueryClientProvider client={queryClient}>
            <Routes>
                <Route path="/" element={<MainPage />} />
                <Route path="/hackathon" element={<HackathonPage />} />
                <Route path="/hackathon/registration" element={<FormPage />} />
                <Route path="/hackathon/verification" element={<VerificationPage />} />

                {/* Meet the Team Routes */}
                <Route path="/dashboard" element={<DashboardPage />} />
                <Route path="/dashboard/meet-the-team" element={<MeetTheTeamPage />} />
                <Route path="/dashboard/meet-the-team/add" element={<AddMemberPage />} />
                <Route path="/dashboard/meet-the-team/:id" element={<EditMemberPage />} />
            </Routes>
        </QueryClientProvider>
    );
}

export default App;
