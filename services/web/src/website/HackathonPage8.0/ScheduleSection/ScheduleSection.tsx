import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import { useState } from 'react';

type Day = 'Friday' | 'Saturday' | 'Sunday';

export const ScheduleSection = () => {
    const [activeTab, setActiveTab] = useState<Day>('Friday');

    return (
        <section
            className="relative w-full min-h-screen flex flex-col items-center py-20 bg-white overflow-hidden"
            id="schedule"
        >
            {/* Vertical border lines */}
            <div className="absolute left-4 lg:left-8 xl:left-16 top-0 bottom-0 w-[4px] lg:w-[6px] xl:w-[8px] bg-black z-20"></div>
            <div className="absolute right-4 lg:right-8 xl:right-16 top-0 bottom-0 w-[4px] lg:w-[6px] xl:w-[8px] bg-black z-20"></div>

            {/* Background Images */}
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

            <div className="relative z-10 w-full">
                {/* Header with Logo and Title */}
                <div
                    className="flex items-center gap-6 mb-16 bg-white border-2 border-black rounded-r-3xl px-8 py-6 -ml-8 mr-24 lg:mr-32 xl:mr-40"
                    style={{
                        boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)',
                    }}
                >
                    <div className="ml-32 lg:ml-40 xl:ml-48 flex items-center gap-6">
                        <img src="/ScheduleSection/logo.png" alt="HackAUBG Logo" className="w-16 h-16 object-contain" />
                        <h2 className="text-black text-5xl font-orbitron font-normal tracking-[0.3em]">SCHEDULE</h2>
                    </div>
                </div>

                {/* Buttons and table aligned with title text */}
                <div className="px-24 lg:px-32 xl:px-40">
                    <Tabs value={activeTab} onValueChange={(value) => setActiveTab(value as Day)} className="w-full">
                        <TabsList className="mb-12 h-auto p-0 gap-4 bg-transparent">
                            <div
                                className="relative p-[2px] rounded-xl"
                                style={{
                                    background: 'linear-gradient(135deg, #B91C1C 0%, #DC2626 100%)',
                                }}
                            >
                                <TabsTrigger
                                    value="Friday"
                                    className="px-8 py-2 rounded-xl font-oxanium text-lg font-semibold transition-all border-0"
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
                                    className="px-8 py-2 rounded-xl font-oxanium text-lg font-semibold transition-all border-0"
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
                                    className="px-8 py-2 rounded-xl font-oxanium text-lg font-semibold transition-all border-0"
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
                                    className="rounded-3xl p-8 w-full max-w-5xl"
                                    style={{
                                        background:
                                            'linear-gradient(135deg, #B91C1C 0%, #DC2626 30%, #F97316 70%, #FB923C 100%)',
                                    }}
                                >
                                    <div>
                                        {scheduleData[day].map((event, index) => (
                                            <div key={index}>
                                                <div className="flex justify-between items-center py-4 px-6 text-white">
                                                    <span className="text-lg font-oxanium">{event.event}</span>
                                                    <span className="text-lg font-oxanium font-bold">{event.time}</span>
                                                </div>
                                                {index !== scheduleData[day].length - 1 && (
                                                    <div
                                                        className="h-[2px] mx-4"
                                                        style={{
                                                            background: 'rgba(255, 255, 255, 0.3)',
                                                            boxShadow:
                                                                '0 0 8px rgba(255, 255, 255, 0.5), 0 0 16px rgba(255, 255, 255, 0.3)',
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
