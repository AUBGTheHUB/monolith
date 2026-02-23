import type { FooterColumn } from './types';

type Props = {
    column: FooterColumn;
};

export const FooterItem = ({ column }: Props) => {
    return (
        <div className="flex flex-col gap-6">
            <h3 className="font-orbitron text-[19px] font-bold text-white tracking-wide">{column.title}</h3>

            <ul className="flex flex-col gap-4 font-oxanium text-[19px] text-[#A9B4C3]">
                {column.items.map((item, index) => (
                    <li key={index}>
                        {item.href ? (
                            <a
                                href={item.href}
                                className=" text-[#A9B4C3] hover:text-white transition-colors duration-200"
                            >
                                {item.label}
                            </a>
                        ) : (
                            <span>{item.label}</span>
                        )}
                    </li>
                ))}
            </ul>
        </div>
    );
};
