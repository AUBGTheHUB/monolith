import React, { Component } from 'react';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import mentorsStyles from './MentorsSection/mentors_section.module.css';

const SampleNextArrow = props => {
    const { className, style, onClick } = props;
    return (
        <img
            onClick={onClick}
            className={className}
            style={{
                ...style,
                display: 'block',
                width: '30px',
                height: '30px',
                right: '-4vw',
                zIndex: 999,
            }}
            src="arrow-right.png"></img>
    );
};

const SamplePrevArrow = props => {
    const { className, style, onClick } = props;
    return (
        <img
            onClick={onClick}
            className={className}
            style={{
                ...style,
                display: 'block',
                width: '30px',
                height: '30px',
                left: '-4vw',
                zIndex: 999,
            }}
            src="arrow-left.png"></img>
    );
};

export default class SimpleSlider extends Component {
    constructor(props) {
        super(props);
        const slides = this.props.view;
        const pictures = this.props.pictures;
        console.log(props);
        this.state = {
            sliders: pictures,
            slides: slides,
        };
    }

    sliders() {
        return this.state.sliders.map(data => {
            return (
                <div className={mentorsStyles['tedko-container']} key={data.id}>
                    <img
                        className={mentorsStyles['tedko-image']}
                        style={{
                            objectFit: 'cover',
                        }}
                        src={data.profilepicture}
                    />
                    <div className={mentorsStyles['text-bottom']}>
                        <p className={mentorsStyles['names']}>
                            {data.firstname} {data.lastname}
                        </p>
                        <div className={mentorsStyles['bonus-info']}>
                            <p className={mentorsStyles['position']}>{data.position}</p>
                            <p className={mentorsStyles['company']}>{data.company}</p>
                        </div>
                    </div>
                </div>
            );
        });
    }
    render() {
        const settings = {
            infinite: true,
            speed: 700,
            slidesToShow: this.state.slides,
            slidesToScroll: this.state.slides,
            arrows: true,
            autoplay: true,
            centerMode: false,
            centerPadding: 30,
            autoplaySpeed: 100000,
            pauseOnHover: true,
            nextArrow: <SampleNextArrow />,
            prevArrow: <SamplePrevArrow />,
            responsive: [
                {
                    breakpoint: 1024,
                    settings: {
                        slidesToShow: 3,
                        slidesToScroll: 3,
                        infinite: true,
                    },
                },
                {
                    breakpoint: 900,
                    settings: {
                        slidesToShow: 2,
                        slidesToScroll: 2,
                    },
                },
                {
                    breakpoint: 700,
                    settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1,
                    },
                },
            ],
        };
        return (
            <>
                <Slider className={mentorsStyles['carousel']} {...settings}>
                    {this.sliders()}
                </Slider>
            </>
        );
    }
}
