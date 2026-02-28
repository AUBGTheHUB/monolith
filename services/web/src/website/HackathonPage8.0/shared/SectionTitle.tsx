interface SectionTitleProps {
    title: string;
    iconSrc: string;
    iconAlt?: string;
    dark?: boolean;
}

export const SectionTitle = ({ title, iconSrc, iconAlt = '', dark = true }: SectionTitleProps) => (
    <div className="flex items-center gap-[5px]">
        <img src={iconSrc} alt={iconAlt} className="h-[42px] w-auto" />
        <h2
            className={`font-orbitron text-[40px] leading-[1] tracking-[0.3em] ${dark ? 'text-[#FFFDF5]' : 'text-black'}`}
        >
            {title}
        </h2>
    </div>
);
