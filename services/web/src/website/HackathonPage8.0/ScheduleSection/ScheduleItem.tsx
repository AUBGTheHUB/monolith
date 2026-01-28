import React from 'react';
import { ScheduleEvent } from './types';

interface ScheduleItemProps extends ScheduleEvent {
    isLast: boolean;
}

export const ScheduleItem: React.FC<ScheduleItemProps> = ({ time, event, isLast }) => (
    <div>
        <div className="flex justify-between items-center py-6 lg:py-8 px-8 lg:px-10 text-white">
            <span className="text-sm sm:text-base lg:text-xl font-oxanium break-words max-w-[65%]">{event}</span>
            <span className="text-sm sm:text-base lg:text-xl font-oxanium font-bold">{time}</span>
        </div>
        {!isLast && (
            <div
                className="h-[2px] mx-8 lg:mx-10"
                style={{
                    background: 'rgba(255, 255, 255, 0.3)',
                    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.25)',
                }}
            />
        )}
    </div>
);
