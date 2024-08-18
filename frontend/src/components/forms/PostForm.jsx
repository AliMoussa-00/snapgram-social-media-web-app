import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { Button } from '@/components/ui/button';
import {
	Form,
	FormControl,
	FormField,
	FormItem,
	FormLabel,
	FormMessage
} from '@/components/ui/form';
import { Textarea } from '@/components/ui/textarea';
import FileUploader from '../shared/FileUploader';
import { Input } from '../ui/input';
import { postValidation } from '@/lib/validation/schemas';
import { useCreatePost } from '@/lib/react-query/queries';
import { useNavigate } from 'react-router-dom';
import { useToast } from '../ui/use-toast';
import { useUserContext } from '@/context/AuthContext';

// if we are updating a post then w will need a post
const PostForm = ({ post }) => {
	const navigate = useNavigate();
	const { toast } = useToast();
	const { user } = useUserContext();
	
	const form = useForm({
		resolver: zodResolver(postValidation),
		defaultValues: {
			caption: post ? post?.caption : "",
			file: [],
			location: post ? post?.location : "",
			tags: post ? post?.tags.join(',') : '',
		}
	});

	//queries
	const { mutateAsync: createPost, isLoading: isLoadingCreate } = useCreatePost();

	const onSubmit = async (values) => {
		try{
			// ACTION = CREATE
			await createPost({
				...values,
				userId: user.id,
			});

			navigate("/");
		}
		catch (error) {
			toast({
				title: `Creating post failed. Please try again.`,
			});
			return;
		}
	}
	return (
		<Form {...form}>
			<form
				onSubmit={form.handleSubmit(onSubmit)}
				className="flex flex-col w-full max-w-5xl gap-9"
			>
				<FormField
					control={form.control}
					name="caption"
					render={({ field }) =>
						<FormItem>
							<FormLabel className="shad-form_label">Caption</FormLabel>
							<FormControl>
								<Textarea
									className="shad-textarea custom-scrollbar"
									{...field}
								/>
							</FormControl>
							<FormMessage className="shad-form_message" />
						</FormItem>}
				/>
				<FormField
					control={form.control}
					name="file"
					render={({ field }) =>
						<FormItem>
							<FormLabel className="shad-form_label">Add Photos</FormLabel>
							<FormControl>
                <FileUploader
                  fieldChange={ field.onChange }
                  mediaUrl= { post?.mediaUrl}
                />
							</FormControl>
							<FormMessage className="shad-form_message" />
						</FormItem>}
				/>
				<FormField
					control={form.control}
					name="location"
					render={({ field }) =>
						<FormItem>
							<FormLabel className="shad-form_label">Add Location</FormLabel>
							<FormControl>
								<Input className="shad-input" {...field} />
							</FormControl>
							<FormMessage className="shad-form_message" />
						</FormItem>}
				/>
				<FormField
					control={form.control}
					name="tags"
					render={({ field }) =>
						<FormItem>
							<FormLabel className="shad-form_label">
								Add Tags (separated by comma " , ")
							</FormLabel>
							<FormControl>
								<Input
									className="shad-input"
									type="text"
									placeholder="Art, Sport, Learning"
									{...field}
								/>
							</FormControl>
							<FormMessage className="shad-form_message" />
						</FormItem>}
				/>
				<div className="flex gap-4 items-center justify-end">
					<Button type="button" className="shad-button_dark_4">
						Cancel
					</Button>
					<Button
						type="submit"
						className="shad-button_primary whitespace-nowrap"
					>
						Submit
					</Button>
				</div>
			</form>
		</Form>
	);
};

export default PostForm;
