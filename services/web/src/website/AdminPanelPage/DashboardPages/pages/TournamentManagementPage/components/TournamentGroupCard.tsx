import { Trophy } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { Styles } from '../../../../AdminStyle';
import type { TournamentGroup, TournamentTeam } from '../types';

interface TournamentGroupCardProps {
    group: TournamentGroup;
    disabled?: boolean;
    onDeclareWinner?: (groupId: string, team: TournamentTeam) => void;
}

export function TournamentGroupCard({ group, disabled = false, onDeclareWinner }: TournamentGroupCardProps) {
    const isMatchReady = group.teams.every(Boolean);
    return (
        <Card className={cn('min-w-0 rounded-2xl p-5 sm:p-6', Styles.glass.card)}>
            <div className="mb-6 flex flex-wrap items-center justify-between gap-2">
                <h3 className="text-lg font-semibold text-white">
                    Round {group.round}
                    {group.bracketNumber ? ` · Match ${group.bracketNumber}` : ''}
                </h3>
                <span className="rounded-full bg-white/10 px-3 py-1 text-xs text-blue-100">
                    {group.winnerId ? 'Completed' : isMatchReady ? 'Awaiting winner' : 'Awaiting teams'}
                </span>
            </div>

            <div className="space-y-3">
                {group.teams.map((team, index) => {
                    if (!team)
                        return (
                            <p
                                key={`pending-${index}`}
                                className="rounded-xl border border-dashed border-white/10 p-4 text-blue-100/60"
                            >
                                Awaiting team
                            </p>
                        );
                    const isWinner = team.id === group.winnerId;

                    return (
                        <div
                            key={team.id}
                            className={cn(
                                'flex flex-col gap-3 rounded-xl border p-4 sm:flex-row sm:items-center sm:justify-between',
                                isWinner ? 'border-cyan-400/40 bg-cyan-400/10' : 'border-white/10 bg-white/[0.02]',
                            )}
                        >
                            <div className="min-w-0">
                                <p className="break-words font-medium text-white">{team.name}</p>
                                {isWinner && (
                                    <span className="mt-1 flex items-center gap-1 text-sm text-cyan-300">
                                        <Trophy size={14} aria-hidden="true" /> Winner
                                    </span>
                                )}
                            </div>
                            {onDeclareWinner && (
                                <Button
                                    type="button"
                                    variant="outline"
                                    size="sm"
                                    disabled={disabled || isWinner || !isMatchReady}
                                    aria-label={`Declare ${team.name} winner of round ${group.round}`}
                                    onClick={() => onDeclareWinner(group.id, team)}
                                    className="w-full shrink-0 border-white/20 bg-white/5 text-white hover:bg-white/10 hover:text-white sm:w-auto"
                                >
                                    {isWinner ? 'Declared winner' : 'Declare winner'}
                                </Button>
                            )}
                        </div>
                    );
                })}
            </div>
        </Card>
    );
}
