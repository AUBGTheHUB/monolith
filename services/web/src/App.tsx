import { Route, Routes } from 'react-router';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MainPage } from './website/MainPage/MainPage';
import { HackathonPage } from './website/HackathonPage/HackathonPage';
import { VerificationPage } from './website/VerificationPage/VerificationPage';
import { FormPage } from './website/RegistrationFormPage/RegistrationFormPage';
import { SponsorsPage } from './website/AdminPanelPage/DashboardPage/pages/SponsorsPage/SponsorsPage';
import { SponsorsAddPage } from './website/AdminPanelPage/DashboardPage/pages/SponsorsPage/SponsorsAddPage';

function App() {
    const queryClient = new QueryClient();

    return (
        <QueryClientProvider client={queryClient}>
            <Routes>
                <Route path="/" element={<MainPage />} />
                <Route path="/hackathon" element={<HackathonPage />} />
                <Route path="/hackathon/registration" element={<FormPage />} />
                <Route path="/hackathon/verification" element={<VerificationPage />} />

                <Route path="/dashboard/sponsors" element={<SponsorsPage />} />
                <Route path="/dashboard/sponsors/add" element={<SponsorsAddPage />} />
            </Routes>
        </QueryClientProvider>
    );
}

export default App;
