import * as React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './card';
import { cn } from '@/lib/utils';

interface AdminCardProps extends React.HTMLAttributes<HTMLDivElement> {
    imageUrl?: string;
    imageAlt?: string;
    title: string;
    subtitle?: string;
    actions?: React.ReactNode;
}

const AdminCard = React.forwardRef<HTMLDivElement, AdminCardProps>(
    ({ className, imageUrl, imageAlt, title, subtitle, actions, ...props }, ref) => (
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
                    {imageUrl && (
                        <div className="relative group">
                            <div className="absolute inset-0 rounded-full bg-[#00B2FF]/20 blur-xl group-hover:bg-[#00B2FF]/40 transition-colors" />
                            <img
                                src={imageUrl}
                                alt={imageAlt || title}
                                className="relative w-32 h-32 rounded-full object-cover border-2 border-white/20 shadow-lg mb-4"
                            />
                        </div>
                    )}
                    <CardTitle className="text-xl text-center text-white">{title}</CardTitle>
                    {subtitle && <p className="text-sm text-blue-200/60 text-center mt-1 font-medium">{subtitle}</p>}
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
