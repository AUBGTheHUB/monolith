import { useEffect, useState } from 'react';
import './articles_section.css';
import axios from 'axios';
import { url } from '../../../Global';

export const ArticlesSection = () => {
    const [articles, setArticles] = useState([]);

    const getArticles = () => {
        axios({
            method: 'get',
            url: url + '/api/members'
        })
            .then((res) => {
                setArticles(res.data.data.data);
            })
            // eslint-disable-next-line no-unused-vars
            .catch((err) => {
                console.log(err);
            });
    };

    useEffect(() => {
        getArticles();
    }, []);

    if (articles) {
        return <div className="articles-container"></div>;
    }
};
