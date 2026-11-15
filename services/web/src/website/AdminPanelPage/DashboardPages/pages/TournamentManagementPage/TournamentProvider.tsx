import { createContext, useContext, useRef, useState, type ReactNode } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { tournamentApi } from './api';
import type { WinnerSelection } from './types';

const queryKey = ['tournament-management'];

function useTournamentState() {
    const queryClient = useQueryClient();
    const [message, setMessage] = useState('');
    const mutationLock = useRef(false);

    const activeQuery = useQuery({
        queryKey: [...queryKey, 'active'],
        queryFn: tournamentApi.getActive,
        retry: false,
        refetchOnWindowFocus: false,
    });
    const inactiveQuery = useQuery({
        queryKey: [...queryKey, 'inactive'],
        queryFn: tournamentApi.getInactive,
        retry: false,
        refetchOnWindowFocus: false,
    });

    const refreshAfterChange = () => queryClient.invalidateQueries({ queryKey });

    const generateMutation = useMutation({
        mutationFn: tournamentApi.generateBracket,
        onSuccess: async () => {
            setMessage('Bracket generated.');
            await refreshAfterChange();
        },
        // lost response may still have created groups -> recheck before allowing another generation.
        onError: refreshAfterChange,
    });

    const winnerMutation = useMutation({
        mutationFn: async ({ group, team }: WinnerSelection) => {
            if (!group.teams.every(Boolean) || !group.teams.some((entry) => entry?.id === team.id)) {
                throw new Error('Both teams must be known before declaring a winner.');
            }
            await tournamentApi.declareWinner(group.id, team);
        },
        onSuccess: async (_, { team }) => {
            setMessage(`${team.name} declared the winner.`);
            await refreshAfterChange();
        },
    });

    const activeGroups = activeQuery.data ?? [];
    const inactiveGroups = inactiveQuery.data ?? [];
    const isLoading = activeQuery.isPending || inactiveQuery.isPending;
    const isRefreshing = activeQuery.isFetching || inactiveQuery.isFetching;
    const loadError = activeQuery.error ?? inactiveQuery.error;
    const isBusy = generateMutation.isPending || winnerMutation.isPending;
    const hasGenerated = activeGroups.length > 0 || inactiveGroups.length > 0;

    return {
        activeGroups,
        inactiveGroups,
        message,
        isLoading,
        isRefreshing,
        loadError,
        isBusy,
        isGenerating: generateMutation.isPending,
        isSavingWinner: winnerMutation.isPending,
        generateError: generateMutation.error,
        winnerError: winnerMutation.error,
        hasGenerated,
        refresh: () => {
            void activeQuery.refetch();
            void inactiveQuery.refetch();
        },
        generateBracket: () => {
            if (mutationLock.current || isBusy || isRefreshing || loadError || isLoading || hasGenerated) return;
            mutationLock.current = true;
            setMessage('');
            generateMutation.mutate(undefined, {
                onSettled: () => {
                    mutationLock.current = false;
                },
            });
        },
        clearWinnerError: winnerMutation.reset,
        declareWinner: async (selection: WinnerSelection) => {
            if (mutationLock.current || isBusy || isRefreshing || loadError || isLoading) return false;
            mutationLock.current = true;
            setMessage('');
            try {
                await winnerMutation.mutateAsync(selection);
                return true;
            } catch {
                return false;
            } finally {
                mutationLock.current = false;
            }
        },
    };
}

const TournamentContext = createContext<ReturnType<typeof useTournamentState> | null>(null);

export function TournamentProvider({ children }: { children: ReactNode }) {
    const state = useTournamentState();
    return <TournamentContext.Provider value={state}>{children}</TournamentContext.Provider>;
}

export function useTournament() {
    const context = useContext(TournamentContext);
    if (!context) throw new Error('Tournament pages must be wrapped in TournamentProvider.');
    return context;
}
