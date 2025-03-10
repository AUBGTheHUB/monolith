import { EmblaOptionsType } from 'embla-carousel';

export const OPTIONS: EmblaOptionsType = {
    breakpoints: {
        '(max-width: 600px)': {
            // Small screens (Mobile)
            align: 'center',
            slidesToScroll: 1,
        },
        '(min-width: 600px) and (max-width: 1500px)': {
            // Medium screens (Tablets)
            align: 'center',
            slidesToScroll: 3,
        },
        '(min-width: 1500px)': {
            // Large screens (Desktops)
            align: 'center',
            slidesToScroll: 4,
        },
    },
};
