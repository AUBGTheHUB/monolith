import { BsLinkedin } from 'react-icons/bs';
import './members.old.css';

export const MembersCard = ({ prop }) => {
    return (
        <div>
            <h1 className="members-card-overlay-text name">{prop.firstname}</h1>
            <h2 className="members-card-overlay-text position">{prop.position}</h2>
            {prop.sociallink !== '' && (
                <BsLinkedin
                    className="members-card-overlay-text linkedin-icon"
                    onClick={() => window.open(prop.sociallink)}
                />
            )}
        </div>
    );
};
