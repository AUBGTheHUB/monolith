import React from 'react';
import { Award } from './awardsConfig';

export const AwardCard: React.FC<Award> = ({ title, prize, currency, number, image }) => {
    const classMap: Record<number, { w: string; h: string; fontNumber: string; fontPrize: string; fontTitle: string }> =
        {
            1: {
                w: 'w-[280px] lg:w-[32vw] xl:w-[500px]',
                h: 'h-[440px] lg:h-[48vw] xl:h-[750px]',
                fontNumber: 'text-[8rem] lg:text-[9vw] xl:text-[14rem]',
                fontPrize: 'text-2xl lg:text-[3.5vw] xl:text-6xl',
                fontTitle: 'text-2xl lg:text-[3.5vw] xl:text-6xl',
            },
            2: {
                w: 'w-[240px] lg:w-[25vw] xl:w-[400px]',
                h: 'h-[380px] lg:h-[40vw] xl:h-[625px]',
                fontNumber: 'text-[6rem] lg:text-[7vw] xl:text-[11rem]',
                fontPrize: 'text-xl lg:text-[2.5vw] xl:text-5xl',
                fontTitle: 'text-xl lg:text-[2vw] xl:text-4xl',
            },
            3: {
                w: 'w-[200px] lg:w-[22vw] xl:w-[344px]',
                h: 'h-[320px] lg:h-[35vw] xl:h-[550px]',
                fontNumber: 'text-[5rem] lg:text-[6vw] xl:text-[9.5rem]',
                fontPrize: 'text-lg lg:text-[2vw] xl:text-4xl',
                fontTitle: 'text-lg lg:text-[1.8vw] xl:text-3xl',
            },
        };

    const classes = classMap[number];

    return (
        <article className="flex flex-col items-center w-full lg:w-auto">
            <div
                className={`relative rounded-[1.5rem] lg:rounded-[2rem] border-2 border-white overflow-hidden shadow-2xl flex flex-col bg-cover bg-center bg-no-repeat ${classes.w} ${classes.h}`}
                style={{ backgroundImage: `url('${image}')` }}
            >
                <div className="flex items-center justify-center border-b-[2px] border-white px-6 lg:px-[2vw] pt-4 lg:pt-[1vw] xl:pt-6 pb-3 lg:pb-[0.8vw] xl:pb-5">
                    <h3 className={`text-white font-orbitron font-bold text-center ${classes.fontTitle}`}>{title}</h3>
                </div>

                <div className="flex-1 flex items-center justify-center">
                    <p className={`text-white font-orbitron font-bold leading-none ${classes.fontNumber}`}>{number}</p>
                </div>

                <div className="flex items-center justify-center border-t-[2px] border-white px-6 lg:px-[2vw] pt-3 lg:pt-[0.8vw] xl:pt-5 pb-4 lg:pb-[1vw] xl:pb-6">
                    <p className={`text-white font-orbitron font-bold text-center ${classes.fontPrize}`}>
                        <span className="award-amount">{prize}</span>{' '}
                        <span className="award-currency-unit">{currency}</span>
                    </p>
                </div>
            </div>
        </article>
    );
};
