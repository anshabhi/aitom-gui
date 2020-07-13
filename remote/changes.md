Hello, I have made many changes and added new features to the code, a rough summary is:

1. added `resumable.js` support for uploads. This will enable us to efficiently take large MRC files as input, as we discussed earlier. It divides large files into smaller pieces and adds more redundancy to upload procedure. But, in the process, your `serve.py` has become messy once again. Please feel free to clean it! I adapted the code from https://github.com/leriomaggio/django2-resumable/, but I have modified `django2_resumable/file_upload.html` in some ways for our purposes, such as using `api-model` as the URL, and saving the links obtained to javascript.

For the implementation of `resumable.js`, I have started using `ModalForms` instead of `FileSystemStorage` for upload. I spent quite a lot of time in learning how to use ModalForms.

2. Similarly, for uploads from server (i.e. downloading .vtk file) I have added a mechanism to serve a file chunk-by-chunk. This way, the file is not required to be loaded entirely into memory at once, and its more efficient. I added a new view in views.py for this. Now `display.html` calls `/download/` route for downloading.

3. I have divided the uploads folder into `mrc` and `vtk` folders. New mrc files are uploaded to `/uploads/mrc` folder, processed vtk files are stored in `/uploads/vtk`

4. The new GUI allows user to choose whether to upload a new file or use an existing one. For this, `/uploads/mrc/` folder acts as the library. 

5. After choosing a file, the user can enter coordinates in the JSON format that we decided earlier. I decided to send this to `api-model-json`, as `api-model` accepts file upload input, and it will get confusing to use a single API for both the formats. Please let me know if this is okay.

6. Reworked `index.html`, for new GUI, and divided it further into `ModalForms`. I have used `MDL Stepper` library for building the UI. Currently, the CSS has quite a few display issues due to conflict with the existing `main.css`. I will fix this tomorrow maybe

The code might get slightly confusing as I haven't put any comments anywhere .... I will add comments and credits or attributions later.

requirements.txt has also been updated with `django2_resumable`
