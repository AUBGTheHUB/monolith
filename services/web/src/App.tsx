import { Route, Routes } from 'react-router';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MainPage } from './website/MainPage/MainPage';
import { HackathonPage as Hackathon7 } from './website/HackathonPage7.0/HackathonPage';
import { VerificationPage } from './website/VerificationPage/VerificationPage';
import { FormPage } from './website/RegistrationFormPage/RegistrationFormPage';
import { MeetTheTeamPage } from '@/website/AdminPanelPage/DashboardPages/pages/MeetTheTeamPage/MeetTheTeamPage';
import { MeetTheTeamEditPage } from '@/website/AdminPanelPage/DashboardPages/pages/MeetTheTeamPage/MeetTheTeamEditPage';
import { LoginPage } from './website/AdminPanelPage/AuthPages/LoginPage/LoginPage';
import { HackathonPage } from './website/HackathonPage8.0/HackathonPage';
import { JudgesListPage } from '@/website/AdminPanelPage/DashboardPages/pages/JudgesPage/JudgesPage';
import { JudgesEditPage } from '@/website/AdminPanelPage/DashboardPages/pages/JudgesPage/JudgesEditPage';
import { SponsorsListPage } from '@/website/AdminPanelPage/DashboardPages/pages/SponsorsPage/SponsorsPage';
import { SponsorsEditPage } from '@/website/AdminPanelPage/DashboardPages/pages/SponsorsPage/SponsorsEditPage';
import { DashboardPage } from '@/website/AdminPanelPage/DashboardPages/DashboardPage';

import { PastEventsPage } from './website/AdminPanelPage/DashboardPages/pages/PastEventsPage/PastEventsPage';
import { PastEventsEditPage } from './website/AdminPanelPage/DashboardPages/pages/PastEventsPage/PastEventsEditPage';

import { Hackathon404Page } from '@/website/ErrorPages/Hackathon404Page/Hackathon404Page.tsx';
import { Admin404Page } from '@/website/ErrorPages/Admin404Page/Admin404Page.tsx';
import { Global404Page } from '@/website/ErrorPages/Global404Page/Global404Page.tsx';
import { RegisterPage } from './website/AdminPanelPage/AuthPages/RegisterPage/RegisterPage';
import { RefreshProvider } from './providers/RefreshProvider';

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
                    <Route path="login" element={<LoginPage />} />
                    <Route path="register" element={<RegisterPage />} />

                    <RefreshProvider>
                        <Route path="dashboard">
                            <Route index element={<DashboardPage />} />
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

                            {/* Past events Sub-group */}
                            <Route path="past-events">
                                <Route index element={<PastEventsPage />} />
                                <Route path="add" element={<PastEventsEditPage />} />
                                <Route path=":id" element={<PastEventsEditPage />} />
                            </Route>
                        </Route>
                    </RefreshProvider>
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
