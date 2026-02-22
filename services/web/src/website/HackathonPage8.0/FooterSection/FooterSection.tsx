import { footerData } from './data';
import { FooterItem } from './FooterItem';
import { VerticalBar } from '@/components/ui/verticalBar';

export const FooterSection = () => {
    return (
        <footer className="relative w-full bg-[#171514] pt-20 pb-8 overflow-hidden rounded-t-[20px]">
            <div className="absolute inset-0 bg-[#171514] bg-cover bg-center blur-[0.4px] opacity-[0.25] pointer-events-none" />

            <VerticalBar isRight={false} isBlack={false} />
            <VerticalBar isRight={true} isBlack={false} />

            <div className="relative z-10 mx-auto max-w-full px-8 md:px-44">
                <div className="grid grid-cols-1 gap-10 md:grid-cols-4 md:gap-8 text-left">
                    {footerData.map((column) => (
                        <FooterItem key={column.id} column={column} />
                    ))}
                </div>

                <div className="mt-16 mb-8 h-px w-full bg-[#521010]" />

                <div className="flex flex-col items-center justify-between gap-4 md:flex-row font-oxanium text-[16px] text-[#A9B4C3]">
                    <span>Copyright The hub</span>
                    <a href="#" className="text-[#A9B4C3] hover:text-white transition-colors duration-200">
                        Privacy Policy
                    </a>
                </div>
            </div>
        </footer>
    );
};
