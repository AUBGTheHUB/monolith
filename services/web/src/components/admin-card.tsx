import * as React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
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
        <Card ref={ref} className={cn('overflow-hidden hover:shadow-lg transition-shadow', className)} {...props}>
            <CardHeader className="bg-gradient-to-br from-blue-50 to-white p-6">
                <div className="flex flex-col items-center">
                    {imageUrl && (
                        <img
                            src={imageUrl}
                            alt={imageAlt || title}
                            className="w-32 h-32 rounded-full object-cover border-4 border-white shadow-lg mb-4"
                        />
                    )}
                    <CardTitle className="text-xl text-center">{title}</CardTitle>
                    {subtitle && <p className="text-sm text-gray-600 text-center mt-1">{subtitle}</p>}
                </div>
            </CardHeader>
            {actions && <CardContent className="p-4 flex gap-2">{actions}</CardContent>}
        </Card>
    ),
);
AdminCard.displayName = 'AdminCard';

export { AdminCard };
