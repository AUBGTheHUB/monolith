import { Route, Routes } from 'react-router';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MainPage } from './website/MainPage/MainPage';
import { HackathonPage as Hackathon7 } from './website/HackathonPage7.0/HackathonPage';
import { VerificationPage } from './website/VerificationPage/VerificationPage';
import { FormPage } from './website/RegistrationFormPage/RegistrationFormPage';
import { MeetTheTeamPage } from './website/AdminPanelPage/DashboardPage/pages/MeetTheTeamPage/MeetTheTeamPage';
import { MeetTheTeamEditPage } from './website/AdminPanelPage/DashboardPage/pages/MeetTheTeamPage/MeetTheTeamEditPage';
import { LoginPage } from './website/AdminPanelPage/LoginPage/LoginPage';
import { HackathonPage } from './website/HackathonPage8.0/HackathonPage';
import { JudgesListPage } from './website/AdminPanelPage/DashboardPage/pages/JudgesPage/JudgesPage';
import { JudgesEditPage } from './website/AdminPanelPage/DashboardPage/pages/JudgesPage/JudgesEditPage';
import { SponsorsListPage } from './website/AdminPanelPage/DashboardPage/pages/SponsorsPage/SponsorsPage';
import { SponsorsEditPage } from './website/AdminPanelPage/DashboardPage/pages/SponsorsPage/SponsorsEditPage';
import { DashboardPage } from './website/AdminPanelPage/DashboardPage/DashboardPage';
import { Hackathon404Page } from '@/website/ErrorPages/Hackathon404Page/Hackathon404Page.tsx';
import { Admin404Page } from '@/website/ErrorPages/Admin404Page/Admin404Page.tsx';
import { Global404Page } from '@/website/ErrorPages/Global404Page/Global404Page.tsx';

function App() {
    const queryClient = new QueryClient();

    return (
        <QueryClientProvider client={queryClient}>
            <Routes>
                {/* Public Routes */}
                <Route path="/" element={<MainPage />} />

                {/* Hackathon Group */}
                <Route path="/hackathon">
                    <Route index element={<HackathonPage />} />
                    <Route path="7.0" element={<Hackathon7 />} />
                    <Route path="registration" element={<FormPage />} />
                    <Route path="verification" element={<VerificationPage />} />
                    {/* 404 Catch-all */}
                    <Route path="*" element={<Hackathon404Page />} />
                </Route>

                {/* Admin Group */}
                <Route path="/admin">
                    <Route index element={<LoginPage />} />

                    <Route path="dashboard" element={<DashboardPage />} />

                    {/* Meet the Team Sub-group */}
                    <Route path="meet-the-team">
                        <Route index element={<MeetTheTeamPage />} />
                        <Route path="add" element={<MeetTheTeamEditPage />} />
                        <Route path=":id" element={<MeetTheTeamEditPage />} />
                    </Route>

                    {/* Judges Sub-group */}
                    <Route path="judges">
                        <Route index element={<JudgesListPage />} />
                        <Route path="add" element={<JudgesEditPage />} />
                        <Route path=":id" element={<JudgesEditPage />} />
                    </Route>

                    {/* Sponsors Sub-group */}
                    <Route path="sponsors">
                        <Route index element={<SponsorsListPage />} />
                        <Route path="add" element={<SponsorsEditPage />} />
                        <Route path=":id" element={<SponsorsEditPage />} />
                    </Route>
                    {/* 404 Catch-all */}
                    <Route path="*" element={<Admin404Page />} />
                </Route>
                {/* 404 Catch-all */}
                <Route path="*" element={<Global404Page />} />
            </Routes>
        </QueryClientProvider>
    );
}

export default App;
