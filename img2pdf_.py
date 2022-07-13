import os 
import img2pdf
from PIL import Image
import argparse
import shutil 
from datetime import date

today = str(date.today()).replace('-','')

parser = argparse.ArgumentParser(description=f"Image2Pdf\nTransform all the ImageShots into PDF, and mv these shots to /Users/Jaye/Desktop/xxxtest/")
parser.add_argument("--dir_path",type=str,default="/Users/Jaye/Desktop/",help="ImageShots Where saved")
parser.add_argument("--pdf_path",type=str,default=f"/Users/Jaye/Desktop/Postgraduate Files/People's Lectures/LabMiccai_PaperSharingLecture/{today}_Lecture.pdf",help="PDF Where you want to save")
args=parser.parse_args()

dir_path = args.dir_path # image files
pdf_path = args.pdf_path # pdf you want to save

img_lst = os.listdir(dir_path)
if '.DS_Store' in img_lst: 
    img_lst.remove('.DS_Store')

'''
*: ---------------------------------------------#
#: move all shots to a new file 
$: ---------------------------------------------#
'''
target_path = f"/Users/Jaye/Desktop/{date.today()}_ScreenShots_Collection/"
if os.path.exists(target_path):
    shutil.rmtree(target_path)
if not os.path.exists(target_path):
    os.mkdir(target_path)

for fname in img_lst:
    if fname.endswith(".png") and str(date.today()) in fname: # move all screenshots from today to path
        img_path = os.path.join(dir_path,fname)
        shutil.move(img_path,target_path)

img_lst = os.listdir(target_path)
if '.DS_Store' in img_lst:
    img_lst.remove('.DS_Store')

'''
*: ---------------------------------------------#
#:  transform Imageshots with PNG to Jpg / make img2pdf happy
$: ---------------------------------------------#
'''

reorder = []
reorder_base = []
for fname in img_lst:
    if fname.endswith(".png"):
        file = fname.split(' ')[-1].split('.')[0:3] # 屏幕快照 2022-7-12 14.18.07.png -> [14, 18, 07]
        file_base = fname.split('.')[0]
        reorder.append(file)
        reorder_base.append(file_base)

index = 0

for i in range(0,len(reorder_base)):
    index = i
    min = reorder[index]     
  
    for j in range(i+1,(len(reorder_base))):

        if min[0] < reorder[j][0]:
            min = reorder[index]
            
        elif min[0] == reorder[j][0]:
            if min[1] < reorder[j][1]:
                min  = reorder[index] 

            elif min[1] == reorder[j][1]:
                if min[2] < reorder[j][2]:
                    min = reorder[index]
                else:
                    index = j
                    min = reorder[j]
            
            else:
                index = j
                min = reorder[j]
                
        elif min[0] > reorder[j][0]:
            index = j
            min = reorder[j]
    
    reorder[i], reorder[index] = reorder[index], reorder[i]
    img_lst[i], img_lst[index] = img_lst[index], img_lst[i] 
    
    path_base = os.path.join(target_path,img_lst[i])

    im = Image.open(path_base)
    im = im.convert('RGB')
    im.save("{}/{}.jpg".format(target_path,i),quality=95)
    os.remove(path_base)

'''
*: ---------------------------------------------#
#:  images to pdf 
$: ---------------------------------------------#
'''
img_lst = os.listdir(target_path)
if '.DS_Store' in img_lst:
    img_lst.remove('.DS_Store')
img_lst.sort(key=lambda x:int(x[:-4]))
img_path_list = []
for item in img_lst:
    if item.endswith(".jpg"):
        item = os.path.join(target_path,item)
        img_path_list.append(item)
    

if os.path.exists(pdf_path):
    os.remove(pdf_path)
with open(pdf_path,"wb") as f:
    content = img2pdf.convert(img_path_list)
    f.write(content)
