import { Fragment } from 'react/jsx-runtime';
import JurySection from './JurySection/components/JurySection';
import MentorsSection from './MentorsSection/components/MentorsSection';

export const HackathonPage = () => {
    return (
        <Fragment>
            <h1 className="font-distant text-white">SF Distant Galaxy Regular</h1>
            <MentorsSection></MentorsSection>
            <JurySection></JurySection>
        </Fragment>
    );
};
