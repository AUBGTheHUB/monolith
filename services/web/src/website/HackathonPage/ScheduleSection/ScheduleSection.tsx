import { Fragment } from 'react/jsx-runtime';

export default function ScheduleSection() {
    return (
        <div className="relative w-full flex justify-center items-center font-mont bg-[#000912]">
            <div className="absolute inset-0">
                <img src="./schedule_bg.png" alt="" className="absolute w-full h-full object-cover  opacity-20" />
                <div className="absolute inset-0 bg-gradient-to-b from-[#000912] via-transparent to-[#000912]" />
            </div>
            <div className="relative w-4/5 flex flex-col z-10 my-24">
                <div className="sm:text-4xl text-3xl sm:mb-20 mb-10 flex items-center ">
                    <img src="./n.png" alt="" className="w-[1.6rem]" />
                    <p className="text-white ml-5 tracking-[0.2em]">SCHEDULE</p>
                </div>
                <div className="flex flex-col">
                    {scheduleData.map(({ day, events }) => (
                        <div key={day} className="flex flex-col sm:flex-row items-start mb-10 relative">
                            <p className="w-full sm:w-2/5 text-white sm:text-3xl text-2xl sm:sticky sm:top-5 mb-6 sm:mb-0 ">
                                {day}
                            </p>
                            <div className="w-full sm:w-3/5 sm:text-lg text-base">
                                <table className="w-full sm:mt-14 border border-separate border-gray-600 rounded-lg bg-[#13181C]/80 backdrop-blur-md">
                                    <tbody>
                                        {events.map(({ time, event }, idx) => (
                                            <Fragment key={event}>
                                                <tr key={idx} className="w-full">
                                                    <td className="w-1/12 p-4 text-[#A9B4C3]">{time}</td>
                                                    <td className="text-white">{event}</td>
                                                </tr>
                                                {idx !== events.length - 1 && (
                                                    <tr>
                                                        <td colSpan={2} className="text-center">
                                                            <hr className="w-[95%] mx-auto border-gray-600 border-[0.5px]" />
                                                        </td>
                                                    </tr>
                                                )}
                                            </Fragment>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

const scheduleData = [
    {
        day: 'Friday',
        events: [
            { time: '16:00', event: 'Registration' },
            { time: '18:00', event: 'Opening Ceremony' },
            { time: '19:00', event: 'Dinner and Brainstorming' },
            { time: '21:00', event: 'Idea Pitching' },
            { time: '21:30', event: 'Start Coding' },
        ],
    },
    {
        day: 'Saturday',
        events: [
            { time: '09:00', event: 'Breakfast' },
            { time: '10:00', event: 'Idea Pitching to Mentors' },
            { time: '11:00', event: 'Mentors Presentations' },
            { time: '11:30', event: 'Mentorship and HR Booths' },
            { time: '13:00', event: 'Lunch' },
            { time: '14:00', event: 'Mentorship and Coding' },
            { time: '17:30', event: 'Mentorship Ends' },
            { time: '19:00', event: 'Dinner and Coding' },
        ],
    },
    {
        day: 'Sunday',
        events: [
            { time: '10:00', event: 'Breakfast and Coding' },
            { time: '12:00', event: 'Submission Deadline' },
            { time: '13:00', event: 'Presentations Begin' },
            { time: '14:10', event: 'Lunch' },
            { time: '19:30', event: 'Award Ceremony' },
        ],
    },
];
