import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { QUERY_KEYS } from './queryKeys';

import {
	createPost,
	createUserAccount,
	getUser,
	signInAccount,
	signOutAccount
} from '../api/requests';

// ============================================================
// USER QUERIES
// ============================================================
export const useGetUser = () => {
	return useQuery({
		queryKey: [QUERY_KEYS.GET_USER],
		queryFn: () => getUser()
	});
};

export const useCreateUserAccount = () => {
	return useMutation({
		mutationFn: newUser => createUserAccount(newUser)
	});
};

export const useSignInAccount = () => {
	return useMutation({
		mutationFn: userCredential => signInAccount(userCredential)
	});
};

export const useSignOutAccount = () => {
	return useMutation({
		mutationFn: () => signOutAccount()
	});
};
// ============================================================
// POST QUERIES
// ============================================================

export const useCreatePost = () => {
	const queryClient = useQueryClient();
	return useMutation({
		mutationFn: (post) => createPost(post),
		onSuccess: () => {
			// queryClient.invalidateQueries({
			// 	queryKey: [QUERY_KEYS.GET_RECENT_POSTS]
			// });
		}
	});
}