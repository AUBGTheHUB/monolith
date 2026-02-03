import React from 'react';
import { Day, ScheduleItemProps, ScheduleTabsProps } from './types';
import { TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { scheduleData } from './data';

export const ScheduleItem: React.FC<ScheduleItemProps> = ({ time, event, isLast }) => (
    <div className={!isLast ? 'mb-[1rem] md:mb-[1.5rem]' : ''}>
        <div className="flex justify-between items-center py-[0.75rem] md:py-[1.25rem] text-white">
            <span className="text-[0.875rem] md:text-[1.188rem] font-oxanium leading-[1.25]">{event}</span>
            <span className="text-[0.875rem] md:text-[1.188rem] font-oxanium font-bold leading-[1.25]">{time}</span>
        </div>
        {!isLast && (
            <div
                className="h-[1px]"
                style={{
                    background: '#A9B4C3',
                    boxShadow: '0 1px 2px rgba(0, 0, 0, 0.1)',
                }}
            />
        )}
    </div>
);

export const ScheduleHeader = () => (
    <div className="w-full max-w-[100vw] md:pl-8 lg:pl-16 xl:pl-28">
        <div className="flex items-center justify-center md:justify-start gap-3 md:gap-4 lg:gap-6">
            <img
                src="/ScheduleSection/logo.png"
                alt="HackAUBG Logo"
                className="w-[2.2rem] h-[1.75rem] md:w-[2.75rem] md:h-[2.2rem] lg:w-[3.5rem] lg:h-[2.8rem] object-contain"
            />
            <h2 className="text-black font-orbitron font-normal text-[1.75rem] md:text-[2.25rem] lg:text-[2.75rem] leading-[1.25] tracking-[0.2em] md:tracking-[0.25em] lg:tracking-[0.3em]">
                SCHEDULE
            </h2>
        </div>
    </div>
);

export const ScheduleTabs: React.FC<ScheduleTabsProps> = ({ activeTab }) => (
    <TabsList className="mb-[1.5rem] h-auto p-0 gap-[0.75rem] md:gap-[1rem] lg:gap-[1.625rem] bg-transparent flex flex-wrap justify-center md:justify-start w-full">
        <div
            className="relative p-[3px] md:p-[3.5px] lg:p-[4px] rounded-[0.75rem] md:rounded-[1rem] lg:rounded-[1.25rem]"
            style={{
                background: 'linear-gradient(135deg, #B91C1C 0%, #DC2626 100%)',
            }}
        >
            <TabsTrigger
                value="Friday"
                className="px-3 md:px-4 lg:px-6 py-1.5 md:py-1.5 lg:py-2 rounded-[calc(0.75rem-3px)] md:rounded-[calc(1rem-3.5px)] lg:rounded-[calc(1.25rem-4px)] font-oxanium text-[1rem] md:text-[1.25rem] lg:text-[1.5rem] font-semibold border-0 relative"
                style={
                    activeTab === 'Friday'
                        ? { backgroundColor: 'white' }
                        : {
                              background: 'linear-gradient(135deg, #B91C1C 0%, #DC2626 100%)',
                              color: 'white',
                          }
                }
            >
                <span
                    style={
                        activeTab === 'Friday'
                            ? {
                                  background: 'linear-gradient(180deg, #DC2626 0%, #B91C1C 100%)',
                                  WebkitBackgroundClip: 'text',
                                  WebkitTextFillColor: 'transparent',
                                  backgroundClip: 'text',
                              }
                            : {}
                    }
                >
                    Friday
                </span>
            </TabsTrigger>
        </div>

        <div
            className="relative p-[3px] md:p-[3.5px] lg:p-[4px] rounded-[0.75rem] md:rounded-[1rem] lg:rounded-[1.25rem]"
            style={{
                background: 'linear-gradient(135deg, #DC2626 0%, #F97316 100%)',
            }}
        >
            <TabsTrigger
                value="Saturday"
                className="px-3 md:px-4 lg:px-6 py-1.5 md:py-1.5 lg:py-2 rounded-[calc(0.75rem-3px)] md:rounded-[calc(1rem-3.5px)] lg:rounded-[calc(1.25rem-4px)] font-oxanium text-[1rem] md:text-[1.25rem] lg:text-[1.5rem] font-semibold border-0 relative"
                style={
                    activeTab === 'Saturday'
                        ? { backgroundColor: 'white' }
                        : {
                              background: 'linear-gradient(135deg, #DC2626 0%, #F97316 100%)',
                              color: 'white',
                          }
                }
            >
                <span
                    style={
                        activeTab === 'Saturday'
                            ? {
                                  background: 'linear-gradient(180deg, #F97316 0%, #DC2626 100%)',
                                  WebkitBackgroundClip: 'text',
                                  WebkitTextFillColor: 'transparent',
                                  backgroundClip: 'text',
                              }
                            : {}
                    }
                >
                    Saturday
                </span>
            </TabsTrigger>
        </div>

        <div
            className="relative p-[3px] md:p-[3.5px] lg:p-[4px] rounded-[0.75rem] md:rounded-[1rem] lg:rounded-[1.25rem]"
            style={{
                background: 'linear-gradient(135deg, #F97316 0%, #FB923C 100%)',
            }}
        >
            <TabsTrigger
                value="Sunday"
                className="px-3 md:px-4 lg:px-6 py-1.5 md:py-1.5 lg:py-2 rounded-[calc(0.75rem-3px)] md:rounded-[calc(1rem-3.5px)] lg:rounded-[calc(1.25rem-4px)] font-oxanium text-[1rem] md:text-[1.25rem] lg:text-[1.5rem] font-semibold border-0 relative"
                style={
                    activeTab === 'Sunday'
                        ? { backgroundColor: 'white' }
                        : {
                              background: 'linear-gradient(135deg, #F97316 0%, #FB923C 100%)',
                              color: 'white',
                          }
                }
            >
                <span
                    style={
                        activeTab === 'Sunday'
                            ? {
                                  background: 'linear-gradient(180deg, #FB923C 0%, #F97316 100%)',
                                  WebkitBackgroundClip: 'text',
                                  WebkitTextFillColor: 'transparent',
                                  backgroundClip: 'text',
                              }
                            : {}
                    }
                >
                    Sunday
                </span>
            </TabsTrigger>
        </div>
    </TabsList>
);

export const ScheduleTable = () => (
    <>
        {(['Friday', 'Saturday', 'Sunday'] as Day[]).map((day) => (
            <TabsContent key={day} value={day}>
                <div
                    className="rounded-[1rem] md:rounded-[1.25rem] w-full"
                    style={{
                        background: 'linear-gradient(135deg, #B91C1C 0%, #DC2626 30%, #F97316 70%, #FB923C 100%)',
                    }}
                >
                    <div className="px-[1.5rem] md:px-[2.25rem] py-[1rem] md:py-[1.313rem]">
                        {scheduleData[day].map((event, index) => (
                            <ScheduleItem
                                key={index}
                                time={event.time}
                                event={event.event}
                                isLast={index === scheduleData[day].length - 1}
                            />
                        ))}
                    </div>
                </div>
            </TabsContent>
        ))}
    </>
);
