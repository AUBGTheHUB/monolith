import React from 'react';
import './schedule_section.css';

export const ScheduleHackathon = () => {
    return (
        <div className="schedule-section-container" id="schedule">
            <h1 className="schedule-section-title">THE SCHEDULE</h1>
            <div className="schedule-text-container">
                <div className="schedule-table-container" id="friday-container">
                    <h1 className="schedule-table-title">FRIDAY</h1>
                    <div className="schedule-table-row">
                        <h2 className="schedule-time">17:30</h2>
                        <p>Registration and Networking</p>
                    </div>
                    <div className="schedule-table-row">
                        <h2 className="schedule-time">18:30</h2>
                        <p>Opening Ceremony</p>
                    </div>
                    <div className="schedule-table-row">
                        <h2 className="schedule-time">20:00</h2>
                        <p>Brainstorming Ideas</p>
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
                <div
                    className="schedule-table-container"
                    id="saturday-container"
                >
                    <h1 className="schedule-table-title">SATURDAY</h1>
                    <div className="schedule-table-row">
                        <h2 className="schedule-time">09:30</h2>
                        <p>Breakfast</p>
                    </div>
                    <div className="schedule-table-row">
                        <h2 className="schedule-time">11:00</h2>
                        <p>Mentorship & HR Sessions</p>
                    </div>
                    <div className="schedule-table-row">
                        <h2 className="schedule-time">11:30</h2>
                        <p>Idea Pitching Pt. 2</p>
                    </div>
                    <div className="schedule-table-row">
                        <h2 className="schedule-time">12:00</h2>
                        <p>Mentorship & HR Sessions</p>
                    </div>
                    <div className="schedule-table-row">
                        <h2 className="schedule-time">13:30</h2>
                        <p>Lunch</p>
                    </div>
                    <div className="schedule-table-row">
                        <h2 className="schedule-time">14:30</h2>
                        <p>Mentorship + Coding</p>
                    </div>
                    <div className="schedule-table-row">
                        <h2 className="schedule-time">19:30</h2>
                        <p>Dinner</p>
                    </div>
                    <div className="schedule-table-row">
                        <h2 className="schedule-time">20:30</h2>
                        <p>Coding</p>
                    </div>
                </div>
                <div className="schedule-table-container">
                    <h1 className="schedule-table-title">SUNDAY</h1>
                    <div className="schedule-table-row">
                        <h2 className="schedule-time">09:30</h2>
                        <p>Breakfast</p>
                    </div>
                    <div className="schedule-table-row">
                        <h2 className="schedule-time">10:30</h2>
                        <p>Coding</p>
                    </div>
                    <div className="schedule-table-row">
                        <h2 className="schedule-time">13:00</h2>
                        <p>Presentation Submission Deadline</p>
                    </div>
                    <div className="schedule-table-row">
                        <h2 className="schedule-time">13:00</h2>
                        <p>Lunch</p>
                    </div>
                    <div className="schedule-table-row">
                        <h2 className="schedule-time">14:30</h2>
                        <p>Presentations Begin</p>
                    </div>
                    <div className="schedule-table-row">
                        <h2 className="schedule-time">19:00</h2>
                        <p>Award Ceremony</p>
                    </div>
                </div>
            </div>
        </div>
    );
};
