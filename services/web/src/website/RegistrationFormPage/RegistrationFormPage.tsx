import { Fragment } from 'react/jsx-runtime';
import RegistrationForm from './RegistrationForm/RegistrationForm';
import { Navigation } from './NavigationSection/Navigation';
import { useFeatureSwitches } from '@/config';

export const FormPage = () => {
    const featureSwitches = useFeatureSwitches();

    return (
        <Fragment>
            <Navigation />
            <RegistrationForm RegSwitch={featureSwitches.RegSwitch} isRegTeamsFull={featureSwitches.isRegTeamsFull} />
        </Fragment>
    );
};
