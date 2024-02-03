export const JourneyStep = ({ props }) => {
    if (props.displayTextLeft) {
        return (
            <div className="journey-desktop-step">
                <div className="journey-desktop-step-info">
                    <div className="journey-desktop-step-info-heading">
                        <img src={props.icon} />
                        <h2>{props.title}</h2>
                    </div>

                    <p>{props.paragraph}</p>
                </div>
                <div className="journey-desktop-step-visuals">
                    <img src={props.blur} className="journey-desktop-step-visuals-blur" />
                    <img src={props.figure} className="journey-desktop-step-visuals-figure" />
                </div>
            </div>
        );
    }

    return (
        <div className="journey-desktop-step">
            <div className="journey-desktop-step-visuals">
                <img src={props.blur} className="journey-desktop-step-visuals-blur" />
                <img src={props.figure} className="journey-desktop-step-visuals-figure" />
            </div>
            <div className="journey-desktop-step-info">
                <div className="journey-desktop-step-info-heading">
                    <img src={props.icon} />
                    <h2>{props.title}</h2>
                </div>

                <p>{props.paragraph}</p>
            </div>
        </div>
    );
};
