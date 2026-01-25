import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import { useState } from 'react';

type Day = 'Friday' | 'Saturday' | 'Sunday';

export const ScheduleSection = () => {
    const [activeTab, setActiveTab] = useState<Day>('Friday');

    return (
        <section className="relative w-full min-h-screen flex flex-col items-center pt-32 pb-20 bg-white" id="schedule">
            <div className="absolute left-4 lg:left-8 xl:left-16 top-0 bottom-0 w-[4px] lg:w-[6px] xl:w-[8px] bg-black z-20"></div>
            <div className="absolute right-4 lg:right-8 xl:right-16 top-0 bottom-0 w-[4px] lg:w-[6px] xl:w-[8px] bg-black z-20"></div>

            <img
                src="/ScheduleSection/left-background.png"
                alt=""
                className="absolute left-0 bottom-0 h-2/3 w-auto object-cover pointer-events-none opacity-60"
            />
            <img
                src="/ScheduleSection/right-background.png"
                alt=""
                className="absolute right-0 bottom-0 h-2/3 w-auto object-cover pointer-events-none opacity-60"
            />

            <div className="relative z-10 w-full max-w-[100vw]">
                <div
                    className="flex items-center gap-4 lg:gap-6 mb-32 bg-white border-2 border-black rounded-r-3xl px-6 lg:px-8 py-6 -ml-8 mr-16 lg:mr-24 xl:mr-40"
                    style={{
                        boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)',
                    }}
                >
                    <div className="ml-16 lg:ml-28 xl:ml-40 flex items-center gap-4 lg:gap-6">
                        <img
                            src="/ScheduleSection/logo.png"
                            alt="HackAUBG Logo"
                            className="w-12 h-12 lg:w-16 lg:h-16 object-contain"
                        />
                        <h2 className="text-black text-3xl lg:text-4xl xl:text-5xl font-orbitron font-normal tracking-[0.3em]">
                            SCHEDULE
                        </h2>
                    </div>
                </div>

                <div className="pl-16 lg:pl-28 xl:pl-40 pr-16 lg:pr-24 xl:pr-40">
                    <Tabs
                        value={activeTab}
                        onValueChange={(value: string) => setActiveTab(value as Day)}
                        className="w-full"
                    >
                        <TabsList className="mb-12 h-auto p-0 gap-4 bg-transparent">
                            <div
                                className="relative p-[2px] rounded-xl"
                                style={{
                                    background: 'linear-gradient(135deg, #B91C1C 0%, #DC2626 100%)',
                                }}
                            >
                                <TabsTrigger
                                    value="Friday"
                                    className="px-6 lg:px-8 py-2 rounded-xl font-oxanium text-lg lg:text-xl font-semibold transition-all border-0"
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
                                    className="px-6 lg:px-8 py-2 rounded-xl font-oxanium text-lg lg:text-xl font-semibold transition-all border-0"
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
                                    className="px-6 lg:px-8 py-2 rounded-xl font-oxanium text-lg lg:text-xl font-semibold transition-all border-0"
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

                        {(['Friday', 'Saturday', 'Sunday'] as Day[]).map((day) => (
                            <TabsContent key={day} value={day}>
                                <div
                                    className="rounded-3xl py-1 lg:py-2 w-full"
                                    style={{
                                        background:
                                            'linear-gradient(135deg, #B91C1C 0%, #DC2626 30%, #F97316 70%, #FB923C 100%)',
                                    }}
                                >
                                    <div>
                                        {scheduleData[day].map((event, index) => (
                                            <div key={index}>
                                                <div className="flex justify-between items-center py-6 lg:py-8 px-8 lg:px-10 text-white">
                                                    <span className="text-lg lg:text-xl font-oxanium">
                                                        {event.event}
                                                    </span>
                                                    <span className="text-lg lg:text-xl font-oxanium font-bold">
                                                        {event.time}
                                                    </span>
                                                </div>
                                                {index !== scheduleData[day].length - 1 && (
                                                    <div
                                                        className="h-[2px] mx-8 lg:mx-10"
                                                        style={{
                                                            background: 'rgba(255, 255, 255, 0.3)',
                                                            boxShadow: '0 4px 6px rgba(0, 0, 0, 0.25)',
                                                        }}
                                                    />
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </TabsContent>
                        ))}
                    </Tabs>
                </div>
            </div>
        </section>
    );
};

const scheduleData: Record<Day, Array<{ time: string; event: string }>> = {
    Friday: [
        { time: '16:00', event: 'Registration' },
        { time: '18:00', event: 'Opening Ceremony' },
        { time: '19:00', event: 'Dinner and Brainstorming' },
        { time: '21:00', event: 'Idea Pitching' },
        { time: '21:30', event: 'Start Coding' },
    ],
    Saturday: [
        { time: '09:00', event: 'Breakfast' },
        { time: '10:00', event: 'Idea Pitching to Mentors' },
        { time: '11:00', event: 'Mentors Presentations' },
        { time: '11:30', event: 'Mentorship and HR Booths' },
        { time: '13:00', event: 'Lunch' },
        { time: '14:00', event: 'Mentorship and Coding' },
        { time: '17:00', event: 'Mentorship Ends' },
        { time: '19:30', event: 'Dinner and Coding' },
    ],
    Sunday: [
        { time: '10:00', event: 'Breakfast and Coding' },
        { time: '12:00', event: 'Submission Deadline' },
        { time: '13:00', event: 'Presentations Begin' },
        { time: '14:00', event: 'Lunch' },
        { time: '19:30', event: 'Award Ceremony' },
    ],
};
