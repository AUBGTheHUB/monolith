'use client';

import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { useState } from 'react';
import { useNavigate } from 'react-router';

type Sponsor = { id: number; name?: string; image?: string; website?: string; link?: string };

export default function AddSponsorPage() {
    const [form, setForm] = useState({
        name: '',
        image: '',
        link: '',
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const navigate = useNavigate();

    const handleSubmit = async () => {
        if (form.name.length < 2 || form.name.length > 50) {
            alert('Name must be between 2 and 50 characters.');
            return;
        }

        try {
            const stored = localStorage.getItem('sponsors');
            const list = stored ? JSON.parse(stored) : [];
            const nextId = list.length ? Math.max(...(list as Sponsor[]).map((s) => s.id)) + 1 : 1;
            const newSponsor = { id: nextId, name: form.name, image: form.image, website: form.link };
            const updated = [...list, newSponsor];
            localStorage.setItem('sponsors', JSON.stringify(updated));
            navigate('/dashboard/sponsors');
        } catch {
            console.error('failed to add sponsor');
        }
    };

    return (
        <div className="p-8 min-h-screen bg-gray-50 text-gray-900 flex items-start justify-center">
            <div className="w-full max-w-md bg-white p-6 rounded-lg shadow-md">
                <h1 className="text-2xl font-bold mb-6">Add new sponsor</h1>
                <div className="flex flex-col gap-4">
                    <div>
                        <Label htmlFor="name">Name</Label>
                        <Input
                            id="name"
                            name="name"
                            value={form.name}
                            onChange={handleChange}
                            placeholder="Sponsor name"
                        />
                    </div>

                    <div>
                        <Label htmlFor="image">Image URL</Label>
                        <Input
                            id="image"
                            name="image"
                            value={form.image}
                            onChange={handleChange}
                            placeholder="https://example.com/logo.png"
                        />
                    </div>

                    <div>
                        <Label htmlFor="link">Link</Label>
                        <Input
                            id="link"
                            name="link"
                            value={form.link}
                            onChange={handleChange}
                            placeholder="https://example.com"
                        />
                    </div>

                    <Button className="mt-4 w-full bg-blue-600 text-white hover:bg-blue-700" onClick={handleSubmit}>
                        Add Sponsor
                    </Button>
                </div>
            </div>
        </div>
    );
}
