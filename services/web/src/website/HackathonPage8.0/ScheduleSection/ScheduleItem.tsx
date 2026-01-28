import React from 'react';
import { Day, ScheduleEvent } from './types';
import { TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { scheduleData } from './data';

interface ScheduleItemProps extends ScheduleEvent {
    isLast: boolean;
}

export const ScheduleItem: React.FC<ScheduleItemProps> = ({ time, event, isLast }) => (
    <div>
        <div className="flex justify-between items-center py-6 lg:py-8 px-8 lg:px-10 text-white">
            <span className="text-sm sm:text-base lg:text-xl font-oxanium break-words max-w-[65%]">{event}</span>
            <span className="text-sm sm:text-base lg:text-xl font-oxanium font-bold">{time}</span>
        </div>
        {!isLast && (
            <div
                className="h-[2px] mx-8 lg:mx-10"
                style={{
                    background: 'rgba(255, 255, 255, 0.3)',
                    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.25)',
                }}
            />
        )}
    </div>
);

export const ScheduleHeader = () => (
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

export const ScheduleTabs: React.FC<ScheduleTabsProps> = ({ activeTab }) => (
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

export const ScheduleTable = () => (
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
