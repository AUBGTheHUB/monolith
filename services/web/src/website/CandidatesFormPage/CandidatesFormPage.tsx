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
                <title>Apply</title>
                <link rel="icon" href="/favicon.ico" />
            </Helmet>
            <Navigation />
            {/*<CandidatesForm RegSwitch={featureSwitches.RegSwitch}*/}
            <CandidatesForm />
        </Fragment>
    );
};
