import * as React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { cn } from '@/utils';

interface AdminCardProps extends React.HTMLAttributes<HTMLDivElement> {
    imageUrl?: string;
    imageAlt?: string;
    title: string;
    subtitle?: string;
    position?: string;
    linkedinUrl?: string;
    actions?: React.ReactNode;
}

const AdminCard = React.forwardRef<HTMLDivElement, AdminCardProps>(
    ({ className, imageUrl, imageAlt, title, subtitle, position, linkedinUrl, actions, ...props }, ref) => (
        <Card
            ref={ref}
            className={cn(
                'overflow-hidden transition-all duration-300',
                'bg-white/5 backdrop-blur-md border-white/10 hover:border-white/20 hover:bg-white/10',
                'shadow-xl shadow-black/20',
                className,
            )}
            {...props}
        >
            <CardHeader className="p-6">
                <div className="flex flex-col items-center">
                    <CardTitle className="text-xl text-center text-white mb-4">{title}</CardTitle>

                    {imageUrl && (
                        <div className="relative group mb-4">
                            <div className="absolute inset-0 rounded-full bg-[#00B2FF]/20 blur-xl group-hover:bg-[#00B2FF]/40 transition-colors" />
                            <img
                                src={imageUrl}
                                alt={imageAlt || title}
                                className="relative w-32 h-32 rounded-full object-cover border-2 border-white/20 shadow-lg"
                            />
                        </div>
                    )}

                    {subtitle && <p className="text-sm text-white/80 text-center font-semibold mt-1">{subtitle}</p>}

                    {position && <p className="text-sm text-blue-200/60 text-center mt-1 font-medium">{position}</p>}

                    {linkedinUrl && (
                        <a
                            href={linkedinUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-xs text-[#0077B5] hover:text-[#00A0DC] hover:underline mt-3 transition-colors"
                        >
                            LinkedIn Profile
                        </a>
                    )}
                </div>
            </CardHeader>

            {actions && (
                <CardContent className="p-4 flex gap-2 bg-black/20 border-t border-white/5">{actions}</CardContent>
            )}
        </Card>
    ),
);
AdminCard.displayName = 'AdminCard';

export { AdminCard };
