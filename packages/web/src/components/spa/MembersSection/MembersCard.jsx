import { BsLinkedin } from 'react-icons/bs';

export const MembersCard = ({ prop }) => {
    return (
        <div className="container">
            <h1 className="members-card-overlay-text name">{prop.firstname}</h1>
            <p className="members-card-overlay-text position">
                {prop.position}
            </p>
            <BsLinkedin
                className="members-card-overlay-text linkedin-icon"
                onClick={() => window.open(prop.sociallink)}
            />
        </div>
    );
};
