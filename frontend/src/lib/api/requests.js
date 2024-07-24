import apiClient from './axios';

export async function getUser() {
	try {
		const response = await apiClient.get('/auth/me');

		return response.data;
	} catch (error) {
		console.error(`Error in 'getUser': ${error}`);
		throw error; // Throw the error so it can be caught in checkAuthUser
	}
}

export async function createUserAccount(newUser) {
	try {
		const response = await apiClient.post('/auth/register', {
			username: newUser.username,
			email: newUser.email,
			password: newUser.password,
			full_name: newUser.name
		});

		const token = response.data;
		return token;
	} catch (error) {
		console.error(`Error in 'createUserAccount': ${error}`);
		const errorObject = {
			statusCode: error.response.status,
			message: error.response.data.detail
		};
		throw errorObject;
	}
}

export async function signInAccount(userCredential) {
	try {
		const response = await apiClient.post(
			'/auth/login',
			new URLSearchParams({
				username: userCredential.email,
				password: userCredential.password
			}),
			{
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded'
				}
			}
		);

		const tokenObject = response.data;
		return tokenObject;
	} catch (error) {
		console.error(`Error in 'signInAccount': ${error}`);
		throw error;
	}
}
