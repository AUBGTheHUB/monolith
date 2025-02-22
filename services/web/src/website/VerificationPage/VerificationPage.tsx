import { Fragment } from 'react/jsx-runtime';
import { Navigation } from '../HackathonPage/Navigation/Navigation';
import { VerificationComponent } from './components/VerificationComponent';

export const VerificationPage = () => {
    return (
        <Fragment>
            <Navigation />
            <VerificationComponent />
        </Fragment>
    );
};
