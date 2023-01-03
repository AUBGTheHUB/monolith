import { useEffect, useState } from 'react';
import './articles_section.css';
import axios from 'axios';
import { url } from '../../../Global';
import { Article, Carousel } from 'react-hovering-cards-carousel';
import '../../../../node_modules/react-hovering-cards-carousel/dist/style.css';

export const ArticlesSection = () => {
    const [articles, setArticles] = useState([]);

    const getArticles = () => {
        axios({
            method: 'get',
            url: url + '/api/article'
        })
            .then((res) => {
                let data = [];
                res.data.data.data.forEach((element) => {
                    data.push(
                        new Article(
                            element.title,
                            element.author,
                            element.mediumlink,
                            element.banner
                        )
                    );
                });

                setArticles(data);
            })

            // eslint-disable-next-line no-unused-vars
            .catch((err) => {
                console.log(err);
            });
    };

    useEffect(() => {
        getArticles();
    }, []);

    //eslint-disable-next-line
    if (!!articles) {
        return (
            <div className="articles-container">
                <Carousel cards={articles} scale={2} />
            </div>
        );
    }
};
