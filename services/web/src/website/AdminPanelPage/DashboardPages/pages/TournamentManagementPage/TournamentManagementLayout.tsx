import { Outlet } from 'react-router';
import { cn } from '@/lib/utils';
import { Styles } from '../../../AdminStyle';
import { TournamentProvider } from './TournamentProvider';

export function TournamentManagementLayout() {
    return (
        <TournamentProvider>
            <main className={cn('min-h-screen p-4 md:p-8', Styles.backgrounds.primaryGradient)}>
                <div className="mx-auto max-w-7xl">
                    <Outlet />
                </div>
            </main>
        </TournamentProvider>
    );
}
