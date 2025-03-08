import { Fragment } from 'react/jsx-runtime';
import { VerificationComponent } from './components/VerificationComponent';
import { Helmet } from 'react-helmet';

export const VerificationPage = () => {
    return (
        <Fragment>
            <Helmet>
                <title>Hackathon Page</title>
                <link rel="icon" href="faviconHack.ico" />
            </Helmet>
            <VerificationComponent />
        </Fragment>
    );
};
