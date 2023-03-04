import React from 'react';
import { useNavigate } from 'react-router-dom';
import './page_not_found.css';

const NotFound = () => {
    const navigate = useNavigate();

    const redirectHome = () => {
        navigate('/');
    };

    return (
        <div className="page-not-found">
            <div className="page-not-found-logo">
                <img
                    src="/hublogo.png"
                    className="page-not-found-logo-image"
                    alt="The Hub AUBG"
                    onClick={redirectHome}
                />
                <p onClick={redirectHome}>The Hub</p>
            </div>
            <div className="background-not-found">
                <div className="page-not-found-text">
                    <h1 className="heading-text-404">404</h1>
                    <h2 className="mid-heading-404">Page not found</h2>
                    <p className="paragraph-404">
                        Seems like the page you are looking for got abducted by
                        aliens...
                    </p>
                    <button
                        className="button-404"
                        type="button"
                        onClick={redirectHome}
                    >
                        Back to Homepage
                    </button>
                </div>
                <div className="hubzie-UFO-image">
                    <img
                        src="/hubzieUFOimage.png"
                        alt="Hubzie being abducted by a UFO"
                    />
                </div>
            </div>
        </div>
    );
};

export default NotFound;
