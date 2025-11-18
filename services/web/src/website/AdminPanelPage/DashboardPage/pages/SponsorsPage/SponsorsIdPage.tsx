'use client';

import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { useEffect, useState } from 'react';
import sponsors from './sponsors.json';
import { useParams, useNavigate } from 'react-router';

type Sponsor = { id: number; name?: string; image?: string; website?: string; link?: string };

export default function EditSponsorPage() {
    const params = useParams();
    const sponsorId = Number((params as unknown as { id?: string })?.id);

    const [localSponsor, setLocalSponsor] = useState<Sponsor | null>(null);
    const navigate = useNavigate();

    useEffect(() => {
        try {
            const stored = localStorage.getItem('sponsors');
            const list = stored ? JSON.parse(stored) : sponsors;
            const found = (list as Sponsor[]).find((s) => s.id === sponsorId);
            setLocalSponsor(found || null);
        } catch {
            setLocalSponsor((sponsors as Sponsor[]).find((s) => s.id === sponsorId) || null);
        }
    }, [sponsorId]);

    const [form, setForm] = useState({
        name: '',
        image: '',
        link: '',
    });

    useEffect(() => {
        const sponsor = localSponsor || (sponsors as Sponsor[]).find((s) => s.id === sponsorId);
        if (sponsor) {
            setForm({
                name: sponsor.name || '',
                image: sponsor.image || '',
                link: (sponsor as Sponsor).link || (sponsor as Sponsor).website || '',
            });
        }
    }, [localSponsor, sponsorId]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async () => {
        if (form.name.length < 2 || form.name.length > 50) {
            alert('Name must be between 2 and 50 characters.');
            return;
        }

        try {
            const stored = localStorage.getItem('sponsors');
            const list = stored ? JSON.parse(stored) : sponsors;
            const updated = (list as Sponsor[]).map((s) =>
                s.id === sponsorId ? { ...s, name: form.name, image: form.image, website: form.link } : s,
            );
            localStorage.setItem('sponsors', JSON.stringify(updated));
            navigate('/dashboard/sponsors');
        } catch (e) {
            console.error(e);
        }
    };

    const sponsor = localSponsor;

    if (!sponsor) return <div className="p-8">Sponsor not found.</div>;

    return (
        <div className="p-8 min-h-screen bg-gray-50 text-gray-900 flex items-start justify-center">
            <div className="w-full max-w-md bg-white p-6 rounded-lg shadow-md">
                <h1 className="text-2xl font-bold mb-6">Edit sponsor</h1>
                <div className="flex flex-col gap-4">
                    <div>
                        <Label htmlFor="name">Name</Label>
                        <Input id="name" name="name" value={form.name} onChange={handleChange} />
                    </div>

                    <div>
                        <Label htmlFor="image">Image URL</Label>
                        <Input id="image" name="image" value={form.image} onChange={handleChange} />
                    </div>

                    <div>
                        <Label htmlFor="link">Link</Label>
                        <Input id="link" name="link" value={form.link} onChange={handleChange} />
                    </div>

                    <Button className="mt-4 w-full bg-blue-600 text-white hover:bg-blue-700" onClick={handleSubmit}>
                        Save Changes
                    </Button>
                </div>
            </div>
        </div>
    );
}
