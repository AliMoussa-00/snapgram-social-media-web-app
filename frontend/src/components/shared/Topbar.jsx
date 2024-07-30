import { Link, useNavigate } from 'react-router-dom';
import { Button } from '../ui/button';
import { useSignOutAccount } from '@/lib/react-query/queries';
import { useEffect } from 'react';
import { useToast } from '../ui/use-toast';
import { useUserContext } from '@/context/AuthContext';

const Topbar = () => {
	const toast = useToast();
	const navigate = useNavigate();
	const { user } = useUserContext();
	const { mutateAsync: signOutAccount, isSuccess } = useSignOutAccount();

	const signOut = async () => {
		try {
			await signOutAccount();
		} catch (error) {
			console.error(`Topbar Sign out failed ${error}`);
			toast({ title: 'Something went wrong. Please try again!' });
		}
	};

	useEffect(
		() => {
			if (isSuccess) {
				navigate(0);
			}
		},
		[navigate, isSuccess]
	);
	return (
		<section className="topbar">
			<div className="flex-between py-4 px-5">
				<Link to="/" className="flex gap-3 items-center">
					<img
						src="/assets/images/logo.svg"
						alt="logo"
						width={130}
						height={325}
					/>
				</Link>

				<div className="flex gap-4">
					<Button
						variant="ghost"
						className="shad-button_ghost"
						onClick={signOut}
					>
						<img src="/assets/icons/logout.svg" alt="logout" />
					</Button>

					<Link to={`/profile/${user.id}`} className="flex-center gap-3">
						<img
							src={user.imageUrl || '/assets/icons/profile-placeholder.svg'}
							alt="profile"
							className="h-8 w-8 rounded-full"
						/>
					</Link>
				</div>
			</div>
		</section>
	);
};

export default Topbar;
