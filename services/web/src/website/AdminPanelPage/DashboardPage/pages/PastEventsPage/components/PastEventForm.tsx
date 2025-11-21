'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';

export interface PastEventFormData {
    title: string;
    image: string;
    tags: string[];
    link?: string;
}
interface PastEventFormProps {
    defaultValues?: Partial<PastEventFormData>;
    onSubmit: (data: PastEventFormData) => void;
    submitLabel?: string;
}

export const PastEventForm = ({ defaultValues, onSubmit, submitLabel = 'Save' }: PastEventFormProps) => {
    const [title, setName] = useState(defaultValues?.title ?? '');
    const [image, setImage] = useState(defaultValues?.image ?? '');
    const [link, setLink] = useState(defaultValues?.link ?? '');
    const [tags, setTags] = useState<string[]>(defaultValues?.tags ?? []);
    const [tagInput, setTagInput] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (title.length < 3 || title.length > 100) {
            alert('Name must be between 3 and 100 characters');
            return;
        }
        if (tags.length === 0) {
            alert('Please add at least one tag');
            return;
        }
        onSubmit({ title, image, link, tags });
    };

    const addTag = () => {
        if (tagInput.trim() && !tags.includes(tagInput.trim())) {
            setTags([...tags, tagInput.trim()]);
            setTagInput('');
        }
    };

    return (
        <form onSubmit={handleSubmit} className="max-w-xl w-full space-y-5">
            <div>
                <Label>Name</Label>
                <Input
                    value={title}
                    onChange={(e) => setName(e.target.value)}
                    className="text-black"
                    placeholder="Event name"
                    minLength={3}
                    maxLength={100}
                    required
                />
            </div>

            <div>
                <Label>Image URL</Label>
                <Input
                    value={image}
                    onChange={(e) => setImage(e.target.value)}
                    className="text-black"
                    placeholder="/public/example.jpg"
                    required
                />
            </div>

            <div>
                <Label>Tags</Label>
                <div className="flex flex-wrap items-center gap-2 border rounded-md px-3 py-2 bg-transparent focus-within:ring-2 focus-within:ring-white/40">
                    {tags.map((t) => (
                        <Badge
                            key={t}
                            onClick={() => setTags(tags.filter((tag) => tag !== t))}
                            className="cursor-pointer bg-white/10 text-white hover:bg-white/20 transition"
                            variant="secondary"
                        >
                            {t} ✕
                        </Badge>
                    ))}
                    <input
                        className="flex-1 bg-transparent outline-none text-white placeholder-gray-400 min-w-[100px]"
                        value={tagInput}
                        placeholder="Type a tag and press Enter"
                        onChange={(e) => setTagInput(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), addTag())}
                    />
                </div>
            </div>
            <div>
                <Label>Link (optional)</Label>
                <Input
                    value={link}
                    onChange={(e) => setLink(e.target.value)}
                    className="text-black"
                    placeholder="https://thehub-aubg.com/events/example"
                />
            </div>

            <Button type="submit" className="border border-white">
                {submitLabel}
            </Button>
        </form>
    );
};
