import { useCallback, useEffect, useRef, useState } from 'react';

export function useCooldownTimer(durationSeconds: number) {
    const [secondsLeft, setSecondsLeft] = useState(0);
    const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

    const start = useCallback(() => {
        setSecondsLeft(durationSeconds);

        if (intervalRef.current) {
            clearInterval(intervalRef.current);
        }

        intervalRef.current = setInterval(() => {
            setSecondsLeft((prev) => {
                if (prev <= 1) {
                    clearInterval(intervalRef.current!);
                    intervalRef.current = null;
                    return 0;
                }
                return prev - 1;
            });
        }, 1000);
    }, [durationSeconds]);

    useEffect(() => {
        return () => {
            if (intervalRef.current) {
                clearInterval(intervalRef.current);
            }
        };
    }, []);

    const isCoolingDown = secondsLeft > 0;

    return { secondsLeft, isCoolingDown, start };
}
