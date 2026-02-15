import React from 'react';
import { ScheduleItemProps } from './types';

export const ScheduleItem: React.FC<ScheduleItemProps> = ({ time, event, isLast }) => (
    <div className={!isLast ? 'mb-[1rem] md:mb-[1.5rem]' : ''}>
        <div className="flex justify-between items-center py-[0.75rem] md:py-[1.25rem] text-white">
            <span className="text-[1rem] md:text-[1.4rem] lg:text-[1.6rem] font-oxanium leading-[1.25]">{event}</span>
            <span className="text-[1rem] md:text-[1.4rem] lg:text-[1.6rem] font-oxanium font-bold leading-[1.25]">
                {time}
            </span>
        </div>
        {!isLast && (
            <div
                className="h-[1px]"
                style={{
                    background: '#A9B4C3',
                    boxShadow: '0 1px 2px rgba(0, 0, 0, 0.1)',
                }}
            />
        )}
    </div>
);
