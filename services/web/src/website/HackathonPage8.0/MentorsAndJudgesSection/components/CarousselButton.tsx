import { Button, type ButtonProps } from '@/components/ui/button';
import { ArrowLeft, ArrowRight } from 'lucide-react';

interface CarousselButtonProps extends ButtonProps {
    left?: boolean;
    right?: boolean;
}

export function CarousselButton({ left, right, ...props }: CarousselButtonProps) {
    return (
        <Button
            {...props}
            className=" border border-[#F2F0F0] rounded-full h-[40px] w-[40px] p-0 flex items-center justify-center disabled:opacity-40 opacity-100"
        >
            <ArrowLeft className={`${left ? 'block' : 'hidden'}`} />
            <ArrowRight className={`${right ? 'block' : 'hidden'}`} />
        </Button>
    );
}
