import { Fragment } from 'react/jsx-runtime';
import RegistrationForm from './RegistrationForm/RegistrationForm';
import { Navigation } from './NavigationSection/Navigation';
import { Helmet } from 'react-helmet';

export const FormPage = () => {
    return (
        <Fragment>
            <Helmet>
                <title>Hackathon 7.0</title>
                <link rel="icon" href="/faviconHack.ico" />
            </Helmet>
            <Navigation />
            <RegistrationForm />
        </Fragment>
    );
};
