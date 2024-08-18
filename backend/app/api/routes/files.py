#!/usr/bin/env python3
"""
Defines the route for handling file uploads from the frontend, 
processing them, and storing them in Amazon S3 (AWS). 
Also handles file downloads when requested by the frontend.
"""

from fastapi import APIRouter, status, HTTPException, Depends, File, UploadFile
import os

from app.api.dependencies import get_current_user
from app.models.user import User


file_router = APIRouter()


@file_router.post('/upload_file',
                  status_code=status.HTTP_201_CREATED,
                  response_description='Upload file from frontend')
async def upload_file(
        file: UploadFile = File(...),
        current_user: User = Depends(get_current_user)) -> dict:
    """
    Uploading file from frontend
    storing file in AWS
    """
    try:
        # testing storing file locally
        dir = '/tmp/snapgram_images/'
        os.makedirs(dir, exist_ok=True)
        file_location = os.path.join(dir, file.filename)

        # Save the uploaded file to the specified location
        with open(file_location, "wb") as f:
            f.write(await file.read())

        return {'message': 'File stored locally'}
    except Exception as e:
        return {"error": f"Failed to delete posts: {e}"}
