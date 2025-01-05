import { Button } from '@/components/ui/button.tsx';

export default function IdentitySection() {
    return (
        <div className="mb-32">
            <h2 className="font-mont font-semibold text-3xl text-primary mb-10">Who are we?</h2>
            <p className="font-hank mb-10">
                The Hub is a club at the American University in Bulgaria. We are a community of young and ambitious
                students with an interest in software development, engineering, design, and technology. <br></br>
                <br></br> Our belief is that getting together with like-minded individuals to exchange experience and
                ideas is the key ingredient needed to ignite innovation and entrepreneurship into the minds and hearts
                of fellow enthusiasts. This is what truly motivates us to get together, organize events, and encourage
                change.
            </p>
            <Button variant="outline_mono" size="round_sm">
                Meet the Team
            </Button>
        </div>
    );
}
