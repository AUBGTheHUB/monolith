interface SectionTitleProps {
    title: string;
    iconSrc: string;
    iconAlt?: string;
    dark?: boolean;
    textColor?: string;
}

export const SectionTitle = ({ title, iconSrc, iconAlt = '', dark = true, textColor }: SectionTitleProps) => (
    <div className="flex items-center gap-[5px]">
        <img src={iconSrc} alt={iconAlt} className="h-[28px] md:h-[42px] w-auto flex-shrink-0" />
        <h2
            className={`font-orbitron text-[24px] md:text-[40px] leading-[1] tracking-[0.12em] md:tracking-[0.3em] ${textColor ?? (dark ? 'text-[#FFFDF5]' : 'text-black')}`}
        >
            {title}
        </h2>
    </div>
);
