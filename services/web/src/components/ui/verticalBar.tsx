export const VerticalBar = ({ isRight, isBlack }: { isRight: boolean; isBlack: boolean }) => {
    const color = isBlack ? 'bg-[#000000]' : 'bg-[#FFFDF5]';
    const position = isRight ? 'right-[39px]' : 'left-[39px]';
    return (
        <div className={`pointer-events-none absolute top-0 bottom-0 ${position} w-[7px] ${color} hidden md:block`} />
    );
};
