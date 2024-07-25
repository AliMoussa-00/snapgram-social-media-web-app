import axios from 'axios';
import { MAIN_ROUTE } from './constants';

const apiClient = axios.create({
	baseURL: MAIN_ROUTE,
	headers: {
		'Content-Type': 'application/json'
	}
});

apiClient.interceptors.request.use(
	config => {
		const tokenObject = JSON.parse(localStorage.getItem('Token'));
		if (tokenObject) {
			config.headers.Authorization = `Bearer ${tokenObject.access_token}`;
		}
		return config;
	},
	error => {
		return Promise.reject(error);
	}
);

apiClient.interceptors.response.use(
	response => {
		return response;
	},
	async error => {
		const originalRequest = error.config;
		if (error.response.status === 401 && !originalRequest._retry) {
			// set the previous request to repeat once again
			originalRequest._retry = true;

			const tokenObject = JSON.parse(localStorage.getItem('Token'));
			if (tokenObject) {
				try {
					const response = await axios.post(
						`${MAIN_ROUTE}/auth/refresh-token`,
						{
							refresh_token: tokenObject.refresh_token
						}
					);

					const newTokenObject = response.data;
					localStorage.setItem('Token', JSON.stringify(newTokenObject));

					// all coming axios requests will use new access token in header
					axios.defaults.headers.common[
						'Authorization'
					] = `Bearer ${newTokenObject.access_token}`;

					// The previous requests will use new access token in header
					originalRequest.headers[
						'Authorization'
					] = `Bearer ${newTokenObject.access_token}`;

					return axios(originalRequest);
				} catch (error) {
					console.error(`refresh token Failed ${error}`);
				}
			}
		}
		return Promise.reject(error);
	}
);

export default apiClient;