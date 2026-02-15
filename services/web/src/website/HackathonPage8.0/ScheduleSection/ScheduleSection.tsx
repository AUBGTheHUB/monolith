import { VerticalBar } from '@/components/ui/verticalBar';
import { useState } from 'react';
import { Tabs } from '@radix-ui/react-tabs';
import { Day } from './types';
import { ScheduleHeader } from './ScheduleHeader';
import { ScheduleTabs } from './ScheduleTabs';
import { ScheduleTable } from './ScheduleTable';

export const ScheduleSection = () => {
    const [activeTab, setActiveTab] = useState<Day>('Friday');

    return (
        <section
            className="relative w-full min-h-[80vh] flex flex-col items-center overflow-x-hidden pt-8 md:pt-16 lg:pt-24 pb-8 md:pb-12 lg:pb-16 bg-white"
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

            <div
                className="relative z-10 w-full px-8 flex flex-col"
                style={{ maxWidth: 'clamp(40rem, 82vw, 80rem)', margin: '0 auto' }}
            >
                <div className="mb-[2rem] md:mb-[3rem] lg:mb-[4.125rem]">
                    <ScheduleHeader />
                </div>

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
        </section>
    );
};
