# BDA-HTML-Generator
Scripts for generating group homepage



## Support
We support generating the following items with scripts:

+ Student
+ Alumni
+ News
+ Publications

## Guide
### Students information 
You will need to modify both `all-en.json` and `all-zh.json` for information on both English and Chinese.

Then you can run `python student.py` to update both
+ index.html
+ index-zh.html
+ alumni.html
+ alumni-zh.html

**Attention**:
When someone is graduating and transferring to Ph.D., 
don't forget to change the `status` item in his/her item in json file :) 

### Publications
The same as students information, 
you need to modify the `paper.json` 
then run `python publication.py`.

### News
The same as students information, 
you need to modify the `news.json` 
then run `python news.py`.