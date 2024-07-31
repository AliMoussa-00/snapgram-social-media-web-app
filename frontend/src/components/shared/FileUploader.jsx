import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';

const FileUploader = ({fieldChange, mediaUrl}) => {
	const [file, setFile] = useState([]);
	const [fileUrl, setFileUrl] = useState();

	const onDrop = useCallback(acceptedFiles => {
        setFile(acceptedFiles);
        fieldChange(acceptedFiles);
        setFileUrl(URL.createObjectURL(acceptedFiles[0]));
	}, [file]);
    const { getRootProps, getInputProps } = useDropzone({
        onDrop,
        accept: {'image/*': ['.png', '.jpeg', '.jpg', '.svg']}
    });

	return (
		<div {...getRootProps()}
			className="flex flex-col flex-center bg-dark-3 rounded-xl cursor-pointer"
		>
			<input {...getInputProps()} className="cursor-pointer" />
			{fileUrl
                ? (
                    <>
                    <div className='flex flex-1 justify-center w-full p-5 lg:p-10'>
                        <img
                            src={fileUrl}
                            alt='uploaded-image'
                            className='file_uploader-image'
                        />
                    </div>
                    <p className='file_uploader-label'>Click or drag photo to replace</p>
                    </>
                )
                : (
                    <div className="file_uploader-box">
                        <img
                            src='/assets/icons/file-upload.svg'
                            width={96}
                            height={77}
                            alt='file-upload'
                        />
                        <h3 className='base-medium text-light-2 mb-2 mt-6'>Drag photo here</h3>
                        <p className='text-light-4 small-regular mb-6'>SVG, PNG, JPG</p>
                    </div>
                )
            }
		</div>
	);
};

export default FileUploader;
