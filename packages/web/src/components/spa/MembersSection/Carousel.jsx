import React, { Component } from 'react';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import './carousel.css';
import { FaLinkedin } from 'react-icons/fa';

export default class SimpleSlider extends Component {
    constructor(props) {
        super(props);
        const slides = this.props.view;
        const pictures = this.props.pictures;
        this.state = {
            sliders: pictures,
            slides: slides,
        };
    }
    sliders() {
        return this.state.sliders.map(data => {
            return (
                <div className="tedko-container" key={data.id}>
                    <div className="tedko-overlay"></div>
                    {data.sociallink ? (
                        <a href={data.sociallink}>
                            <FaLinkedin className="socialmedia" />
                        </a>
                    ) : null}
                    <img
                        className={'tedko-image'}
                        style={{
                            height: '200px',
                            width: '200px',
                            borderRadius: '10px',
                            objectFit: 'cover',
                            margin: '0px',
                        }}
                        src={data.profilepicture}
                    />
                    <div className="text-bottom">
                        {data.firstname} {data.lastname}
                    </div>
                    <div className="text-department">{data.department}</div>
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
            autoplaySpeed: 10000,
            pauseOnHover: true,
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
