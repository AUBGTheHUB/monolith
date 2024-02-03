import React from 'react';
import './video_section.css';

export const VideoSection = () => {
    return (
        <div className="video-container">
            <h1 className="video-header">Watch the HackAUBG 4.0 recap!</h1>
            <iframe
                className="video"
                width="853"
                height="480"
                src={'https://www.youtube.com/embed/avP5xho4Yk0'}
                // frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
                title="Embedded youtube"
            />
        </div>
    );
};

export default VideoSection;
