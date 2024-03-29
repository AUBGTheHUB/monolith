import React from 'react';
import './schedule_section.css';
import { FsContext } from '../../../../feature_switches';
import { useContext } from 'react';

export const ScheduleHackathon = () => {
    // eslint-disable-next-line
    const [featureSwitches, _] = useContext(FsContext);

    if (featureSwitches.Schedule) {
        return (
            <div className="schedule-section-container" id="schedule">
                <h1 className="schedule-section-title">THE SCHEDULE</h1>
                <div className="schedule-text-container">
                    <div className="schedule-table-container" id="friday-container">
                        <h1 className="schedule-table-title">FRIDAY</h1>
                        <div className="schedule-table-row">
                            <h2 className="schedule-time">16:00</h2>
                            <p>Registration</p>
                        </div>
                        <div className="schedule-table-row">
                            <h2 className="schedule-time">18:00</h2>
                            <p>Opening Ceremony</p>
                        </div>
                        <div className="schedule-table-row">
                            <h2 className="schedule-time">19:00</h2>
                            <p>Dinner and Brainstorming</p>
                        </div>
                        <div className="schedule-table-row">
                            <h2 className="schedule-time">21:00</h2>
                            <p>Idea Pitching</p>
                        </div>
                        <div className="schedule-table-row">
                            <h2 className="schedule-time">21:30</h2>
                            <p>Start coding</p>
                        </div>
                    </div>
                    <div className="schedule-table-container" id="saturday-container">
                        <h1 className="schedule-table-title">SATURDAY</h1>
                        <div className="schedule-table-row">
                            <h2 className="schedule-time">09:00</h2>
                            <p>Breakfast</p>
                        </div>
                        <div className="schedule-table-row">
                            <h2 className="schedule-time">10:00</h2>
                            <p>Idea Pitching to Mentors</p>
                        </div>
                        <div className="schedule-table-row">
                            <h2 className="schedule-time">11:00</h2>
                            <p>Mentors Presentations</p>
                        </div>
                        <div className="schedule-table-row">
                            <h2 className="schedule-time">11:30</h2>
                            <p>Mentorship and HR Booths</p>
                        </div>
                        <div className="schedule-table-row">
                            <h2 className="schedule-time">13:00</h2>
                            <p>Lunch</p>
                        </div>
                        <div className="schedule-table-row">
                            <h2 className="schedule-time">14:00</h2>
                            <p>Mentorship and Coding</p>
                        </div>
                        <div className="schedule-table-row">
                            <h2 className="schedule-time">17:30</h2>
                            <p>Mentorship Ends</p>
                        </div>
                        <div className="schedule-table-row">
                            <h2 className="schedule-time">19:00</h2>
                            <p>Dinner and Coding</p>
                        </div>
                    </div>
                    <div className="schedule-table-container">
                        <h1 className="schedule-table-title">SUNDAY</h1>
                        <div className="schedule-table-row">
                            <h2 className="schedule-time">10:00</h2>
                            <p>Breakfast and Coding</p>
                        </div>
                        <div className="schedule-table-row">
                            <h2 className="schedule-time">12:00</h2>
                            <p>Submission Deadline</p>
                        </div>
                        <div className="schedule-table-row">
                            <h2 className="schedule-time">13:00</h2>
                            <p>Presentations Begin</p>
                        </div>
                        <div className="schedule-table-row">
                            <h2 className="schedule-time">14:10</h2>
                            <p>Lunch</p>
                        </div>
                        <div className="schedule-table-row">
                            <h2 className="schedule-time">19:30</h2>
                            <p>Award Ceremony</p>
                        </div>
                    </div>
                </div>
            </div>
        );
    } else {
        return (
            <p className="schedule_closed" id="registration">
                Schedule coming soon!
            </p>
        );
    }
};
