import { Button } from '@/components/ui/button.tsx';

type EventTicketType = {
    imgSrc: string;
    title: string;
    tags: Array<string>;
};

export default function EventTicket({ imgSrc, title, tags }: EventTicketType) {
    return (
        <div className="flex flex-col min-w-50 max-w-80 max-[450px]:max-w-full h-60 p-2 border rounded-2xl font-semibold">
            <div className="h-4/6 w-full">
                <img src={imgSrc} alt="" className="object-cover w-full h-full rounded-xl" />
            </div>
            <div className="h-2/6 py-3 flex flex-col gap-2">
                <h3 className="text-primary">{title}</h3>
                <div className="flex">
                    {tags.map((tag, index) => (
                        <Button variant="tag_xs" size="round_xs" className="font-semibold" key={index}>
                            {tag.toUpperCase()}
                        </Button>
                    ))}
                </div>
            </div>
        </div>
    );
}
