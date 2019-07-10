### Before you get started

To run these scripts, you need the following installed:

1. Python 3 and <= 3.6
2. OpenCV Python extensions
 - I highly recommend these OpenCV installation guides: 
   https://www.pyimagesearch.com/opencv-tutorials-resources-guides/ 
3. The python libraries listed in requirements.txt
 - Try running "pip3 install -r requirements.txt"

### Step 1: Fetch some CAPTCHA images from Baacloud
Run:

python3 fetchCaptchas.py

The image results will be stored in the "images/baacloud_source_captcha_images"

### Step 2: Manually mark the image correct text
Run:

python3 baacloud_html_mark.py

The marked image results will be stored in the "images/baacloud_marked_captcha_images"

### Step 3: Extract single letters from CAPTCHA images

Run:

python3 baacloud_extract_single_letters.py

The results will be stored in the "images/baacloud_extracted_letter_images" folder.


### Step 4: Train the neural network to recognize single letters

Run:

python3 baacloud_train_model.py

This will write out "models/baacloud_captcha_model.hdf5" and "models/baacloud_model_labels.dat"


### Step 5: Use the model to check success percent of marked CAPTCHAs!

Run: 

python3 baacloud_captchas_percent.py