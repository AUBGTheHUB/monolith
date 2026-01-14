import { Route, Routes } from 'react-router';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MainPage } from './website/MainPage/MainPage';
import { HackathonPage } from './website/HackathonPage/HackathonPage';
import { VerificationPage } from './website/VerificationPage/VerificationPage';
import { FormPage } from './website/RegistrationFormPage/RegistrationFormPage';
import { LoginPage } from './website/AdminPanelPage/LoginPage/LoginPage';
import { JudgesListPage } from './website/AdminPanelPage/DashboardPage/pages/JudgesPage/JudgesPage';
import { JudgesEditPage } from './website/AdminPanelPage/DashboardPage/pages/JudgesPage/JudgesEditPage';

function App() {
    const queryClient = new QueryClient();

    return (
        <QueryClientProvider client={queryClient}>
            <Routes>
                <Route path="/" element={<MainPage />} />
                <Route path="/hackathon" element={<HackathonPage />} />
                <Route path="/hackathon/registration" element={<FormPage />} />
                <Route path="/hackathon/verification" element={<VerificationPage />} />
                <Route path="/admin" element={<LoginPage />} />

                <Route path="/admin/dashboard/judges" element={<JudgesListPage />} />
                <Route path="/admin/dashboard/judges/add" element={<JudgesEditPage />} />
                <Route path="/admin/dashboard/judges/:id" element={<JudgesEditPage />} />
            </Routes>
        </QueryClientProvider>
    );
}

export default App;
