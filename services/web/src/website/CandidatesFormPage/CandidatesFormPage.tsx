import { Fragment } from 'react/jsx-runtime';
import CandidatesForm from '@/website/CandidatesFormPage/CandidatesForm/CandidatesForm.tsx';
import { Navigation } from './NavigationSection/Navigation';
// import { useFeatureSwitches } from '@/config';
import { Helmet } from 'react-helmet';

export const CandidatesFormPage = () => {
    // const featureSwitches = useFeatureSwitches();

    return (
        <Fragment>
            <Helmet>
                <title>Hackathon 8.0</title>
                <link rel="icon" href="/faviconHack.ico" />
            </Helmet>
            <Navigation />
            {/*<CandidatesForm RegSwitch={featureSwitches.RegSwitch} isRegTeamsFull={featureSwitches.isRegTeamsFull} />*/}
            <CandidatesForm />
        </Fragment>
    );
};
