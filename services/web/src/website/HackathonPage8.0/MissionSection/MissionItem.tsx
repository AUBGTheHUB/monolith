import { missionContent } from './data';
import './MissionItem.css';

export const MissionItem = () => {
    return (
        <>
            <div
                className="
                    w-full
                    rounded-[20px]
                    p-6
                    md:px-10
                    md:py-8
                    font-oxanium
                    leading-[1.4]
                    text-white
                    mission-item-container
                "
            >
                {missionContent.paragraphs.map((text, index) => (
                    <p key={index} className={index > 0 ? 'mt-6' : undefined}>
                        {text}
                    </p>
                ))}
            </div>
        </>
    );
};
