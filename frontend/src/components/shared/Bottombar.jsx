import { useUserContext } from '@/context/AuthContext';
import { bottombarLinks } from '@/lib/constants';
import { Link, NavLink, useLocation, useNavigate } from 'react-router-dom';

const Bottombar = () => {
	const { user } = useUserContext();
	const { pathname } = useLocation();

	return (
		<section className="bottom-bar">
			{bottombarLinks.map(link => {
				const isActive = pathname === link.route;
				return (
					<Link
						to={link.route}
						key={link.label}
						className={`${isActive &&
							'bg-primary-500 rounded-[10px]'} flex-center flex-col p-2 transition`}
					>
						<img
							src={link.imgURL}
							alt={link.label}
							width={16}
							height={16}
							className={`${isActive && 'invert-white'}`}
						/>
						<p className="tiny-medium text-light-2">
							{link.label}
						</p>
					</Link>
				);
			})}
		</section>
	);
};

export default Bottombar;
