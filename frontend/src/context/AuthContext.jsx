/**
 * Creating the authentication context to be used
 * in the child components
 */
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useState, useEffect, useContext, createContext } from 'react';
import { AUTH_ROUTE } from '@/constants';

const INITIAL_USER = {
	id: '',
	name: '',
	username: '',
	email: '',
	imageUrl: '',
	bio: ''
};

const INITIAL_STATE = {
	user: INITIAL_USER,
	isLoading: false,
	isAuthenticated: false,
	setUser: () => {},
	setIsAuthenticated: () => {},
	checkAuthUser: async () => false
};

/**
 * 'AuthContext' = It serves as a way to pass data through the component tree
 *  without having to pass props down manually at every level.
 */
const AuthContext = createContext(INITIAL_STATE);

/**
 * 'AuthProvider': Implements the logic for managing the context state and provides
 *  these values to its children via AuthContext.Provider.
 */
export function AuthProvider({ children }) {
	const navigate = useNavigate();
	const [user, setUser] = useState(INITIAL_USER);
	const [isAuthenticated, setIsAuthenticated] = useState(false);
	const [isLoading, setIsLoading] = useState(false);

	const checkAuthUser = async () => {
		setIsLoading(true);

		try {
			const accessToken = localStorage.getItem('accessToken');

			axios
				.get(`${AUTH_ROUTE}/me`, {
					headers: {
						Authorization: `Bearer ${accessToken}`,
						'Content-Type': 'application/json'
					}
				})
				.then(response => {
					console.log(`response of '/me' : ${response.data}\n`);
					const {
						_id,
						email,
						username,
						full_name,
						bio,
						profile_picture_url
					} = response.data;

					setUser({
						id: _id,
						username,
						email,
						bio,
						imageUrl: profile_picture_url,
						name: full_name
					});

					setIsAuthenticated(true);
					return true;
				})
				.catch(error => {
					console.error(`Error with headers in GET request: ${error}\n`);
				});
		} catch (error) {
			console.log(`Authentication error: ${error}`);
			return false;
		} finally {
			setIsLoading(false);
		}
	};

	useEffect(() => {
		const accessToken = localStorage.getItem('accessToken');
		if (!accessToken) {
			navigate('/sign-in');
		}
		checkAuthUser();
	}, []);

	// defining the value to be passed to the components
	const value = {
		user,
		isLoading,
		isAuthenticated,
		setUser,
		setIsAuthenticated,
		checkAuthUser
	};

	return (
		<AuthContext.Provider value={value}>
			{children}
		</AuthContext.Provider>
	);
}

export const useUserContext = () => useContext(AuthContext);
