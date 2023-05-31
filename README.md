# COMP3000HK Computing Project - Image Spam Detection Using Machine Learning

## To download images file for CNN model
The image dataset contains many files and the size is around 2GB, GitHub is not allowed to commmit.
Please download below file and unzip it to "`machine_learning/dataset/images`" directory

[Images Dataset](https://liveplymouthac-my.sharepoint.com/:u:/g/personal/ho_t_lo_students_plymouth_ac_uk/EV5c66JVexpGkSnP8jbYPPQBs5l3DWB7JMsc2gToVJpNUQ?e=VpodKX)

## Serve trained model to Flask API
The trainer model filesize are too large, please download below files and put into "`backend/`" directory

[Image classifier model](https://liveplymouthac-my.sharepoint.com/:u:/g/personal/ho_t_lo_students_plymouth_ac_uk/ERKb3uKSMrRFtOZ7rAb3C4ABSC0WQtnKlGJ24NqFbm3ulA?e=nO5tvz)

[Text classifier model](https://liveplymouthac-my.sharepoint.com/:u:/g/personal/ho_t_lo_students_plymouth_ac_uk/EUMSdP8QOIJIgiNXamcAYcQBs5671__3tHWXA-arO9I1_Q?e=OErf3A)

## Convert Spam/Ham dataset to Image
```
cd selenium
pip -r requirement.txt
python3 generate_screenshots_from_csv.py
```