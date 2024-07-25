import { useForm } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
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

import { signUpValidation } from '@/lib/validation/schemas';
import Loader from '@/components/shared/Loader';
import { useUserContext } from '@/context/Authcontext';
import { useCreateUserAccount } from '@/lib/react-query/queries';
import { useToast } from '@/components/ui/use-toast';


const SignupForm = () => {
	const { toast } = useToast()
	const navigate = useNavigate()
	// Queries
	const { mutateAsync: createUserAccount, isLoading: isCreatingAccount } = useCreateUserAccount();
	const {checkAuthUser, isLoading: isUserLoading} = useUserContext()
	
	// defining the form
	const form = useForm({
		resolver: zodResolver(signUpValidation),
		defaultValues: {
			full_name: '',
			email: '',
			username: '',
			password: ''
		}
	});

	
	// set function to "async"
	const onSubmit = async (values) => {
		try {
			await createUserAccount(values)
		
			// setUser(newUser)
			const isLoggedIn = await checkAuthUser()
			if (isLoggedIn) {
				form.reset()
				navigate("/")
			}
			else {
				toast({ 
					title: "Sign up failed.",
					description: "Please try again.",
				 });
			}
		}
		catch (error) {
			if (error.response) {
				const message = error.response.data.detail;
				if (message === "Email already registered") {
					toast({
						title: "Email Already Registered.",
						description: "The email you entered is already in use. Please use a different email address.",
					});
				}
				else if (message === "username already registered") {
					toast({
						title: "Username Already Taken",
						description: "The username you entered is already in use. Please choose a different username.",
					});
				}
				else {
					toast({
						title: "Sign up failed.",
						description: "Please try again.",
					})
				}
			}
			else {
				toast({
					title: "Sign up failed.",
					description: "Network error or unexpected issue. Please try again.",
				})
			}
		}
	}

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
						name="full_name"
						render={({ field }) =>
							<FormItem>
								<FormLabel>Full Name</FormLabel>
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
						{isCreatingAccount || isUserLoading
							? (<div className="flex-center gap-2"> <Loader/> Loading...</div>)
							: ("Sign up")}
					</Button>

					<p className="text-small-regular text-light-2 text-center mt-2">
						Already have an account ?
						<Link
							to="/sign-in"
							className="text-primary-500 text-small-semibold ml-1"
						>
							Log in
						</Link>
					</p>
				</form>
			</div>
		</Form>
	);
};

export default SignupForm;
