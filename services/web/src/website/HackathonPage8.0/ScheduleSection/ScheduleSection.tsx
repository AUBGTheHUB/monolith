import { useState } from 'react';
import { Tabs } from '@radix-ui/react-tabs';
import { Day } from './types';
import { ScheduleHeader } from './ScheduleHeader';
import { ScheduleTabs } from './ScheduleTabs';
import { ScheduleTable } from './ScheduleTable';
import './style.css';

export const ScheduleSection = () => {
    const [activeTab, setActiveTab] = useState<Day>('Friday');

    const handleTabChange = (value: string) => {
        setActiveTab(value as Day);
    };

    return (
        <section
            className="relative w-full min-h-[80vh] flex flex-col items-center overflow-x-hidden py-8 md:py-16 lg:py-24 bg-[#FFFDF5]"
            id="schedule"
        >
            <img
                src="/ScheduleSection/left-background.png"
                alt=""
                className="absolute left-0 bottom-0 max-h-[50vh] md:max-h-[60vh] lg:max-h-[70vh] w-auto object-contain pointer-events-none opacity-60"
            />
            <img
                src="/ScheduleSection/right-background.png"
                alt=""
                className="absolute right-0 bottom-0 max-h-[50vh] md:max-h-[60vh] lg:max-h-[70vh] w-auto object-contain pointer-events-none opacity-60"
            />

            <div className="relative z-10 w-full grid place-items-center">
                <div className="w-full flex flex-col md:px-0 px-8 schedule-container">
                    <div className="mb-[2rem] md:mb-[3rem] lg:mb-[4.125rem]">
                        <ScheduleHeader />
                    </div>
                    <Tabs value={activeTab} onValueChange={handleTabChange} className="w-full">
                        <div className="mb-[2rem] md:mb-[2.5rem] lg:mb-[3.5rem]">
                            <ScheduleTabs activeTab={activeTab} />
                        </div>
                        <ScheduleTable />
                    </Tabs>
                </div>
            </div>
        </section>
    );
};
