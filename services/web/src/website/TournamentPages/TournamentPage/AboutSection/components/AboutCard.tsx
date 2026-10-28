interface AboutCardContent {
    title: string;
    description: string;
    image: string;
}

export default function AboutCard({ title, description, image }: AboutCardContent) {
    return (
        <div className="border-2 rounded-2xl px-3 md:px-4 w-[70%] lg:w-[24%] border-[#C79B3B] flex flex-col pt-4 pb-8 md:pb-10 gap-3">
            <div className="flex flex-col items-center gap-1">
                <img src={`${image}`} className="w-[36px] h-[36px] md:w-[60px] md:h-[60px]" alt="" />
                <h4 className="font-league font-bold text-[#C79B3B] text-base md:text-xl text-center">{title}</h4>
            </div>
            <div className="text-[#90D5FF] text-xs md:text-base font-normal">{description}</div>
        </div>
    );
}
