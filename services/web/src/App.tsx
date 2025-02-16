import { Route, Routes } from 'react-router';
import { QueryClient, QueryClientProvider, useQuery } from '@tanstack/react-query';
import { OldAppPage } from './website/OldAppPage/OldAppPage';
import { MainPage } from './website/MainPage/MainPage';
import { HackathonPage } from './website/HackathonPage/HackathonPage';
import { fetchFeatureSwitches } from './website/constants';

function FeatureSwitchesProvider() {
    const { data: apiFeatureSwitches } = useQuery({
        queryKey: ['feature-switches'],
        queryFn: fetchFeatureSwitches,
    });

    console.log('Feature Switches:', apiFeatureSwitches);
}

function App() {
    const queryClient = new QueryClient();

    FeatureSwitchesProvider();

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
