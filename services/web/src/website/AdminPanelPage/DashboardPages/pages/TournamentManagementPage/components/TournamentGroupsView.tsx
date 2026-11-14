import { useRef, useState } from 'react';
import { Helmet } from 'react-helmet';
import { Link } from 'react-router';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { Styles } from '../../../../AdminStyle';
import { useTournament } from '../TournamentProvider';
import type { TournamentGroup, TournamentTeam, WinnerSelection } from '../types';
import { TournamentGroupCard } from './TournamentGroupCard';
import { WinnerConfirmationDialog } from './WinnerConfirmationDialog';

export function TournamentGroupsView({ inactive = false }: { inactive?: boolean }) {
    const tournament = useTournament();
    const [selection, setSelection] = useState<WinnerSelection | null>(null);
    const returnFocusRef = useRef<HTMLElement | null>(null);
    const headingRef = useRef<HTMLHeadingElement>(null);
    const groups = inactive ? tournament.inactiveGroups : tournament.activeGroups;
    const disabled = tournament.isBusy || tournament.isRefreshing || tournament.isLoading || !!tournament.loadError;

    const selectWinner = (group: TournamentGroup, team: TournamentTeam) => {
        returnFocusRef.current = document.activeElement instanceof HTMLElement ? document.activeElement : null;
        tournament.clearWinnerError();
        setSelection({ group, team });
    };
    const confirmWinner = async () => {
        if (selection && (await tournament.declareWinner(selection))) setSelection(null);
    };

    return (
        <>
            <Helmet>
                <title>{inactive ? 'Past Tournament Groups' : 'Tournament Management'} - The Hub AUBG</title>
            </Helmet>
            <Button asChild variant="ghost" className={cn('mb-6', Styles.glass.ghostButton)}>
                <Link to={inactive ? '..' : '/admin/dashboard'} relative="path">
                    <span aria-hidden="true">←</span>
                    {inactive ? 'Back to active groups' : 'Back to dashboard'}
                </Link>
            </Button>
            <div className="mb-8 flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
                <div>
                    <h1 className={cn('text-3xl sm:text-4xl', Styles.text.title)}>
                        {inactive ? 'Past groups' : 'Tournament management'}
                    </h1>
                    <p className={Styles.text.subtitle}>
                        {inactive
                            ? 'Review completed matches and their winners.'
                            : 'Generate the bracket and declare match winners.'}
                    </p>
                </div>
                <div className="flex flex-col gap-3 sm:flex-row">
                    {!inactive && (
                        <>
                            <Button asChild variant="outline" className={Styles.actions.secondaryButton}>
                                <Link to="past">Past groups</Link>
                            </Button>
                            <Button
                                type="button"
                                onClick={tournament.generateBracket}
                                disabled={disabled || tournament.hasGenerated}
                                className={cn('bg-[#00B2FF] hover:bg-[#0096D6]', Styles.actions.primaryButton)}
                            >
                                {tournament.isGenerating ? 'Generating…' : 'Generate bracket'}
                            </Button>
                        </>
                    )}
                    <Button
                        type="button"
                        variant="outline"
                        onClick={tournament.refresh}
                        disabled={tournament.isBusy || tournament.isRefreshing}
                        className={Styles.actions.secondaryButton}
                    >
                        {tournament.isRefreshing ? 'Refreshing…' : 'Refresh groups'}
                    </Button>
                </div>
            </div>

            <p role="status" className="mb-4 min-h-6 text-sm text-cyan-300">
                {tournament.message}
            </p>
            {tournament.loadError && (
                <div role="alert" className="mb-6 rounded-xl border border-red-300/30 bg-red-400/10 p-4 text-red-100">
                    <p>Could not load tournament groups.</p>
                    <div className="mt-3 flex flex-wrap gap-3">
                        <Button
                            type="button"
                            onClick={tournament.refresh}
                            disabled={tournament.isRefreshing}
                            variant="outline"
                            className={Styles.actions.secondaryButton}
                        >
                            Retry
                        </Button>
                    </div>
                </div>
            )}
            {!inactive && tournament.generateError && (
                <p role="alert" className="mb-6 rounded-xl border border-red-300/30 p-4 text-red-100">
                    Could not generate the bracket. Refresh groups and try again.
                </p>
            )}

            <section aria-labelledby="groups-heading" aria-busy={tournament.isRefreshing || tournament.isLoading}>
                <h2
                    ref={headingRef}
                    tabIndex={-1}
                    id="groups-heading"
                    className="mb-5 text-2xl font-semibold text-white"
                >
                    {inactive ? 'Inactive groups' : 'Active groups'}
                </h2>
                {tournament.isLoading ? (
                    <p className="rounded-xl border border-white/10 p-8 text-blue-100/70">Loading groups…</p>
                ) : groups.length > 0 ? (
                    <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
                        {groups.map((group) => (
                            <TournamentGroupCard
                                key={group.id}
                                group={group}
                                disabled={disabled}
                                onDeclareWinner={inactive ? undefined : (_, team) => selectWinner(group, team)}
                            />
                        ))}
                    </div>
                ) : (
                    !tournament.loadError && (
                        <Card className={cn('border-dashed p-8 text-center sm:p-12', Styles.glass.card)}>
                            <p className="text-blue-100/70">
                                {inactive
                                    ? 'No completed matches yet.'
                                    : tournament.hasGenerated
                                      ? 'No active groups. Check past groups for completed matches.'
                                      : 'No active groups yet. Generate a bracket to get started.'}
                            </p>
                        </Card>
                    )
                )}
            </section>
            <WinnerConfirmationDialog
                selection={selection}
                isPending={tournament.isSavingWinner}
                error={tournament.winnerError}
                onCancel={() => setSelection(null)}
                onReturnFocus={() => {
                    const target = returnFocusRef.current;
                    if (target?.isConnected && !(target instanceof HTMLButtonElement && target.disabled))
                        target.focus();
                    else headingRef.current?.focus();
                }}
                onConfirm={() => {
                    void confirmWinner();
                }}
            />
        </>
    );
}
