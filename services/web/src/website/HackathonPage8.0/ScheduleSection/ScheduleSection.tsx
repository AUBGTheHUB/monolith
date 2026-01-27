import { Tabs } from '@/components/ui/tabs';
import { useState } from 'react';
import { Day } from './scheduleConfig';
import { ScheduleHeader } from './ScheduleHeader';
import { ScheduleTabs } from './ScheduleTabs';
import { ScheduleTable } from './ScheduleTable';

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
