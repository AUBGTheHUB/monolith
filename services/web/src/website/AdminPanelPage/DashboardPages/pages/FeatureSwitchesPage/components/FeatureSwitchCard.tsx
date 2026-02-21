import { Card } from '@/components/ui/card.tsx';
import { Button } from '@/components/ui/button.tsx';
import { cn } from '@/lib/utils.ts';

export type FSCardProps = {
    name: string;
    currentState: boolean;
    onToggle: () => void;

    // Optional labels so the page can control wording (and reuse messages.tsx)
    toggleOnLabel?: string; // when currently ON (button turns it OFF)
    toggleOffLabel?: string; // when currently OFF (button turns it ON)
    statusOnLabel?: string;
    statusOffLabel?: string;

    className?: string;
};

export default function FeatureSwitchCard({
    name,
    currentState,
    onToggle,
    toggleOnLabel = 'Turn off',
    toggleOffLabel = 'Turn on',
    statusOnLabel = 'Enabled',
    statusOffLabel = 'Disabled',
    className,
}: FSCardProps) {
    return (
        <Card className={cn('p-8', className)}>
            <div className="flex flex-col gap-6">
                <div>
                    <div className="flex items-start justify-between gap-4">
                        <h3 className="text-2xl font-semibold text-white">{name}</h3>

                        <span
                            className={cn(
                                'shrink-0 rounded-full px-3 py-1 text-xs font-medium border',
                                currentState
                                    ? 'bg-white/10 text-white border-white/15'
                                    : 'bg-black/10 text-white/70 border-white/10',
                            )}
                        >
                            {currentState ? statusOnLabel : statusOffLabel}
                        </span>
                    </div>

                    <p className="mt-2 text-sm text-white/70">
                        {currentState ? 'This feature is currently active.' : 'This feature is currently inactive.'}
                    </p>
                </div>

                <Button
                    variant="outline"
                    className="w-full bg-white/5 border-white/10 text-white hover:bg-white/20 hover:text-white transition-all"
                    onClick={onToggle}
                >
                    {currentState ? toggleOnLabel : toggleOffLabel}
                </Button>
            </div>
        </Card>
    );
}
