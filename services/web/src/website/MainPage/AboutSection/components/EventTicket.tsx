import { Button } from '@/components/ui/button.tsx';

type EventTicketProps = {
    imgSrc: string;
    title: string;
    tags: Array<string>;
    onClick?: () => void;
};

export default function EventTicket({ imgSrc, title, tags, onClick }: EventTicketProps) {
    return (
        <div
            onClick={onClick}
            className={`flex flex-1 flex-col min-w-[300px] w-full sm:w-auto h-80 p-2 border rounded-2xl font-semibold transition-transform hover:scale-[1.02] active:scale-95 ${onClick ? 'cursor-pointer' : ''} bg-white`}
        >
            <div className="h-4/6 w-full">
                <img src={imgSrc} alt={title} className="object-cover w-full h-full rounded-xl" />
            </div>
            <div className="h-2/6 py-3 flex flex-col gap-2 justify-between">
                <h3 className="text-primary text-lg line-clamp-1" title={title}>
                    {title}
                </h3>
                <div className="flex flex-wrap gap-2 overflow-hidden h-16">
                    {tags.slice(0, 3).map((tag, index) => (
                        <Button variant="tag_xs" size="round_xs" className="font-semibold text-xs" key={index}>
                            {tag.toUpperCase()}
                        </Button>
                    ))}
                    {tags.length > 3 && <span className="text-xs text-gray-500 self-center">+{tags.length - 3}</span>}
                </div>
            </div>
        </div>
    );
}
