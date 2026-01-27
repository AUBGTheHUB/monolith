import { TabsContent } from '@/components/ui/tabs';
import { Day, scheduleData } from './scheduleConfig.ts';

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
                            <div key={index}>
                                <div className="flex justify-between items-center py-6 lg:py-8 px-8 lg:px-10 text-white">
                                    <span className="text-sm sm:text-base lg:text-xl font-oxanium break-words max-w-[65%]">
                                        {event.event}
                                    </span>
                                    <span className="text-sm sm:text-base lg:text-xl font-oxanium font-bold">
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
    </>
);
