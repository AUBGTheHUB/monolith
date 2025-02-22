import { Route, Routes } from 'react-router';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { OldAppPage } from './website/OldAppPage/OldAppPage';
import { MainPage } from './website/MainPage/MainPage';
import { HackathonPage } from './website/HackathonPage/HackathonPage';
import { useFetchFeatureSwitches } from './config';
import { FormPage } from './website/RegistrationFormPage/RegistrationFormPage';

function App() {
    const queryClient = new QueryClient();

    return (
        <QueryClientProvider client={queryClient}>
            <Routes>
                <Route path="/old" element={<OldAppPage />} />
                <Route path="/" element={<MainPage />} />
                <Route path="/hackathon" element={<HackathonPage />} />
                <Route path="/hackathon/registration" element={<FormPage />} />
            </Routes>
        </QueryClientProvider>
    );
}

useFetchFeatureSwitches();

export default App;
