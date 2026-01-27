import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import { useState } from 'react';
import { Day } from './Schedule.types';
import { scheduleData } from './Schedule.data';
import { ScheduleItem } from './ScheduleItem';

import React from 'react';

const ScheduleHeader = () => (
    <div
        className="flex items-center gap-4 lg:gap-6 mb-24 bg-white border-y-2 border-r-2 sm:border-2 border-black rounded-r-3xl px-6 lg:px-8 py-6 -ml-0 sm:-ml-8 mr-16 lg:mr-24 xl:mr-40"
        style={{ boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)' }}
    >
        <div className="ml-4 sm:ml-16 lg:ml-28 xl:ml-40 flex items-center gap-4 lg:gap-6">
            <img
                src="/ScheduleSection/logo.png"
                alt="HackAUBG Logo"
                className="w-10 h-10 sm:w-12 sm:h-12 lg:w-16 lg:h-16 object-contain"
            />
            <h2 className="text-black font-orbitron font-normal tracking-[0.3em] text-[clamp(1.25rem,3.5vw,3rem)]">
                SCHEDULE
            </h2>
        </div>
    </div>
);

interface ScheduleTabsProps {
    activeTab: Day;
}

const ScheduleTabs: React.FC<ScheduleTabsProps> = ({ activeTab }) => (
    <TabsList className="mb-12 h-auto p-0 gap-4 bg-transparent flex flex-wrap justify-start w-full">
        <div
            className="relative p-[2px] rounded-[14px]"
            style={{
                background: 'linear-gradient(135deg, #B91C1C 0%, #DC2626 100%)',
            }}
        >
            <TabsTrigger
                value="Friday"
                className="px-6 lg:px-8 py-2 rounded-[12px] font-oxanium text-sm sm:text-base lg:text-xl font-semibold transition-all border-0"
                style={
                    activeTab === 'Friday'
                        ? { backgroundColor: 'white', color: '#DC2626' }
                        : {
                              background: 'linear-gradient(135deg, #B91C1C 0%, #DC2626 100%)',
                              color: 'white',
                          }
                }
            >
                Friday
            </TabsTrigger>
        </div>

        <div
            className="relative p-[2px] rounded-[14px]"
            style={{
                background: 'linear-gradient(135deg, #DC2626 0%, #F97316 100%)',
            }}
        >
            <TabsTrigger
                value="Saturday"
                className="px-6 lg:px-8 py-2 rounded-[12px] font-oxanium text-sm sm:text-base lg:text-xl font-semibold transition-all border-0"
                style={
                    activeTab === 'Saturday'
                        ? { backgroundColor: 'white', color: '#DC2626' }
                        : {
                              background: 'linear-gradient(135deg, #DC2626 0%, #F97316 100%)',
                              color: 'white',
                          }
                }
            >
                Saturday
            </TabsTrigger>
        </div>

        <div
            className="relative p-[2px] rounded-[14px]"
            style={{
                background: 'linear-gradient(135deg, #F97316 0%, #FB923C 100%)',
            }}
        >
            <TabsTrigger
                value="Sunday"
                className="px-6 lg:px-8 py-2 rounded-[12px] font-oxanium text-sm sm:text-base lg:text-xl font-semibold transition-all border-0"
                style={
                    activeTab === 'Sunday'
                        ? { backgroundColor: 'white', color: '#F97316' }
                        : {
                              background: 'linear-gradient(135deg, #F97316 0%, #FB923C 100%)',
                              color: 'white',
                          }
                }
            >
                Sunday
            </TabsTrigger>
        </div>
    </TabsList>
);

const ScheduleTable = () => (
    <>
        {(['Friday', 'Saturday', 'Sunday'] as Day[]).map((day) => (
            <TabsContent key={day} value={day}>
                <div
                    className="rounded-3xl py-1 lg:py-2 w-full"
                    style={{
                        background: 'linear-gradient(135deg, #B91C1C 0%, #DC2626 30%, #F97316 70%, #FB923C 100%)',
                    }}
                >
                    <div>
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

export const ScheduleSection = () => {
    const [activeTab, setActiveTab] = useState<Day>('Friday');

    return (
        <section
            className="relative w-full min-h-screen flex flex-col items-center overflow-x-hidden pt-16 sm:pt-24 lg:pt-32 pb-12 sm:pb-16 lg:pb-20 bg-white"
            id="schedule"
        >
            <div className="absolute left-4 lg:left-8 xl:left-16 top-0 bottom-0 w-[2px] sm:w-[4px] lg:w-[6px] xl:w-[8px] bg-black z-20"></div>
            <div className="absolute right-4 lg:right-8 xl:right-16 top-0 bottom-0 w-[2px] sm:w-[4px] lg:w-[6px] xl:w-[8px] bg-black z-20"></div>

            <img
                src="/ScheduleSection/left-background.png"
                alt=""
                className="absolute left-0 bottom-0 max-h-[70vh] w-auto object-contain pointer-events-none opacity-60"
            />
            <img
                src="/ScheduleSection/right-background.png"
                alt=""
                className="absolute right-0 bottom-0 max-h-[70vh] w-auto object-contain pointer-events-none opacity-60"
            />

            <div className="relative z-10 w-full max-w-[100vw]">
                <ScheduleHeader />

                <div className="pl-16 lg:pl-28 xl:pl-40 pr-16 lg:pr-24 xl:pr-40">
                    <Tabs
                        value={activeTab}
                        onValueChange={(value: string) => setActiveTab(value as Day)}
                        className="w-full"
                    >
                        <ScheduleTabs activeTab={activeTab} />
                        <ScheduleTable />
                    </Tabs>
                </div>
            </div>
        </section>
    );
};
