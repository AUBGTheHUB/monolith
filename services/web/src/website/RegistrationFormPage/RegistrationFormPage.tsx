import { Fragment } from 'react/jsx-runtime';
import RegistrationForm from './RegistrationForm/RegistrationForm';
import { Navigation } from './NavigationSection/Navigation';
import { useFeatureSwitches } from '@/config';
import { Helmet } from 'react-helmet';

export const FormPage = () => {
    const featureSwitches = useFeatureSwitches();

    return (
        <Fragment>
            <Helmet>
                <title>Hackathon 7.0</title>
                <link rel="icon" href="/faviconHack.ico" />
            </Helmet>
            <Navigation />
            <RegistrationForm RegSwitch={featureSwitches.RegSwitch} isRegTeamsFull={featureSwitches.isRegTeamsFull} />
        </Fragment>
    );
};
