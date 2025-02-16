type JuryModule = {
    imgSrc: string;
    name: string;
    job: string;
    company: string;
};

export default function JutyAndMentorModule({ imgSrc, name, job, company }: JuryModule) {
    return (
        <div className="relative min-w-[19rem] max-w-[19rem]  h-96 border-[1px] rounded-[6px] border-[#A9B4C3] font-semibold ">
            <div className="h-full w-full">
                <img src={imgSrc} alt={name} className="object-fill w-full h-full rounded-[6px]" />
            </div>
            <div className="absolute flex flex-col inset-x-0 bottom-0 w-full h-1/4 py-3 pl-2 gap-2 bg-[#010B15]/[0.8] rounded-b-[6px] ">
                <img src="/jury/jury_line_and_dot.svg" className="w-1/6"></img>
                <h3 className="text-secondary opacity-100">{name}</h3>
                <h4 className="text-[#83939F] text-[0.64rem]">
                    {job} | {company}
                </h4>
            </div>
        </div>
    );
}
