import React from 'react';
import identityProposition from '../StaticContent/identityProposition.json';
import { Button } from '@/components/ui/button.tsx';

export default function IdentitySection() {
    return (
        <div className="mb-32">
            <h2 className="font-mont font-semibold text-3xl text-primary mb-10">Who are we?</h2>
            <p className="font-hank mb-10">{identityProposition.message}</p>
            <Button variant="outline_mono" size="round_sm">
                Meet the Team
            </Button>
        </div>
    );
}
