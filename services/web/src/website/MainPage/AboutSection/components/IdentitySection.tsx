import React from 'react';
import identityProposition from '../StaticContent/identityProposition.json';
import { Button } from '@/components/ui/button.tsx';

const IdentitySection: React.FC = () => {
    return (
        <div className="mb-40">
            <h1 className="font-mont font-semibold text-3xl text-primary mb-10">Who are we?</h1>
            <p className="font-hank mb-10">{identityProposition.message}</p>
            <Button variant="outline_mono" size="round_sm">
                Meet the Team
            </Button>
        </div>
    );
};

export default IdentitySection;
