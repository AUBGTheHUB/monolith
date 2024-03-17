import React from 'react';
import { Button } from 'react-bootstrap';
import { downloadTeamsURL } from '../../../../Global';
import axios from 'axios';
import styles from './hackathon_teams.module.css';

const getTeams = () => {
    const token = localStorage.getItem('auth_token');

    axios({
        method: 'get',
        url: downloadTeamsURL,
        headers: { 'BEARER-TOKEN': token },
        responseType: 'blob',
    })
        .then(res => {
            const blob = new Blob([res.data], { type: 'application/octet-stream' });
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'teams.csv');
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        })
        .catch(err => {
            console.log(err);
        });
};

export const Hackteams = () => {
    return (
        <div className={styles.hackteams_container}>
            <Button onClick={() => getTeams()} className={styles.download_btn}>
                Download Teams
            </Button>
            {/* <a onClick={() => getTeams()}>Download Teams</a> */}
        </div>
    );
};
