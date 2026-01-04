import { Route, Routes, Navigate } from 'react-router';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MainPage } from './website/MainPage/MainPage';
import { HackathonPage } from './website/HackathonPage/HackathonPage';
import { VerificationPage } from './website/VerificationPage/VerificationPage';
import { FormPage } from './website/RegistrationFormPage/RegistrationFormPage';
import { LoginPage } from './website/AdminPanelPage/LoginPage/LoginPage';
import FeatureSwitchesPage from '@/website/AdminPanelPage/DashboardPage/pages/FeatureSwitchesPage/FeatureSwitchesPage';
import FeatureSwitchAddPage from '@/website/AdminPanelPage/DashboardPage/pages/FeatureSwitchesPage/FeatureSwitchAddPage';

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
                <Route path="/" element={<Navigate to="/dashboard/feature-switches" replace />} />
                <Route path="/dashboard/feature-switches" element={<FeatureSwitchesPage />} />
                <Route path="/dashboard/feature-switches/add" element={<FeatureSwitchAddPage />} />
                <Route path="*" element={<div style={{ padding: 24 }}>Not Found</div>} />
            </Routes>
        </QueryClientProvider>
    );
}

export default App;
