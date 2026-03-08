import React from 'react';
import { ScheduleItemProps } from './types';
import './style.css';

export const ScheduleItem: React.FC<ScheduleItemProps> = ({ time, event, isLast }) => (
    <div className={!isLast ? 'mb-[0.75rem] md:mb-[1rem]' : ''}>
        <div className="flex justify-between items-center py-[0.5rem] md:py-[0.9rem] text-white">
            <span className="font-oxanium leading-[1.25] table-row-text">{event}</span>
            <span className="font-oxanium font-bold leading-[1.25] table-row-text">{time}</span>
        </div>
        {!isLast && <div className="schedule-divider" />}
    </div>
);
