type HubberModuleType = {
    imgSrc: string;
    name: string;
};

export default function HubberModule({ imgSrc, name }: HubberModuleType) {
    return (
        <div className="group flex flex-col min-w-28 max-w-80 max-[1122px]:max-w-full p-2 border border-[rgb(255,255,255,0.2)] rounded-[15px] font-semibold transition-all duration-300 hover:bg-transparent">
            <div className="relative w-full">
                <img src={imgSrc} alt={name} className="block w-full h-auto rounded-xl" />
            </div>
            <div className="py-3 gap-2">
                <h3
                    className="text-secondary truncate w-full group-hover:whitespace-normal group-hover:overflow-visible"
                    style={{ textOverflow: 'clip' }}
                >
                    {name}
                </h3>
            </div>
        </div>
    );
}
