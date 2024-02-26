import React, { Fragment, useContext, useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import LandingHome from './components/spa/MainPage';
import NotFound from './components/other/NotFound';
import LandingAdminPage from './components/admin_page/landing_admin_page';
import Dashboard from './components/admin_page/admin_dashboard';
import './App.css';
import { HackAUBG } from './components/spa/HackAUBG/HackAUBG';
import { JobsSection } from './components/spa/JobsSection/JobsSection';
import { goBackIfActionsAreStateless, handleUrlDependantStyling } from './Global';
import { FsContext, loadFeatureSwitches, parseFeatureSwitches } from './feature_switches';
import { Toaster } from 'react-hot-toast';
import AdminRoutesWithBackButton from './AdminRoutesWithBackButton';
import { VerifyAccount } from './components/spa/HackAUBG/VerifyAccountPop/VerifyAccount';

function App() {
    document.addEventListener('locationChange', handleUrlDependantStyling);
    window.addEventListener('load', handleUrlDependantStyling);
    useEffect(handleUrlDependantStyling, []);

    goBackIfActionsAreStateless();

    const [featureSwitches, setFeatureSwitches] = useContext(FsContext);

    useEffect(() => {
        const handleFsUpdate = async () => {
            const fs = await loadFeatureSwitches();
            setFeatureSwitches({ ...featureSwitches, ...parseFeatureSwitches(fs) });
        };
        handleFsUpdate();
    }, []);

    return (
        <Fragment>
            <Toaster />
            <Routes>
                <Route path="/" element={<LandingHome />} />
                <Route path="/*" element={<NotFound />} />
                <Route path="/hackaubg" element={<HackAUBG />}>
                    <Route path=":variable_name" element={<VerifyAccount />} />
                </Route>
                {featureSwitches.jobs ? <Route path="/jobs" element={<JobsSection />} /> : null}
                <Route path="/admin" element={<LandingAdminPage />} />
                <Route path="/admin/dashboard" element={<Dashboard />} />
                <Route path="/admin/dashboard/*" element={<AdminRoutesWithBackButton />} />
            </Routes>
        </Fragment>
    );
}

export default App;
