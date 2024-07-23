import { useMutation, useQuery } from '@tanstack/react-query';
import { QUERY_KEYS } from './queryKeys';

import { createUserAccount, getUser, signInAccount } from '../api/requests';

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
