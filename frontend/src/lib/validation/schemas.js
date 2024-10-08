/**
 * I will be using 'zod' for validating forms
 */
import { z } from 'zod';

export const signUpValidation = z.object({
	name: z.string().min(2, { message: 'Name is too short' }).max(50),
	username: z.string().min(2).max(50),
	email: z.string().email().min(2).max(50),
	password: z
		.string()
		.min(8, { message: 'Password must be at least 8 characters' })
		.max(50)
});

export const signInValidation = z.object({
	email: z.string().email().min(2).max(50),
	password: z
		.string()
		.min(8, { message: 'Password must be at least 8 characters' })
		.max(50)
});
