import { ReactNode } from 'react';
import { cn } from '@/lib/utils';
import { Card } from '@/components/ui/card';
import { ExternalLink } from 'lucide-react';

interface AdminCardProps extends React.HTMLAttributes<HTMLDivElement> {
    imageUrl: string;
    imageAlt: string;
    title: string;
    subtitle: string;
    tierColor?: string;
    tierBgColor?: string;
    position?: string;
    linkedinUrl?: string;
    actions?: ReactNode;
}

export function AdminCard({
    imageUrl,
    imageAlt,
    title,
    subtitle,
    tierColor,
    tierBgColor,
    position,
    linkedinUrl,
    actions,
    className,
    ...rest
}: AdminCardProps) {
    return (
        <Card 
            className={cn('overflow-hidden flex flex-col h-full border-0', className)}
            {...rest}
        >
            <div className="relative h-48 w-full bg-white/5 p-6 flex items-center justify-center overflow-hidden">
                <div 
                    className={cn(
                        "absolute inset-0 opacity-10 pointer-events-none", 
                        tierBgColor
                    )} 
                />
                
                <img
                    src={imageUrl}
                    alt={imageAlt}
                    className="max-h-full max-w-full object-contain relative z-10 transition-transform duration-500 hover:scale-110"
                />
            </div>

            <div className="flex flex-col flex-grow p-6 space-y-4">
                <div className="flex justify-between items-start gap-4">
                    <div>
                        <h3 className="text-xl font-bold text-white mb-1">{title}</h3>
                        
                        <div className="flex flex-wrap gap-2 mt-2">
                            <span
                                className={cn(
                                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wide shadow-sm',
                                    'bg-gray-100 text-gray-800', 
                                    tierBgColor, 
                                    tierColor   
                                )}
                            >
                                {subtitle}
                            </span>

                            {position && (
                                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-500/10 text-green-400 border border-green-500/20">
                                    {position}
                                </span>
                            )}
                        </div>
                    </div>
                </div>

                {linkedinUrl && (
                    <a
                        href={linkedinUrl}
                        target="_blank"
                        rel="noreferrer"
                        className="flex items-center text-sm text-gray-400 hover:text-white transition-colors group/link w-fit"
                    >
                        <span className="truncate max-w-[200px]">{linkedinUrl.replace(/^https?:\/\//, '')}</span>
                        <ExternalLink className="w-3 h-3 ml-2 opacity-0 -translate-x-2 group-hover/link:opacity-100 group-hover/link:translate-x-0 transition-all" />
                    </a>
                )}

                <div className="flex-grow" />

                {actions && <div className="pt-2">{actions}</div>}
            </div>
        </Card>
    );
}