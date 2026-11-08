import { useQuery } from '@tanstack/react-query';
import { Helmet } from 'react-helmet';
import { apiClient } from '@/services/apiClient';
import { BracketRound } from './components/BracketRound';
import { ChampionBox } from './components/ChampionBox';
import { MobileBracket } from './components/MobileBracket';
import { TOTAL_ROUNDS, findGroup, type BackendGroup } from './types/bracket';

export default function TournamentBracket() {
    const {
        data: groups = [],
        isLoading,
        isError,
    } = useQuery({
        queryKey: ['tournament', 'groups'],
        queryFn: () => apiClient.get<{ groups: BackendGroup[] }>('/groups'),
        select: (res) => res.groups,
    });

    const rounds = Array.from({ length: TOTAL_ROUNDS }, (_, i) => i + 1);

    return (
        <div className="relative">
            <Helmet>
                <title>Tournament Bracket</title>
            </Helmet>

            {isLoading && <p className="absolute left-1/2 top-4 z-10 -translate-x-1/2 text-white">Loading bracket…</p>}
            {isError && (
                <p className="absolute left-1/2 top-4 z-10 -translate-x-1/2 text-white">Failed to load bracket.</p>
            )}

            <div className="xl:hidden">
                <MobileBracket groups={groups} />
            </div>

            <div className="hidden h-screen min-h-[44rem] bg-[linear-gradient(90deg,#1B2A2F_0%,#0A1C30_30%,#081A2E_65%,#1F3F5C_100%)] text-white [--gap:4rem] [--head:10rem] xl:flex 2xl:[--gap:6rem]">
                <div className="flex flex-1 gap-[var(--gap)] py-12 pl-12 pr-[var(--gap)]">
                    {rounds.map((r) => (
                        <BracketRound key={r} round={r} groups={groups} />
                    ))}
                </div>
                <ChampionBox final={findGroup(groups, TOTAL_ROUNDS, 1)} />
            </div>
        </div>
    );
}
