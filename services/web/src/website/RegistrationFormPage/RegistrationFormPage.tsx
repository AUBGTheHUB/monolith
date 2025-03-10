import { Fragment } from 'react/jsx-runtime';
import RegistrationForm from './RegistrationForm/RegistrationForm';
import { Navigation } from '../MainPage/Navigation/Navigation';

export const FormPage = () => {
    return (
        <Fragment>
            <Navigation />
            <RegistrationForm />
        </Fragment>
    );
};
