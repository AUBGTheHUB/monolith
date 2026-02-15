import React from 'react';
import { TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ScheduleTabsProps } from './types';

export const ScheduleTabs: React.FC<ScheduleTabsProps> = ({ activeTab }) => (
    <TabsList className="mb-[1.5rem] h-auto p-0 gap-[0.75rem] md:gap-[1rem] lg:gap-[1.625rem] bg-transparent flex flex-wrap justify-center md:justify-start w-full">
        <div
            className="relative p-[3px] md:p-[3.5px] lg:p-[4px] rounded-[0.75rem]"
            style={{
                background: 'linear-gradient(135deg, #B91C1C 0%, #DC2626 100%)',
            }}
        >
            <TabsTrigger
                value="Friday"
                className="rounded-[calc(0.75rem-3px)] md:rounded-[calc(0.75rem-3.5px)] lg:rounded-[calc(0.75rem-4px)] font-oxanium text-[1rem] md:text-[1.4rem] lg:text-[1.6rem] font-semibold border-0 relative w-[5.5rem] md:w-[7rem] lg:w-[10rem] h-[2rem] lg:h-[3rem] flex items-center justify-center"
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
            className="relative p-[3px] md:p-[3.5px] lg:p-[4px] rounded-[0.75rem]"
            style={{
                background: 'linear-gradient(135deg, #DC2626 0%, #F97316 100%)',
            }}
        >
            <TabsTrigger
                value="Saturday"
                className="rounded-[calc(0.75rem-3px)] md:rounded-[calc(0.75rem-3.5px)] lg:rounded-[calc(0.75rem-4px)] font-oxanium text-[1rem] md:text-[1.4rem] lg:text-[1.6rem] font-semibold border-0 relative w-[5.5rem] md:w-[7rem] lg:w-[10rem] h-[2rem] lg:h-[3rem] flex items-center justify-center"
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
            className="relative p-[3px] md:p-[3.5px] lg:p-[4px] rounded-[0.75rem]"
            style={{
                background: 'linear-gradient(135deg, #F97316 0%, #FB923C 100%)',
            }}
        >
            <TabsTrigger
                value="Sunday"
                className="rounded-[calc(0.75rem-3px)] md:rounded-[calc(0.75rem-3.5px)] lg:rounded-[calc(0.75rem-4px)] font-oxanium text-[1rem] md:text-[1.4rem] lg:text-[1.6rem] font-semibold border-0 relative w-[5.5rem] md:w-[7rem] lg:w-[10rem] h-[2rem] lg:h-[3rem] flex items-center justify-center"
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
