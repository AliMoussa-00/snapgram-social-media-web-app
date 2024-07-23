import { useUserContext } from '@/context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { useCreateUserAccount } from '@/lib/react-query/queries';

import { useForm } from 'react-hook-form';
import { Link } from 'react-router-dom';
import { zodResolver } from '@hookform/resolvers/zod';
import {
	Form,
	FormControl,
	FormField,
	FormItem,
	FormLabel,
	FormMessage
} from '@/components/ui/form';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import Loader from '@/components/shared/Loader';

import { signUpValidation } from '@/lib/validation/schemas';
import { TOKEN_OBJECT } from '@/lib/api/constants';

const SignupForm = () => {
	const navigate = useNavigate();
	const { checkAuthUser, isLoading: isUserLoading } = useUserContext();

	// Queries
	const {
		mutateAsync: createUserAccount,
		isLoading: isCreatingAccount
	} = useCreateUserAccount();

	// defining the form
	const form = useForm({
		resolver: zodResolver(signUpValidation),
		defaultValues: {
			name: '',
			username: '',
			email: '',
			password: ''
		}
	});

	// set function to "async"
	const onSubmit = async values => {
		try {
			const tokenObject = await createUserAccount(values);
			if (!tokenObject) throw new Error('createUserAccount Failed');

			localStorage.setItem(TOKEN_OBJECT, JSON.stringify(tokenObject));

			const isLoggedIn = await checkAuthUser();
			if (isLoggedIn) {
				form.reset();
				navigate('/');
			} else {
				console.error('isLoggedIn Failed!! <useToast>');
				return;
			}
		} catch (error) {
			console.error(`SignUp Form error: ${error}`);
			if (error.message === '400') {
				form.setError('email', { message: 'Email already exists' });
			}
		}
	};

	return (
		<Form {...form}>
			<div className="sm:w-420 flex-center flex-col mt-12">
				<img src="/assets/images/logo.svg" />

				<h2 className="h3-bold md:h2-bold pt-5 ">Create a new account</h2>

				<p className="text-light-3 small-medium md:base-regular mt-2">
					To use Snapgram please enter your details.
				</p>

				<form
					onSubmit={form.handleSubmit(onSubmit)}
					className="flex flex-col gap-5 w-full mt-4"
				>
					<FormField
						control={form.control}
						name="name"
						render={({ field }) =>
							<FormItem>
								<FormLabel>Name</FormLabel>
								<FormControl>
									<Input type="text" className="shad-input" {...field} />
								</FormControl>
								<FormMessage />
							</FormItem>}
					/>
					<FormField
						control={form.control}
						name="username"
						render={({ field }) =>
							<FormItem>
								<FormLabel>Username</FormLabel>
								<FormControl>
									<Input type="text" className="shad-input" {...field} />
								</FormControl>
								<FormMessage />
							</FormItem>}
					/>
					<FormField
						control={form.control}
						name="email"
						render={({ field }) =>
							<FormItem>
								<FormLabel>Email</FormLabel>
								<FormControl>
									<Input type="email" className="shad-input" {...field} />
								</FormControl>
								<FormMessage />
							</FormItem>}
					/>
					<FormField
						control={form.control}
						name="password"
						render={({ field }) =>
							<FormItem>
								<FormLabel>Password</FormLabel>
								<FormControl>
									<Input type="password" className="shad-input" {...field} />
								</FormControl>
								<FormMessage />
							</FormItem>}
					/>
					<Button type="submit" className="shad-button_primary">
						{isUserLoading || isCreatingAccount
							? <div className="flex-center gap-2">
									{' '}<Loader /> Loading...
								</div>
							: 'Sign up'}
					</Button>

					<p className="text-small-regular text-light-2 text-center mt-2">
						Already have an account ?
						<Link
							to="/sign-in"
							className="text-primary-500 text-small-semibold ml-1"
						>
							Login
						</Link>
					</p>
				</form>
			</div>
		</Form>
	);
};

export default SignupForm;
