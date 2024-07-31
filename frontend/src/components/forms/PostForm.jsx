import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { Button } from '@/components/ui/button';
import {
	Form,
	FormControl,
	FormDescription,
	FormField,
	FormItem,
	FormLabel,
	FormMessage
} from '@/components/ui/form';
import { Textarea } from '@/components/ui/textarea';
import FileUploader from '../shared/FileUploader';
import { Input } from '../ui/input';

const formSchema = z.object({
	username: z.string().min(2).max(50)
});

// if we are updating a post then w will need a post
const PostForm = ({post}) => {
	const form = useForm({
		resolver: zodResolver(formSchema),
		defaultValues: { username: '' }
	});

	function onSubmit(values) {
		console.log(values);
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
								<Input className="shad-input" />
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
