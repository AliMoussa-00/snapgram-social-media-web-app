import { useUserContext } from '@/context/AuthContext';
import { Navigate, Outlet } from 'react-router-dom';

const RootLayout = () => {
	const { user, isAuthenticated } = useUserContext();
	console.log(`User: ${JSON.stringify(user)}`);

	return (
		<>
			{!isAuthenticated ? (
				<Navigate to='/sign-in' />
			) : (
					<>
						<div>RootLayout</div>
				</>
			)}
		</>
	)
};

export default RootLayout;
