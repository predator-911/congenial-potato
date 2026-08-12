import {z} from 'zod';
export const renameSchema = z.object({original_filename: z.string().min(1).max(160)});
