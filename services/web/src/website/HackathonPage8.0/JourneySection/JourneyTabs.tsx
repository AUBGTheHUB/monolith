import React from 'react';
import { TabsList, TabsTrigger } from '@/components/ui/tabs';

type JourneyTab = 'start' | 'gather' | 'hack' | 'finish';

export type JourneyTabEntry = {
    value: JourneyTab;
    label: string;
};

type Props = {
    activeTab: JourneyTab;
    entries: JourneyTabEntry[];
};

const stylesByValue: Record<JourneyTab, { wrapperBg: string; inactiveBg: string; activeTextGradient: string }> = {
    start: {
        wrapperBg: 'linear-gradient(135deg, #B91C1C 0%, #DC2626 100%)',
        inactiveBg: 'linear-gradient(135deg, #B91C1C 0%, #DC2626 100%)',
        activeTextGradient: 'linear-gradient(180deg, #DC2626 0%, #B91C1C 100%)',
    },
    gather: {
        wrapperBg: 'linear-gradient(135deg, #DC2626 0%, #F97316 100%)',
        inactiveBg: 'linear-gradient(135deg, #DC2626 0%, #F97316 100%)',
        activeTextGradient: 'linear-gradient(180deg, #F97316 0%, #DC2626 100%)',
    },
    hack: {
        wrapperBg: 'linear-gradient(135deg, #DC2626 0%, #F97316 100%)',
        inactiveBg: 'linear-gradient(135deg, #DC2626 0%, #F97316 100%)',
        activeTextGradient: 'linear-gradient(180deg, #F97316 0%, #DC2626 100%)',
    },
    finish: {
        wrapperBg: 'linear-gradient(135deg, #F97316 0%, #FB923C 100%)',
        inactiveBg: 'linear-gradient(135deg, #F97316 0%, #FB923C 100%)',
        activeTextGradient: 'linear-gradient(180deg, #FB923C 0%, #F97316 100%)',
    },
};

export const JourneyTabs: React.FC<Props> = ({ activeTab, entries }) => {
    return (
        <TabsList
            className={[
                // MOBILE: 2x2, SM+: 4-column — always fills the full container width
                'grid grid-cols-2 sm:grid-cols-4 gap-3 w-full bg-transparent p-0',
                'md:gap-[1rem] xl:gap-[1.625rem]',
            ].join(' ')}
        >
            {entries.map((entry) => {
                const s = stylesByValue[entry.value];
                const isActive = activeTab === entry.value;

                return (
                    <div
                        key={entry.value}
                        className="relative w-full p-[3px] md:p-[3.5px] xl:p-[4px] rounded-[0.75rem]"
                        style={{ background: s.wrapperBg }}
                    >
                        <TabsTrigger
                            value={entry.value}
                            className={[
                                'rounded-[calc(0.75rem-3px)] md:rounded-[calc(0.75rem-3.5px)] xl:rounded-[calc(0.75rem-4px)]',
                                'font-oxanium font-semibold border-0 relative',
                                'w-full h-[2.25rem] sm:h-[2rem] md:h-[2.5rem] xl:h-[3rem]',
                                'flex items-center justify-center',
                                'text-[clamp(16px,2.5vw,22px)]',
                            ].join(' ')}
                            style={
                                isActive
                                    ? { backgroundColor: '#FFFDF5' }
                                    : { background: s.inactiveBg, color: '#FFFDF5' }
                            }
                        >
                            <span
                                style={
                                    isActive
                                        ? {
                                              background: s.activeTextGradient,
                                              WebkitBackgroundClip: 'text',
                                              WebkitTextFillColor: 'transparent',
                                              backgroundClip: 'text',
                                          }
                                        : {}
                                }
                            >
                                {entry.label}
                            </span>
                        </TabsTrigger>
                    </div>
                );
            })}
        </TabsList>
    );
};
