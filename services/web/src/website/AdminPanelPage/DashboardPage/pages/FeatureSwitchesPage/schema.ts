import { z } from "zod";

export const featureSwitchSchema = z.object({
  name: z
    .string()
    .trim()
    .min(2, { message: "Name must be at least 2 characters." })
    .max(12, { message: "Name must be at most 12 characters." }),
});

export type FeatureSwitchForm = z.infer<typeof featureSwitchSchema>;
