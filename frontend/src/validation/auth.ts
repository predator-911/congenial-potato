import {z} from 'zod';
export const authSchema = z.object({email: z.string().email(), password: z.string().min(10).max(256)});
