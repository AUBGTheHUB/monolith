import { createContext, useContext, type ReactNode } from 'react';
import { useQuery } from '@tanstack/react-query';
import { tournamentApi } from '@/website/TournamentPages/TournamentBracket/api.ts';

const queryKey = ['tournament-bracket'];

function useTournamentBracketState() {
    const groupsQuery = useQuery({
        queryKey: [...queryKey, 'active'],
        queryFn: tournamentApi.getGroups,
        retry: false,
        refetchOnWindowFocus: false,
    });

    const isLoading = groupsQuery.isPending;
    const isRefreshing = groupsQuery.isFetching;
    const loadError = groupsQuery.error;

    return {
        isLoading,
        isRefreshing,
        loadError,
    };
}

const TournamentBracketContext = createContext<ReturnType<typeof useTournamentBracketState> | null>(null);

export function TournamentBracketProvider({ children }: { children: ReactNode }) {
    const state = useTournamentBracketState();
    return <TournamentBracketContext.Provider value={state}>{children}</TournamentBracketContext.Provider>;
}

export function useTournamentBracket() {
    const context = useContext(TournamentBracketContext);
    if (!context) throw new Error('Tournament pages must be wrapped in TournamentProvider.');
    return context;
}
