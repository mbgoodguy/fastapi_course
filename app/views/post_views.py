# @app.post('/feedback')
# def feedback_handler(feedback: Feedback):
#     feedbacks.append(feedback.message)
#     return {'message': f'Feedback received. Thank you, {feedback.name}'}
#
#
# @app.post("/files/")
# async def create_file(file: Annotated[bytes, File()]):
#     return {"file_size": len(file), "filename": file.filename}
#
#
# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):
#     return {"filename": file.filename}
#
#
# @app.get('/download_file')
# async def download_file():
#     return FileResponse(path='q.txt', filename='your_file.txt', media_type='multipart/form-data')
