import { Route, Routes } from 'react-router';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MainPage } from './website/MainPage/MainPage';
import { HackathonPage } from './website/HackathonPage/HackathonPage';
import { VerificationPage } from './website/VerificationPage/VerificationPage';
import { FormPage } from './website/RegistrationFormPage/RegistrationFormPage';
import { DashboardPage } from './website/AdminPanelPages/DashboardPage/DashboardPage.tsx';
import { JudgesListPage } from './website/AdminPanelPages/JudgesListPage/JudgesListPage.tsx';
import { JudgesAddPage } from './website/AdminPanelPages/JudgesAddPage/JudgesAddPage.tsx';
import { JudgesEditPage } from './website/AdminPanelPages/JudgesEditPage/JudgesEditPage.tsx';

function App() {
    const queryClient = new QueryClient();

    return (
        <QueryClientProvider client={queryClient}>
            <Routes>
                <Route path="/" element={<MainPage />} />
                <Route path="/hackathon" element={<HackathonPage />} />
                <Route path="/hackathon/registration" element={<FormPage />} />
                <Route path="/hackathon/verification" element={<VerificationPage />} />р
                {/* Admin Dashboard for Admin Panel Routes */}
                <Route path="/dashboard" element={<DashboardPage />} />
                <Route path="/dashboard/judges" element={<JudgesListPage />} />
                <Route path="/dashboard/judges/add" element={<JudgesAddPage />} />
                <Route path="/dashboard/judges/:id" element={<JudgesEditPage />} />
            </Routes>
        </QueryClientProvider>
    );
}

export default App;
