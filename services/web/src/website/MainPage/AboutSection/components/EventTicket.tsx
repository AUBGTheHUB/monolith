import { Button } from '@/components/ui/button.tsx';

type EventTicketProps = {
    imgSrc: string;
    title: string;
    tags?: Array<string>;
    onClick?: () => void;
};

export default function EventTicket({ imgSrc, title, tags, onClick }: EventTicketProps) {
    return (
        <div
            onClick={onClick}
            className={`group flex h-full w-full flex-col overflow-hidden rounded-2xl border bg-white p-2 font-semibold shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md active:scale-[0.99] ${onClick ? 'cursor-pointer' : ''}`}
        >
            <div className="w-full aspect-[4/3] overflow-hidden rounded-xl bg-gray-100">
                <img
                    src={imgSrc}
                    alt={title}
                    className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-[1.03]"
                />
            </div>
            <div className="flex min-h-[7.25rem] flex-col justify-between gap-2 py-3">
                <h3 className="min-h-[3.5rem] text-lg text-primary line-clamp-2" title={title}>
                    {title}
                </h3>
                <div className="flex h-16 flex-wrap content-start gap-2 overflow-hidden">
                    {tags &&
                        tags.slice(0, 3).map((tag, index) => (
                            <Button variant="tag_xs" size="round_xs" className="font-semibold text-xs" key={index}>
                                {tag.toUpperCase()}
                            </Button>
                        ))}
                    {tags && tags.length > 3 && (
                        <span className="text-xs text-gray-500 self-center">+{tags.length - 3}</span>
                    )}
                </div>
            </div>
        </div>
    );
}
