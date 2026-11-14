import { Outlet } from 'react-router';
import { TournamentProvider } from '@/website/AdminPanelPage/DashboardPages/pages/TournamentManagementPage/TournamentProvider.tsx';

export function TournamentBracketLayout() {
    return (
        <TournamentProvider>
            <Outlet />
        </TournamentProvider>
    );
}
