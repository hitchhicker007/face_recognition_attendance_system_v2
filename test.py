import os,cv2,csv,time
from datetime import datetime
import face_recognition
from pathlib import Path
from PIL import Image, ImageDraw, ImageTk
import subprocess

#
# def writecsv(path,array_s,array_e): #function for writing csv file
#     array_known = []
#     array_unknown = []
#     l = 0
#     while l<len(array_s):
#         if(array_s[l]==array_e[l]):
#             if (array_s[l]==array_e[l])!="Unknown Person":
#                 array_known.append(array_s[l])
#             else:
#                 array_unknown.append(array_s[l])
#         l+=1
#
#     with open(path+'/session_known.csv','a',newline='') as csvFile:
#         writer = csv.writer(csvFile)
#         writer.writerow(["Enrollment","Full Name","Date","Time"])
#         for i in array_known:
#             writer.writerow([i])
#     csvFile.close()
#
#     with open(path + '/session_unknown.csv', 'a', newline='') as csvFile:
#         writer = csv.writer(csvFile)
#         writer.writerow(["Enrollment", "Full Name", "Date", "Time"])
#         for i in array_unknown:
#             writer.writerow([i])
#     csvFile.close()
#
# class start_class():
#     def start(self):
#         sem = "4"
#         field = "CE"
#         class_name = "A"
#         start_time = {}
#         subjects = []
#
#         with open('test.csv','r') as file:
#             reader = csv.reader(file)
#             for row in reader:
#                 subjects.append(row[0])
#                 start_time.update({row[1]:row[2]})
#
#         timestamp = time.strftime('%H:%M:%S')
#         print(start_time)
#
#         pic=0
#         bt=""
#         lec_flag = False
#         while True:
#             for st in start_time:
#                 while True:
#                     if timestamp==st:
#                         cap = cv2.VideoCapture(0)
#                         current_time = time.strftime('%H.%M.%S')
#                         current_date = datetime.today().strftime('%Y.%m.%d')
#                         ts = current_time + '_' + current_date
#                         attendance_path = str('attendance/' + ts)
#                         while pic<5:
#                             if not os.path.exists(attendance_path):
#                                 os.makedirs(attendance_path)
#                             ret, frame = cap.read()
#                             # cv2.imshow('win', frame)
#                             cv2.imwrite(attendance_path+'/'+'pic_'+str(pic)+'.jpg',frame)
#                             time.sleep(2)
#                             k = cv2.waitKey(30) & 0xff
#                             if k == 27:
#                                 cap.release()
#                                 timestamp = time.strftime('%H:%M:%S')
#                                 break
#                             timestamp = time.strftime('%H:%M:%S')
#                             pic+=1
#                         cap.release()
#                         path = Path(
#                             'images/sem-' + sem + '/' + field + '/class-' + class_name + '/')  # path of students details
#
#                         images = []
#                         names = []
#                         enrolls = []
#
#                         for imagepath in path.glob("*.jpg"):
#                             img = face_recognition.load_image_file(str(imagepath))
#                             img_encode = face_recognition.face_encodings(img)[0]
#                             images.append(img_encode)
#                             filename = str(imagepath).split("\\")[-1]
#                             imname = filename.split('.')[-2]
#                             name = imname.split('_')[-2]
#                             names.append(name)
#                             enrol = imname.split('_')[-3]
#                             enrolls.append(enrol)
#
#                         path2 = Path(attendance_path)
#
#                         j = 0
#                         test_imgs = []
#                         pil_imgs = []
#                         draws = []
#                         face_locs = []
#                         present_student = []
#
#                         for classimg in path2.glob("*.jpg"):  # scanning images which is taken above
#
#                             test_img = face_recognition.load_image_file(str(classimg))
#                             face_loc = face_recognition.face_locations(test_img)
#                             face_locs.append(face_loc)
#                             face_encodes = face_recognition.face_encodings(test_img, face_loc)
#                             test_imgs.append(face_encodes)
#
#                             pil_img = Image.fromarray(test_img)
#                             pil_imgs.append(pil_img)
#
#                             draw = ImageDraw.Draw(pil_img)
#                             draws.append(draw)
#
#                         for test_img, pil_img, draw, face_loc in zip(test_imgs, pil_imgs, draws, face_locs):
#
#                             resultpath = str('result/sem-' + sem + '/' + field + '/class-' + class_name + '/' + ts)
#                             if not os.path.exists(resultpath):
#                                 os.makedirs(resultpath)
#
#                             for (top, right, bottom, left), face_encode in zip(face_loc, test_img):
#                                 matches = face_recognition.compare_faces(images, face_encode, tolerance=0.5)
#
#                                 name = "Unknown Person"
#
#                                 if True in matches:
#                                     first_match_index = matches.index(True)
#                                     name = names[first_match_index]
#                                     enrols = enrolls[first_match_index]
#
#                                 draw.rectangle(((left, top), (right, bottom)), outline=(0, 255, 0))
#
#                                 if enrols != "":
#                                     present_student.append(enrols)
#
#                                 txt_w, txt_h = draw.textsize(name)
#                                 draw.rectangle(((left, bottom - txt_h - 3), (right, bottom)), fill=(0, 255, 0),
#                                                outline=(0, 255, 0))
#                                 draw.text((left + 6, bottom - txt_h - 4), name, fill=(0, 0, 0))
#
#                             pil_img.save(resultpath + '/' + str(j) + '.jpg')
#                             j = j + 1
#
#                         del draws
#
#                         final_present_students_start = []  # list that contains present students
#                         final_present_students_end = []
#                         if lec_flag:
#                             for stud in present_student:
#                                 if stud not in final_present_students_end:
#                                     final_present_students_end.append(stud)
#                             writecsv(resultpath, final_present_students_start,final_present_students_end)
#                             del final_present_students_end
#                             del final_present_students_start
#                         else:
#                             for stud in present_student:
#                                 if stud not in final_present_students_start:
#                                     final_present_students_start.append(stud)
#                             # writecsv(resultpath, final_present_students_start,final_present_students_end)
#                         if st == bt:
#                             pic = 0
#                             break
#                         else:
#                             try:
#                                 pic = 0
#                                 bt = start_time[st]
#                                 st = start_time[st]
#                                 lec_flag = True
#                             except:
#                                 pic = 0
#                                 break
#                     else:
#                         pic = 0
#                         timestamp = time.strftime('%H:%M:%S')
#             break
#
#         print("ok")
cap = cv2.VideoCapture(1)
while True:
    ret,frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    cv2.imshow('win',frame)
