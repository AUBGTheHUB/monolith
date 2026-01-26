import { Route, Routes } from 'react-router';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MainPage } from './website/MainPage/MainPage';
import { HackathonPage as Hackathon7 } from './website/HackathonPage7.0/HackathonPage';
import { VerificationPage } from './website/VerificationPage/VerificationPage';
import { FormPage } from './website/RegistrationFormPage/RegistrationFormPage';
import { LoginPage } from './website/AdminPanelPage/LoginPage/LoginPage';
import { HackathonPage } from './website/HackathonPage8.0/HackathonPage';
import { JudgesListPage } from './website/AdminPanelPage/DashboardPage/pages/JudgesPage/JudgesPage';
import { JudgesEditPage } from './website/AdminPanelPage/DashboardPage/pages/JudgesPage/JudgesEditPage';
import { SponsorsListPage } from './website/AdminPanelPage/DashboardPage/pages/SponsorsPage/SponsorsPage';
import { SponsorsEditPage } from './website/AdminPanelPage/DashboardPage/pages/SponsorsPage/SponsorsEditPage';
import { DashboardPage } from './website/AdminPanelPage/DashboardPage/DashboardPage';

function App() {
    const queryClient = new QueryClient();

    return (
        <QueryClientProvider client={queryClient}>
            <Routes>
                <Route path="/" element={<MainPage />} />
                <Route path="/hackathon7.0" element={<Hackathon7 />} />
                <Route path="/hackathon" element={<HackathonPage />} />
                <Route path="/hackathon/registration" element={<FormPage />} />
                <Route path="/hackathon/verification" element={<VerificationPage />} />
                <Route path="/admin" element={<LoginPage />} />
                <Route path="/admin/dashboard" element={<DashboardPage />} />

                <Route path="/admin/judges" element={<JudgesListPage />} />
                <Route path="/admin/judges/add" element={<JudgesEditPage />} />
                <Route path="/admin/judges/:id" element={<JudgesEditPage />} />

                <Route path="/admin/sponsors" element={<SponsorsListPage />} />
                <Route path="/admin/sponsors/add" element={<SponsorsEditPage />} />
                <Route path="/admin/sponsors/:id" element={<SponsorsEditPage />} />
            </Routes>
        </QueryClientProvider>
    );
}

export default App;
