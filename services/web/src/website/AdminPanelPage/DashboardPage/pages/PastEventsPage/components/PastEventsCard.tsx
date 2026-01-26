import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { PastEventCardProps } from '@/types/past-events';

export const PastEventCard = ({ id, title, image, tags, link }: PastEventCardProps) => (
    <Card className="overflow-hidden transition hover:shadow-md">
        <img src={image} alt={title} width={600} height={300} className="w-full h-48 object-cover" />
        <CardHeader>
            <CardTitle className="text-lg font-semibold">{title}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
            <div className="flex flex-wrap gap-2">
                {tags.map((t) => (
                    <Badge key={t} variant="secondary">
                        {t}
                    </Badge>
                ))}
            </div>
            <div className="flex gap-2">
                {link && (
                    <a href={link} target="_blank" rel="noreferrer">
                        <Button variant="outline" size="sm">
                            View
                        </Button>
                    </a>
                )}
                <a href={`/dashboard/past-events/${id}`}>
                    <Button size="sm" className="border border-white">
                        Edit
                    </Button>
                </a>
            </div>
        </CardContent>
    </Card>
);
