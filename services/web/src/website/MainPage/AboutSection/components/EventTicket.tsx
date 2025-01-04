import { Button } from '@/components/ui/button.tsx';

export default function EventTicket({ imgSrc, title, tags }: { imgSrc: string; title: string; tags: Array<string> }) {
    return (
        <div className="flex flex-col min-w-50 max-w-80 h-60 p-2 border rounded-2xl font-semibold">
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
