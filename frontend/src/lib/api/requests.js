import apiClient from './axios';
import { TOKEN_OBJECT } from './constants';

// ============================================================
// USER QUERIES
// ============================================================

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

export async function signOutAccount() {
	try {
		const response = await apiClient.post('/auth/logout');

		if (response.status !== 200) throw new Error('Logout Failed');

		localStorage.removeItem(TOKEN_OBJECT);
	} catch (error) {
		console.error(`signOutAccount Failed: ${error}`);
		throw error;
	}
}

// ============================================================
// POST QUERIES
// ============================================================
export async function uploadFile(file) {
	try {
		const formData = new FormData();
		formData.append('file', file);

		const response = await apiClient.post('/files/upload_file', formData, {
			headers: {
				'Content-Type': 'multipart/form-data'
			}
		});

		console.log('\nUpload File Response:', response.data);

		// return the file_url if success
		return 'file url';
	} catch (error) {
		console.error(`Uploading file error: ${error}`);
	}
}

export async function createPost(post) {
	try {
		const uploadedFileUrl = uploadFile(post.file[0]);
		if (!uploadedFileUrl) throw new Error('Upload File Failed');

		/**
		 * I will need to update the Backend to accept: caption, location and tags
		 * for now i will just a simple request
		 */

		console.log(`uploadedFileUrl: ${uploadedFileUrl}`);
		const response = await apiClient.post('/posts/', {
			user_id: post.userId,
			content: 'Post Contents',
			media_type: 'Image',
			media_url: 'uploadedFileUrl'
		});
		console.log('\nCreate Post Response:', response.data);
	} catch (error) {
		console.error(`Create Post error: ${error}`);
		throw error;
	}
}
