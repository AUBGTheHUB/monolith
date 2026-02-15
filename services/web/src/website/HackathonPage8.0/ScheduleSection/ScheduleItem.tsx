import React from 'react';
import { ScheduleItemProps } from './types';
import './ScheduleStyle.css';

export const ScheduleItem: React.FC<ScheduleItemProps> = ({ time, event, isLast }) => (
    <div className={!isLast ? 'mb-[1rem] md:mb-[1.5rem]' : ''}>
        <div className="flex justify-between items-center py-[0.75rem] md:py-[1.25rem] text-white">
            <span className="font-oxanium leading-[1.25] table-row-text">{event}</span>
            <span className="font-oxanium font-bold leading-[1.25] table-row-text">{time}</span>
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
