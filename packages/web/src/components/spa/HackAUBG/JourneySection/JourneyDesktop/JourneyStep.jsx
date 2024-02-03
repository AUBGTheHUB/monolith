import { JourneyStepVisuals } from './JourneyStepVisuals';

export const JourneyStep = ({ title, paragraph, icon, blur, figure, displayTextLeft }) => {
    return (
        <div className="journey-desktop-step">
            {!displayTextLeft && <JourneyStepVisuals blur={blur} figure={figure} />}

            <div className="journey-desktop-step-info">
                <div className="journey-desktop-step-info-heading">
                    <img src={icon} />
                    <h2>{title}</h2>
                </div>

                <p>{paragraph}</p>
            </div>

            {displayTextLeft && <JourneyStepVisuals blur={blur} figure={figure} />}
        </div>
    );
};
