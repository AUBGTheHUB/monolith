import { recapContent } from './data';
import './RecapVideo.css';

export const RecapVideo = () => {
    return (
        <div className="recap-video-wrapper">
            <iframe
                className="recap-video-iframe"
                src={recapContent.youtubeEmbedUrl}
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
                title="HACKAUBG 7.0"
            />
        </div>
    );
};
