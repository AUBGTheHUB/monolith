export type Day = 'Friday' | 'Saturday' | 'Sunday';

export type ScheduleEvent = {
    time: string;
    event: string;
};

export interface ScheduleItemProps extends ScheduleEvent {
    isLast: boolean;
}

export interface ScheduleTabsProps {
    activeTab: Day;
}
