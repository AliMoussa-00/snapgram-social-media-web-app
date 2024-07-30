import AuthLayout from './_auth/AuthLayout';
import RootLayout from './_root/RootLayout';
import SigninForm from './_auth/forms/SigninForm';
import SignupForm from './_auth/forms/SignupForm';
import './globals.css';
import { Routes, Route } from 'react-router-dom';
import { Toaster } from '@/components/ui/toaster';

import {
	AllUsers,
	CreatePost,
	EditPost,
	Explore,
	Home,
	PostDetail,
	Profile,
	Saved,
	UpdateProfile
} from './_root/pages/index.js';

const App = () => {
	return (
		<main className="flex h-screen">
			<Routes>
				{/* Public Routes */}
				<Route element={<AuthLayout />}>
					<Route path="/sign-in" element={<SigninForm />} />
					<Route path="/sign-up" element={<SignupForm />} />
				</Route>

				{/* Private Routes */}
				<Route element={<RootLayout />}>
					<Route index element={<Home />} />
					<Route path="/explore" element={<Explore />} />
					<Route path="/saved" element={<Saved />} />
					<Route path="/create-post" element={<CreatePost />} />
					<Route path="/posts/:id" element={<PostDetail />} />
					<Route path="/update-post/:id" element={<EditPost />} />
					<Route path="/all-users" element={<AllUsers />} />
					<Route path="/profile/:id" element={<Profile />} />
					<Route path="/update-profile/:id" element={<UpdateProfile />} />
				</Route>
			</Routes>

			<Toaster />
		</main>
	);
};

export default App;
