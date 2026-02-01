import { VerticalBar } from '@/components/ui/verticalBar';
import { useState } from 'react';
import { ScheduleHeader, ScheduleTable, ScheduleTabs } from './ScheduleItem';
import { Tabs } from '@radix-ui/react-tabs';
import { Day } from './types';

export const ScheduleSection = () => {
    const [activeTab, setActiveTab] = useState<Day>('Friday');

    return (
        <section
            className="relative w-full min-h-screen flex flex-col items-center overflow-x-hidden pt-8 md:pt-16 lg:pt-24 pb-8 md:pb-12 lg:pb-16 bg-white"
            id="schedule"
        >
            <div className="absolute inset-0 z-50 pointer-events-none">
                <VerticalBar isRight={false} isBlack={true} />
                <VerticalBar isRight={true} isBlack={true} />
            </div>

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

            <div className="relative z-10 w-full max-w-[100vw] px-4 md:px-8">
                <div className="mb-[2rem] md:mb-[3rem] lg:mb-[4.125rem]">
                    <ScheduleHeader />
                </div>

                <div className="md:pl-8 lg:pl-16 xl:pl-28 md:pr-8 lg:pr-16 xl:pr-24">
                    <Tabs
                        value={activeTab}
                        onValueChange={(value: string) => setActiveTab(value as Day)}
                        className="w-full"
                    >
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
