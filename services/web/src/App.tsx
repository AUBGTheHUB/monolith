import { Route, Routes } from 'react-router';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { OldAppPage } from './website/OldAppPage/OldAppPage';
import { MainPage } from './website/MainPage/MainPage';
import { HackathonPage } from './website/HackathonPage/HackathonPage';
import { useFetchFeatureSwitches } from './config';
import { VerificationPage } from './website/VerificationPage/VerificationPage';

function App() {
    const queryClient = new QueryClient();

    return (
        <QueryClientProvider client={queryClient}>
            <Routes>
                <Route path="/old" element={<OldAppPage />} />
                <Route path="/" element={<MainPage />} />
                <Route path="/hackathon" element={<HackathonPage />} />
                <Route path="/hackathon/verification" element={<VerificationPage />} />
            </Routes>
        </QueryClientProvider>
    );
}

useFetchFeatureSwitches();

export default App;
