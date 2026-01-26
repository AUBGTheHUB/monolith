type AwardCardProps = {
    title: string;
    position: number;
    prize: string;
    background: string;
    width: string;
    height: string;
    titleSize: string;
    numberSize: string;
    prizeSize: string;
};

export const AwardCard = ({
    title,
    position,
    prize,
    background,
    width,
    height,
    titleSize,
    numberSize,
    prizeSize,
}: AwardCardProps) => {
    return (
        <article className="flex flex-col items-center">
            <div
                className={`relative rounded-[1.5rem] lg:rounded-[2rem] border-2 border-white overflow-hidden ${width} ${height} bg-cover bg-center bg-no-repeat shadow-2xl flex flex-col`}
                style={{ backgroundImage: `url('${background}')` }}
            >
                <div className="pt-4 lg:pt-[1vw] xl:pt-6 px-6 lg:px-[1.5vw] xl:px-9 pb-3 lg:pb-[0.8vw] xl:pb-5 flex items-center justify-center border-b-[2px] border-white">
                    <h3 className={`text-white font-orbitron font-bold text-center ${titleSize}`}>{title}</h3>
                </div>

                <div className="flex-1 flex items-center justify-center">
                    <p className={`text-white font-orbitron font-bold leading-none ${numberSize}`}>{position}</p>
                </div>

                <div className="pt-3 lg:pt-[0.8vw] xl:pt-5 pb-4 lg:pb-[1vw] xl:pb-6 px-6 lg:px-[1.5vw] xl:px-9 flex items-center justify-center border-t-[2px] border-white">
                    <p className={`text-white font-orbitron font-bold text-center ${prizeSize}`}>{prize}</p>
                </div>
            </div>
        </article>
    );
};
