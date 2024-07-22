import { useUserContext } from '@/context/AuthContext';

const RootLayout = () => {
	const { user } = useUserContext();
	console.log(`User: ${JSON.stringify(user)}`);

	return <div>RootLayout</div>;
};

export default RootLayout;
