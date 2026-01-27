export type Day = 'Friday' | 'Saturday' | 'Sunday';

export const scheduleData: Record<Day, Array<{ time: string; event: string }>> = {
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
