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

import Loader from '@/components/shared/Loader';
import { signInValidation } from '@/lib/validation/schemas';
import { useUserContext } from '@/context/Authcontext';
import { useSignInAccount } from '@/lib/react-query/queries';
import { useToast } from '@/components/ui/use-toast';
import { ToastAction } from '@/components/ui/toast';

const SigninForm = () => {
	const { toast } = useToast()
  const navigate = useNavigate()
  // Queries
	const { mutateAsync: signInAccount, isLoading: isSignInAccount} = useSignInAccount();
	const {checkAuthUser, isLoading: isUserLoading} = useUserContext()
  
  // defining the form
  const form = useForm({
      resolver: zodResolver(signInValidation),
      defaultValues: {
          email: '',
          password: ''
      }
  });

  // set function to "async"
  const onSubmit = async (values) => {
    try {
      await signInAccount(values)

      const isLoggedIn = await checkAuthUser()
      if (isLoggedIn) {
        form.reset()
        navigate("/") 
      }
      else {
        toast({
          title: "Login failed",
          description: "Please try again.",
        })
      }      
    }
    catch (error) {
      toast({
        title: "Login failed",
        description: "An unexpected error occurred. Please try again.",
      })
		}
  }
  
  return (
    <Form {...form}>
      <div className="sm:w-420 flex-center flex-col mt-12">
        <img src="/assets/images/logo.svg" />
        <h2 className="h3-bold md:h2-bold pt-5 ">Login to your account</h2>
        
        <p className="text-light-3 small-medium md:base-regular mt-2">
          Welcome back! Please enter you details
        </p>
        <form
          onSubmit={form.handleSubmit(onSubmit)}
          className="flex flex-col gap-5 w-full mt-4"
        >
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
            {isSignInAccount || isUserLoading
              ? (<div className="flex-center gap-2"> {' '}<Loader /> Loading... </div>)
              : ("Log in")}
          </Button>
          <p className="text-small-regular text-light-2 text-center mt-2">
            Don&apos;t have an account ?
            <Link
              to="/sign-up"
              className="text-primary-500 text-small-semibold ml-1"
            >
              Sign up
            </Link>
          </p>
        </form>
      </div>
    </Form>
    );
};

export default SigninForm;