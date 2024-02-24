import React, { Component } from 'react';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
//import './carousel.css';

const SampleNextArrow = props => {
    const { className, style, onClick } = props;
    return (
        <svg
            onClick={onClick}
            className={className}
            style={{ ...style, display: 'flex' }}
            width="44"
            height="44"
            viewBox="0 0 44 44"
            fill="none"
            xmlns="http://www.w3.org/2000/svg">
            <path
                d="M42.1666 20.1673V23.834H40.3333V25.6673H38.4999V27.5007H36.6666V29.334H34.8333V31.1673H32.9999V33.0007H31.1666V34.834H29.3333V36.6673H27.4999V38.5007H25.6666V40.334H23.8333V42.1673H21.9999V40.334H20.1666V38.5007H18.3333V36.6673H20.1666V34.834H21.9999V33.0007H23.8333V31.1673H25.6666V29.334H27.4999V27.5007H29.3333V25.6673H1.83325V18.334H29.3333V16.5007H27.4999V14.6673H25.6666V12.834H23.8333V11.0007H21.9999V9.16732H20.1666V7.33398H18.3333V5.50065H20.1666V3.66732H21.9999V1.83398H23.8333V3.66732H25.6666V5.50065H27.4999V7.33398H29.3333V9.16732H31.1666V11.0007H32.9999V12.834H34.8333V14.6673H36.6666V16.5007H38.4999V18.334H40.3333V20.1673H42.1666Z"
                fill="#FB4298"
            />
        </svg>
    );

    //    <div className={className} style={{ ...style, display: 'block', background: 'red' }} onClick={onClick} />;
};

const SamplePrevArrow = props => {
    const { className, style, onClick } = props;
    return (
        <svg
            onClick={onClick}
            className={className}
            style={{ ...style, display: 'flex', transform: 'rotate(180deg)', marginRight: '10px' }}
            width="44"
            height="44"
            viewBox="0 0 44 44"
            fill="none"
            xmlns="http://www.w3.org/2000/svg">
            <path
                d="M42.1666 20.1673V23.834H40.3333V25.6673H38.4999V27.5007H36.6666V29.334H34.8333V31.1673H32.9999V33.0007H31.1666V34.834H29.3333V36.6673H27.4999V38.5007H25.6666V40.334H23.8333V42.1673H21.9999V40.334H20.1666V38.5007H18.3333V36.6673H20.1666V34.834H21.9999V33.0007H23.8333V31.1673H25.6666V29.334H27.4999V27.5007H29.3333V25.6673H1.83325V18.334H29.3333V16.5007H27.4999V14.6673H25.6666V12.834H23.8333V11.0007H21.9999V9.16732H20.1666V7.33398H18.3333V5.50065H20.1666V3.66732H21.9999V1.83398H23.8333V3.66732H25.6666V5.50065H27.4999V7.33398H29.3333V9.16732H31.1666V11.0007H32.9999V12.834H34.8333V14.6673H36.6666V16.5007H38.4999V18.334H40.3333V20.1673H42.1666Z"
                fill="#FB4298"
            />
        </svg>
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
                <div className="tedko-container" key={data.id}>
                    <img
                        className={'tedko-image'}
                        style={{
                            objectFit: 'cover',
                            margin: '10px',
                        }}
                        src={data.profilepicture}
                    />
                    <div className="text-bottom">
                        <p className="names">
                            {data.firstname} {data.lastname}
                        </p>
                        <div className="bonus-info">
                            <p className="position">{data.position}</p>
                            <p className="company">{data.company}</p>
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
                    breakpoint: 700,
                    settings: {
                        slidesToShow: 2,
                        slidesToScroll: 2,
                    },
                },
                {
                    breakpoint: 480,
                    settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1,
                    },
                },
            ],
        };
        return (
            <>
                <Slider className="carousel" {...settings}>
                    {this.sliders()}
                </Slider>
            </>
        );
    }
}
