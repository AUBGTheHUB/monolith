export const JourneyStepVisuals = ({ blur, figure }) => {
    return (
        <div className="journey-desktop-step-visuals">
            <img src={blur} className="journey-desktop-step-visuals-blur" />
            <img src={figure} className="journey-desktop-step-visuals-figure" />
        </div>
    );
};
