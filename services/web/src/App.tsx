import { Route, Routes } from 'react-router';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MainPage } from './website/MainPage/MainPage';
import { HackathonPage } from './website/HackathonPage/HackathonPage';
import { VerificationPage } from './website/VerificationPage/VerificationPage';
import { FormPage } from './website/RegistrationFormPage/RegistrationFormPage';

import PastEventsPage from './website/AdminPanelPage/DashboardPage/pages/PastEventsPage/PastEventsPage';
import AddPastEventPage from './website/AdminPanelPage/DashboardPage/pages/PastEventsPage/AddPastEventPage';
import EditPastEventPage from './website/AdminPanelPage/DashboardPage/pages/PastEventsPage/EditPastEventPage';

function App() {
    const queryClient = new QueryClient();

    return (
        <QueryClientProvider client={queryClient}>
            <Routes>
                <Route path="/" element={<MainPage />} />
                <Route path="/hackathon" element={<HackathonPage />} />
                <Route path="/hackathon/registration" element={<FormPage />} />
                <Route path="/hackathon/verification" element={<VerificationPage />} />

                <Route path="/dashboard/past-events" element={<PastEventsPage />} />
                <Route path="/dashboard/past-events/add" element={<AddPastEventPage />} />
                <Route path="/dashboard/past-events/:id" element={<EditPastEventPage />} />
            </Routes>
        </QueryClientProvider>
    );
}

export default App;
