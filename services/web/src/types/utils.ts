import { z } from 'zod';

export const zDateTime = z.string().refine((val) => {
    const date = val.split(' ')[0];
    const time = val.split(' ')[1];

    const zDate = z.string().date()
    const zTime= z.string().time()

    return zDate.safeParse(date) && zTime.safeParse(time)
});
