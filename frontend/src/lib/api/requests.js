import { AUTH_ROUTE, TOKEN_OBJECT } from './constants';

export async function getUser() {
	const tokenObject = JSON.parse(localStorage.getItem(TOKEN_OBJECT));
	const accessToken = tokenObject.access_token;
	// I need to use the refresh token and the token type

	try {
		const response = await fetch(`${AUTH_ROUTE}/me`, {
			method: 'GET',
			headers: {
				Authorization: `Bearer ${accessToken}`,
				'Content-Type': 'application/json'
			}
		});

		if (!response.ok) {
			throw new Error();
		}

		const data = await response.json();
		return data;
	} catch (error) {
		console.error(`Error in 'getUser': ${error}`);
		throw error; // Throw the error so it can be caught in checkAuthUser
	}
}

export async function createUserAccount(newUser) {
	const u = JSON.stringify({
		username: newUser.username,
		email: newUser.email,
		password: newUser.password,
		full_name: newUser.name
	});
	console.log(`newUSER==>>> ${u}`);
	try {
		const response = await fetch(`${AUTH_ROUTE}/register`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				username: newUser.username,
				email: newUser.email,
				password: newUser.password,
				full_name: newUser.name
			})
		});
		if (!response.ok) {
			throw new Error(response.status);
		}

		const token = response.json();
		return token;
		// localStorage.setItem(TOKEN_OBJECT, JSON.stringify(data));
	} catch (error) {
		console.error(`Error in 'createUserAccount': ${error}`);
		throw error;
	}
}
