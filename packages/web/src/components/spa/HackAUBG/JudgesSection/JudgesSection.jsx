import React from 'react';
import './judges_section.css';

export const JudgesSection = () => {
    return (
        <div className="judges-container">
            <h1 className="judges-header">Judges</h1>
            <div className="judges-picture">
                <img src="https://cdn.freecodecamp.org/curriculum/css-photo-gallery/1.jpg"></img>
                <img src="https://cdn.freecodecamp.org/curriculum/css-photo-gallery/2.jpg"></img>
                <img src="https://cdn.freecodecamp.org/curriculum/css-photo-gallery/3.jpg"></img>
                <img src="https://cdn.freecodecamp.org/curriculum/css-photo-gallery/4.jpg"></img>
                <img src="https://cdn.freecodecamp.org/curriculum/css-photo-gallery/5.jpg"></img>
                <img src="https://cdn.freecodecamp.org/curriculum/css-photo-gallery/6.jpg"></img>
            </div>
        </div>
    );
};

export default JudgesSection;
