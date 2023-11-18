import React, { Component } from 'react';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import style from './carousel.module.css';
import { FaLinkedin } from 'react-icons/fa';

export default class SimpleSlider extends Component {
    constructor(props) {
        super(props);
        console.log(this.props.view);
        const view = this.props.view;
        const pictures = this.props.pictures;
        const slides = view != 'mobile' ? 4 : 1;
        console.log(pictures);
        this.state = {
            sliders: pictures,
            slides: slides,
        };
    }
    sliders() {
        return this.state.sliders.map(data => {
            console.log(data.sociallink);
            return (
                <div className={style.container} key={data.id}>
                    <div className={style.overlay}></div>
                    {data.sociallink ? (
                        <a href={data.sociallink}>
                            <FaLinkedin className={style.socialmedia} />
                        </a>
                    ) : null}
                    <img
                        className={style.image}
                        style={{
                            height: '200px',
                            width: '200px',
                            borderRadius: '10px',
                            objectFit: 'cover',
                            margin: '0px',
                        }}
                        src={data.profilepicture}
                    />
                    <div className={style.textbottom}>
                        {data.firstname} {data.lastname}
                    </div>
                    <div className={style.textdepartment}>{data.department}</div>
                </div>
            );
        });
    }
    render() {
        const settings = {
            infinite: true,
            speed: 700,
            slidesToShow: 2,
            slidesToScroll: 2,
            arrows: true,
            autoplay: false,
            centerMode: false,
            centerPadding: 20,
            autoplaySpeed: 3000,
            pauseOnHover: true,
        };
        return (
            <>
                <Slider className={style.carousel} {...settings}>
                    {this.sliders()}
                </Slider>
            </>
        );
    }
}
