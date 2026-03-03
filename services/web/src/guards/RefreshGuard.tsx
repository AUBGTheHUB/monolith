import { useEffect } from 'react';
import { Outlet } from 'react-router';
import { useAuthStore } from '@/hooks/useAuthStore';
import { Loader2 } from 'lucide-react';
import { Styles } from '../website/AdminPanelPage/AdminStyle.ts';
import { cn } from '@/lib/utils';

export const RefreshGuard = () => {
    const isInitialized = useAuthStore((state) => state.isInitialized);
    const initialize = useAuthStore((state) => state.initialize);

    useEffect(() => {
        initialize();
    }, [initialize]);

    if (!isInitialized) {
        return (
            <div
                className={cn(
                    'flex flex-col items-center justify-center min-h-screen w-full',
                    Styles.backgrounds.primaryGradient,
                )}
            >
                <div className="relative flex items-center justify-center">
                    {/* Outer glowing ring */}
                    <div
                        className="absolute inset-0 rounded-full blur-xl opacity-20 animate-pulse"
                        style={{ backgroundColor: Styles.colors.hubCyan }}
                    ></div>

                    {/* The Spinner */}
                    <Loader2
                        className="w-12 h-12 animate-spin transition-all"
                        style={{ color: Styles.colors.hubCyan }}
                    />
                </div>

                <p className="mt-4 text-white/60 font-mono text-sm tracking-widest uppercase animate-pulse">
                    Verifying Session
                </p>
            </div>
        );
    }

    return <Outlet />;
};
