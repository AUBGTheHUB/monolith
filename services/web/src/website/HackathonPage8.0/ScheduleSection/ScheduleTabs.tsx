import { TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Day } from './scheduleConfig';
import React from 'react';

interface ScheduleTabsProps {
    activeTab: Day;
}

export const ScheduleTabs: React.FC<ScheduleTabsProps> = ({ activeTab }) => (
    <TabsList className="mb-12 h-auto p-0 gap-4 bg-transparent flex flex-wrap justify-start w-full">
        <div
            className="relative p-[2px] rounded-xl"
            style={{
                background: 'linear-gradient(135deg, #B91C1C 0%, #DC2626 100%)',
            }}
        >
            <TabsTrigger
                value="Friday"
                className="px-6 lg:px-8 py-2 rounded-xl font-oxanium text-sm sm:text-base lg:text-xl font-semibold transition-all border-0"
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
            className="relative p-[2px] rounded-xl"
            style={{
                background: 'linear-gradient(135deg, #DC2626 0%, #F97316 100%)',
            }}
        >
            <TabsTrigger
                value="Saturday"
                className="px-6 lg:px-8 py-2 rounded-xl font-oxanium text-sm sm:text-base lg:text-xl font-semibold transition-all border-0"
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
            className="relative p-[2px] rounded-xl"
            style={{
                background: 'linear-gradient(135deg, #F97316 0%, #FB923C 100%)',
            }}
        >
            <TabsTrigger
                value="Sunday"
                className="px-6 lg:px-8 py-2 rounded-xl font-oxanium text-sm sm:text-base lg:text-xl font-semibold transition-all border-0"
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
