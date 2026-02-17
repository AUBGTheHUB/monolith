import { recapContent } from './data';

export const RecapVideo = () => {
    return (
        <div className="relative w-full max-w-full mx-auto pt-[56.25%] overflow-hidden rounded-[20px] bg-black/20">
            <iframe
                className="absolute inset-0 w-full h-full border-0"
                src={recapContent.youtubeEmbedUrl}
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
                title="HackAUBG Recap Video"
            />
        </div>
    );
};
