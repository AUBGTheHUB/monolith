import { Route, Routes } from 'react-router';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { OldAppPage } from './website/OldAppPage/OldAppPage';
import { MainPage } from './website/MainPage/MainPage';
import { HackathonPage } from './website/HackathonPage/HackathonPage';
import { useFetchFeatureSwitches } from './website/constants';
import { API_URL } from './website/constants';

function App() {
    const queryClient = new QueryClient();

    useFetchFeatureSwitches(); // Fetch feature switches and update the array
    console.log(API_URL);
    return (
        <QueryClientProvider client={queryClient}>
            <Routes>
                <Route path="/old" element={<OldAppPage />} />
                <Route path="/" element={<MainPage />} />
                <Route path="/hackathon" element={<HackathonPage />} />
            </Routes>
        </QueryClientProvider>
    );
}

export default App;
