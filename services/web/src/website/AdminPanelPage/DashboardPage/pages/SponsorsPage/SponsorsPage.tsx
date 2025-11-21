import { Card, CardFooter, CardContent } from '@/components/ui/card';
import sponsors from './sponsors.json';
import { Button } from '@/components/ui/button';
import { Plus } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router';

export default function SponsorsPage() {
    const navigate = useNavigate();

    const [localSponsors, setLocalSponsors] = useState<typeof sponsors>([]);

    useEffect(() => {
        try {
            const stored = localStorage.getItem('sponsors');
            if (stored) {
                setLocalSponsors(JSON.parse(stored));
            } else {
                localStorage.setItem('sponsors', JSON.stringify(sponsors));
                setLocalSponsors(sponsors);
            }
        } catch {
            setLocalSponsors(sponsors);
        }
    }, []);

    const handleDelete = (id: number) => {
        const updated = localSponsors.filter((s) => s.id !== id);
        setLocalSponsors(updated);
        localStorage.setItem('sponsors', JSON.stringify(updated));
    };

    return (
        <div className="p-8 relative min-h-screen bg-gray-50 text-gray-900">
            <div className="max-w-7xl mx-auto">
                <h1 className="text-3xl font-bold mb-6 text-gray-900">Sponsors</h1>

                <div className="flex flex-wrap -mx-2 gap-6">
                    {localSponsors.map((sponsor) => (
                        <Card
                            key={sponsor.id}
                            className="flex flex-col items-center justify-between rounded-2xl shadow-sm hover:shadow-md transition-all p-4 bg-white text-black w-80 mx-2"
                        >
                            <CardContent className="flex flex-col items-center gap-2 w-full">
                                <div className="w-full h-40 relative rounded-xl overflow-hidden bg-gray-100">
                                    <img
                                        src={sponsor.image}
                                        alt={sponsor.name}
                                        className="object-contain p-2 w-full h-full"
                                    />
                                </div>
                                <div className="text-center font-semibold mt-2 text-gray-900">{sponsor.name}</div>
                            </CardContent>
                            <CardFooter className="flex justify-between w-full gap-2">
                                <Button
                                    variant="destructive"
                                    className="w-1/2 bg-black text-white hover:opacity-90"
                                    onClick={() => handleDelete(sponsor.id)}
                                >
                                    Delete
                                </Button>
                                <Button
                                    variant="secondary"
                                    className="w-1/2 bg-blue-600 text-white hover:bg-blue-700"
                                    onClick={() => navigate(`/dashboard/sponsors/edit/${sponsor.id}`)}
                                >
                                    Edit
                                </Button>
                            </CardFooter>
                        </Card>
                    ))}
                </div>

                <Button
                    className="fixed bottom-8 right-8 rounded-full h-14 w-14 shadow-lg bg-blue-600 text-white hover:bg-blue-700"
                    size="icon"
                    onClick={() => navigate('/dashboard/sponsors/add')}
                >
                    <Plus className="h-6 w-6" />
                </Button>
            </div>
        </div>
    );
}
