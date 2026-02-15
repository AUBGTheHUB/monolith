import { TabsContent } from '@/components/ui/tabs';
import { scheduleData } from './data';
import { ScheduleItem } from './ScheduleItem';
import { Day } from './types';
import './ScheduleStyle.css';

export const ScheduleTable = () => (
    <>
        {(['Friday', 'Saturday', 'Sunday'] as Day[]).map((day) => (
            <TabsContent key={day} value={day} className="w-full">
                <div
                    className="rounded-[1rem] md:rounded-[1.25rem] w-full"
                    style={{
                        background: 'linear-gradient(135deg, #B91C1C 0%, #DC2626 30%, #F97316 70%, #FB923C 100%)',
                        width: '100%',
                    }}
                >
                    <div className="px-[1.5rem] md:px-[2.25rem] py-[1rem] md:py-[1.313rem]">
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
