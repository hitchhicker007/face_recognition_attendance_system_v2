from classes import Ui_loginWindow,Ui_registerWindow,Ui_MainWindow,AddStudent,Update_student, Remove_student,Upload_time_table, takeAttendance
from PyQt5 import QtWidgets,QtGui
import mysql.connector as mysql
import shutil,random,string

import os,cv2,csv,time
from datetime import datetime
import face_recognition
from pathlib import Path
from PIL import Image, ImageDraw

con = mysql.connect(host="localhost", user="php", password="", database="pyqt")
custor = con.cursor()

class Firstwindow(QtWidgets.QMainWindow, Ui_loginWindow):
    def __init__(self, parent=None):
        super(Firstwindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon48.png'))
        self.pushButton_2.clicked.connect(self.hide)
        self.pushButton.clicked.connect(self.login)

    def login(self):
        uname = self.lineEdit.text()
        passwd = self.lineEdit_2.text()

        if(uname=="" or passwd==""):
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("All Fields are required !")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setWindowIcon(QtGui.QIcon('icon48.png'))
            x = msg.exec_()
        else:
            con = mysql.connect(host="localhost", user="root", password="", database="pyqt")
            custor = con.cursor()
            custor.execute('select * from faculty_info where username = %s and password = %s', (uname, passwd))
            rows = custor.fetchall()
            if rows:
                self.hide()
                self.admin = AdminWindow()
                self.admin.show()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("User Not Found !!")
                msg.setWindowIcon(QtGui.QIcon('icon48.png'))
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                x = msg.exec_()



class UploadTimeTable(QtWidgets.QMainWindow,Upload_time_table):
    def __init__(self, parent=None):
        super(UploadTimeTable, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon48.png'))
        self.pushButton_3.clicked.connect(self.goback)
        self.pushButton.clicked.connect(self.select_file)
        self.pushButton_2.clicked.connect(self.save_file)
        self.pushButton_4.clicked.connect(self.reset)


    def reset(self):
        self.comboBox.setCurrentText("Select Semester")
        self.comboBox_2.setCurrentText("Select Branch")
        self.comboBox_3.setCurrentText("Select Class")
        self.label_2.setText("<html><head/><body><p><span style=\" color:#ff0000;\">File name</span></p></body></html>")
        self.progressBar.setProperty("value", 0)


    def goback(self):
        self.hide()
        self.admin = AdminWindow()
        self.admin.show()

    def select_file(self):
        if self.validity():
            sem, brnch, cls = self.get_data()
            temp = QtWidgets.QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*csv)')
            global filepath
            filepath = str(temp[0])
            filename = filepath.split('/')[-1]
            self.label_2.setText("<html><head/><body><p><span style=\" color:#ff0000;\">"+filename+"</span></p></body></html>")
        else:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("All Fields are required !")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setWindowIcon(QtGui.QIcon('icon48.png'))
            x = msg.exec_()


    def save_file(self):
        sem,brnch,cls = self.get_data()
        if self.validity():
            file_name = str(sem+'_'+brnch+'_'+cls+'.csv')
            shutil.copy(filepath,'time-tables/'+file_name)
            print("done")
            self.pbar = 0
            while self.pbar<100:
                self.pbar+=0.0001
                self.progressBar.setValue(self.pbar)

        else:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("All Fields are required !")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setWindowIcon(QtGui.QIcon('icon48.png'))
            x = msg.exec_()


    def validity(self):
        sem,brnch,cls = self.get_data()
        if (sem == "Select Semester" or brnch == "Select Branch" or cls == "Select Class"):
            return False
        else:
            return True


    def get_data(self):
        sem = self.comboBox.currentText()
        branch = self.comboBox_2.currentText()
        clsname = self.comboBox_3.currentText()
        return (sem,branch,clsname)


class take_Attendance(QtWidgets.QMainWindow,takeAttendance):
    def __init__(self, parent=None):
        super(take_Attendance, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon48.png'))
        self.pushButton_3.clicked.connect(self.goback)
        self.pushButton.clicked.connect(self.start_att)

    def goback(self):
        self.hide()
        self.admin = AdminWindow()
        self.admin.show()

    # def writecsv(pathh, array):  # function for writing csv file
    #     with open(pathh + '/session.csv', 'a', newline='') as csvFile:
    #         writer = csv.writer(csvFile)
    #         writer.writerow(["Enrollment", "Date", "Time"])
    #         for i in array:
    #             writer.writerow([i, datetime.today().strftime('%Y-%m-%d'),
    #                              time.strftime('%H-%M-%S')])
    #     csvFile.close()

    def start_att(self):
        sem = "4"
        field = "CE"
        class_name = "A"
        start_time = {}
        subjects = []

        with open('test.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                subjects.append(row[0])
                start_time.update({row[1]: row[2]})

        timestamp = time.strftime('%H:%M:%S')
        print(start_time)

        pic = 0
        bt = ""
        lec_flag = False
        while True:
            for st in start_time:
                while True:
                    if timestamp == st:
                        print("Image Capturing...")
                        # cap = cv2.VideoCapture("http://192.168.43.54:8080/video")
                        cap = cv2.VideoCapture(1)
                        current_time = time.strftime('%H.%M.%S')
                        current_date = datetime.today().strftime('%Y.%m.%d')
                        ts = current_time + '_' + current_date
                        attendance_path = str('attendance/' + ts)
                        while pic < 5:
                            if not os.path.exists(attendance_path):
                                os.makedirs(attendance_path)
                            ret, frame = cap.read()
                            # cv2.imshow('win', frame)
                            cv2.imwrite(attendance_path + '/' + 'pic_' + str(pic) + '.jpg', frame)
                            time.sleep(2)
                            k = cv2.waitKey(30) & 0xff
                            if k == 27:
                                cap.release()
                                print("Image Captured :)")
                                timestamp = time.strftime('%H:%M:%S')
                                break
                            timestamp = time.strftime('%H:%M:%S')
                            pic += 1
                        print("Image captured")
                        cap.release()
                        path = Path(
                            'images/sem-' + sem + '/' + field + '/class-' + class_name + '/')  # path of students details

                        images = []
                        names = []
                        enrolls = []

                        for imagepath in path.glob("*.jpg"):
                            img = face_recognition.load_image_file(str(imagepath))
                            img_encode = face_recognition.face_encodings(img)[0]
                            images.append(img_encode)
                            filename = str(imagepath).split("\\")[-1]
                            imname = filename.split('.')[-2]
                            name = imname.split('_')[-2]
                            names.append(name)
                            enrol = imname.split('_')[-3]
                            enrolls.append(enrol)

                        path2 = Path(attendance_path)

                        j = 0
                        test_imgs = []
                        pil_imgs = []
                        draws = []
                        face_locs = []
                        present_student = []

                        for classimg in path2.glob("*.jpg"):  # scanning images which is taken above

                            test_img = face_recognition.load_image_file(str(classimg))
                            face_loc = face_recognition.face_locations(test_img)
                            face_locs.append(face_loc)
                            face_encodes = face_recognition.face_encodings(test_img, face_loc)
                            test_imgs.append(face_encodes)

                            pil_img = Image.fromarray(test_img)
                            pil_imgs.append(pil_img)

                            draw = ImageDraw.Draw(pil_img)
                            draws.append(draw)

                        for test_img, pil_img, draw, face_loc in zip(test_imgs, pil_imgs, draws, face_locs):

                            resultpath = str('result/sem-' + sem + '/' + field + '/class-' + class_name + '/' + ts)
                            if not os.path.exists(resultpath):
                                os.makedirs(resultpath)

                            for (top, right, bottom, left), face_encode in zip(face_loc, test_img):
                                matches = face_recognition.compare_faces(images, face_encode, tolerance=0.5)

                                name = "Unknown Person"

                                if True in matches:
                                    first_match_index = matches.index(True)
                                    name = names[first_match_index]
                                    enrols = enrolls[first_match_index]

                                draw.rectangle(((left, top), (right, bottom)), outline=(0, 255, 0))

                                if enrols != "":
                                    present_student.append(enrols)

                                txt_w, txt_h = draw.textsize(name)
                                draw.rectangle(((left, bottom - txt_h - 3), (right, bottom)), fill=(0, 255, 0),
                                               outline=(0, 255, 0))
                                draw.text((left + 6, bottom - txt_h - 4), name, fill=(0, 0, 0))

                            pil_img.save(resultpath + '/' + str(j) + '.jpg')
                            j = j + 1

                        del draws

                        final_present_students = []  # list that contains present students
                        for stud in present_student:
                            if stud not in final_present_students:
                                final_present_students.append(stud)
                        #
                        # with open(resultpath + '/session.csv', 'a', newline='') as csvFile:
                        #     writer = csv.writer(csvFile)
                        #     writer.writerow(["Enrollment", "Date", "Time"])
                        #     for i in final_present_students:
                        #         writer.writerow([i, datetime.today().strftime('%Y-%m-%d'),time.strftime('%H-%M-%S')])
                        #         print("inserting")
                        #         custor.execute('insert into present_students values("",%s,%s,%s,"4","A","CE")',(str(i),str(time.strftime('%H-%M-%S')),str(datetime.today().strftime('%Y-%m-%d'))))
                        #         custor.execute('commit')
                        #         print("inserted")
                        # csvFile.close()

                        # self.writecsv(resultpath, final_present_students)  # calling writecsv() function

                         # list that contains present students


                        if lec_flag:
                            # print("end")
                            final_present_students_end = []
                            for stud in final_present_students:
                                if stud not in final_present_students_end:
                                    final_present_students_end.append(stud)


                            for lecstart in final_present_students_end:

                                for lecend in final_present_students_start:
                                    if lecstart==lecend:
                                        # database_entry.append(lecstart)
                                        print(lecstart)
                                        custor.execute('insert into present_students values("",%s,%s,%s,"4","A","CE")',(str(lecstart),str(datetime.today().strftime('%Y-%m-%d')),str(time.strftime('%H:%M:%S'))))
                                        custor.execute('commit')
                                    else:
                                        print("not match")


                            del final_present_students_end
                            del final_present_students_start

                        else:
                            # print("start")
                            final_present_students_start = []
                            for stud in present_student:
                                if stud not in final_present_students_start:
                                    final_present_students_start.append(stud)
                                    # print('lec. start')
                            # self.writecsv(resultpath, final_present_students_start,final_present_students_end)
                        if st == bt:
                            pic = 0
                            break
                        else:
                            try:
                                pic = 0
                                bt = start_time[st]
                                st = start_time[st]
                                lec_flag = True
                            except:
                                pic = 0
                                break
                    else:
                        pic = 0
                        timestamp = time.strftime('%H:%M:%S')

            break

        print("ok")



class Remove_stud(QtWidgets.QMainWindow,Remove_student):
    def __init__(self, parent=None):
        super(Remove_stud, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon48.png'))
        self.pushButton_4.clicked.connect(self.remove)
        self.pushButton_5.clicked.connect(self.goback)

    def goback(self):
        self.hide()
        self.admin = AdminWindow()
        self.admin.show()

    def remove(self):
        if(self.lineEdit_4.text()==""):
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("All Fields are required !")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setWindowIcon(QtGui.QIcon('icon48.png'))
            x = msg.exec_()
        else:
            if self.validity():
                status_type = self.comboBox.currentText()
                if status_type=="activate":
                    enr = self.lineEdit_4.text()
                    custor.execute('update students_info set status = "active" where enrol = '+enr+'')
                    custor.execute('commit')
                    self.lineEdit_4.setText("")
                else:
                    choice = QtWidgets.QMessageBox.question(self, 'window', "Sure, You Want to Remove this student?",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                    if choice==QtWidgets.QMessageBox.Yes:
                        # self.remove_img()
                        print("fska")
                        enr = self.lineEdit_4.text()
                        custor.execute('update students_info set status = "deactive" where enrol = '+enr+'')
                        custor.execute('commit')
                        self.lineEdit_4.setText("")
                    else:
                        pass
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Enrollment number not found !")
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setWindowIcon(QtGui.QIcon('icon48.png'))
                x = msg.exec_()
    #
    # def remove_img(self):
    #     custor.execute('select * from students_info where enrol = ' + self.lineEdit_4.text() + '')
    #     temp = custor.fetchall()
    #     path = str("images/sem-"+temp[0][5]+"/"+temp[0][6]+"/Class-"+temp[0][7]+"/"+temp[0][4]+"_"+temp[0][1]+"_"+temp[0][2]+".jpg")
    #     os.remove(path=path)

    def validity(self):
        custor.execute('select * from students_info')
        temp = custor.fetchall()
        for i in temp:
            if str(i[5]) == str(self.lineEdit_4.text()):
                return True
        return False


class Update_stud(QtWidgets.QMainWindow,Update_student):
    def __init__(self, parent=None):
        super(Update_stud, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon48.png'))
        self.pushButton_5.clicked.connect(self.goback)
        self.lineEdit_2.setDisabled(True)
        self.lineEdit_3.setDisabled(True)
        # self.lineEdit_4.setDisabled(True)
        self.lineEdit_5.setDisabled(True)
        self.lineEdit_6.setDisabled(True)
        self.lineEdit_7.setDisabled(True)
        self.lineEdit.setDisabled(True)
        self.lineEdit_8.setDisabled(True)
        self.lineEdit_9.setDisabled(True)
        self.comboBox.setDisabled(True)
        self.comboBox_2.setDisabled(True)
        self.comboBox_3.setDisabled(True)
        self.pushButton_4.setDisabled(True)
        self.pushButton_3.clicked.connect(self.fetch_data)
        self.pushButton_4.clicked.connect(self.update_detail)

    def goback(self):
        self.hide()
        self.admin = AdminWindow()
        self.admin.show()

    def fetch_data(self):
        if(self.lineEdit_4.text()==""):
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("All Fields are required !")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setWindowIcon(QtGui.QIcon('icon48.png'))
            x = msg.exec_()
        else:
            if self.validity():
                custor.execute('select * from students_info where enrol = '+self.lineEdit_4.text()+'')
                rows = custor.fetchall()
                self.lineEdit.setText(str(rows[0][1]))
                self.lineEdit_2.setText(str(rows[0][2]))
                self.lineEdit_3.setText(str(rows[0][3]))
                self.lineEdit_5.setText(str(rows[0][4]))
                self.comboBox.setCurrentText(rows[0][5])
                self.comboBox_2.setCurrentText(rows[0][6])
                self.comboBox_3.setCurrentText(rows[0][7])
                self.lineEdit_6.setDisabled(False)
                self.lineEdit_7.setDisabled(False)
                self.lineEdit_8.setDisabled(False)
                self.lineEdit_9.setDisabled(False)
                self.pushButton_4.setDisabled(False)
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Enrollment number not found !")
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setWindowIcon(QtGui.QIcon('icon48.png'))
                x = msg.exec_()

    def validity(self):
        custor.execute('select * from students_info')
        temp = custor.fetchall()
        for i in temp:
            if str(i[4]) == str(self.lineEdit_4.text()):
                return True
        return False

    def update_detail(self):
        if(self.lineEdit_6.text()=="" or self.lineEdit_7.text()=="" or self.lineEdit_8.text()=="" or self.lineEdit_9.text()==""):
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("All Fields are required !")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setWindowIcon(QtGui.QIcon('icon48.png'))
            x = msg.exec_()
        else:
            custor.execute('update students_info set fname=%s, lname=%s,email=%s,enrol=%s where enrol=%s',(self.lineEdit_8.text(), self.lineEdit_7.text(), self.lineEdit_9.text(), self.lineEdit_6.text(),self.lineEdit_4.text()))
            custor.execute("commit")
            self.rename_img()
            self.lineEdit.setText("")
            self.lineEdit_2.setText("")
            self.lineEdit_3.setText("")
            self.lineEdit_4.setText("")
            self.lineEdit_5.setText("")
            self.lineEdit_6.setText("")
            self.lineEdit_7.setText("")
            self.lineEdit_8.setText("")
            self.lineEdit_9.setText("")
            self.comboBox.setCurrentText("Semester")
            self.comboBox_2.setCurrentText("Branch")
            self.comboBox_3.setCurrentText("Class")
            self.pushButton_4.setDisabled(True)

    def rename_img(self):
        src_old = str("images/sem-" + self.comboBox.currentText() + "/" + self.comboBox_2.currentText() + "/class-" + self.comboBox_3.currentText() + "/" + self.lineEdit_4.text() + "_" + self.lineEdit.text() + "_" + self.lineEdit_2.text() + ".jpg")
        src_new = str("images/sem-" +self.comboBox.currentText()+ "/" + self.comboBox_2.currentText() + "/class-" + self.comboBox_3.currentText() + "/" + self.lineEdit_6.text()+ "_" + self.lineEdit_8.text() + "_" + self.lineEdit_7.text() + ".jpg")

        os.rename(src_old, src_new)

class AdminWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(AdminWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon48.png'))
        self.pushButton_7.clicked.connect(self.logout)
        self.pushButton.clicked.connect(self.addstudent)
        self.pushButton_2.clicked.connect(self.updatestud)
        self.pushButton_3.clicked.connect(self.remove_stud)
        self.pushButton_4.clicked.connect(self.upload_tt)
        self.pushButton_6.clicked.connect(self.startAttendance)

    def remove_stud(self):
        self.hide()
        self.temp = Remove_stud()
        self.temp.show()

    def logout(self):
        choice = QtWidgets.QMessageBox.question(self, 'window', "Sure, You Want to LogOut?",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice==QtWidgets.QMessageBox.Yes:
            self.hide()
            self.login = Firstwindow()
            self.login.show()
        else:
            pass

    def addstudent(self):
        self.hide()
        self.addstudent = AddStud()
        self.addstudent.show()

    def updatestud(self):
        self.hide()
        self.updatestudent = Update_stud()
        self.updatestudent.show()

    # def save_file(self):
    #     path = QtWidgets.QFileDialog.getOpenFileName(self,'Open CSV', os.getenv('HOME'),'CSV(*csv)')
    #     newPath = shutil.copy(path[0], 'sample.csv')
    #     print("foe")

    def upload_tt(self):
        self.hide()
        self.tt = UploadTimeTable()
        self.tt.show()

    def startAttendance(self):
        self.hide()
        self.take = take_Attendance()
        self.take.show()


class AddStud(QtWidgets.QMainWindow,AddStudent):
    def __init__(self, parent=None):
        super(AddStud, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon48.png'))
        self.pushButton_3.clicked.connect(self.goback)
        self.pushButton.clicked.connect(self.take_pic)
        self.pushButton_2.hide()
        self.pushButton_2.clicked.connect(self.submit)
        self.lineEdit_5.setDisabled(True)

    def goback(self):
        self.hide()
        self.admin = AdminWindow()
        self.admin.show()

    def take_pic(self):
        fname,lname,email,enrol,sem,branch,classs = self.fetch_data()

        if(fname=="" or lname=="" or email=="" or enrol=="" or sem=="Select Semester" or branch=="Select Branch" or classs=="Select Class"):
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("All Fields are required !")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setWindowIcon(QtGui.QIcon('icon48.png'))
            x = msg.exec_()
        else:
            if self.validation():
                path = str('./images/sem-' + str(sem) + '/' + branch + '/class-' + classs)
                if not os.path.exists(path):
                    os.makedirs(path)
                cap = cv2.VideoCapture(1)
                while True:
                    ret, frame = cap.read()
                    cv2.imshow('window', frame)
                    k = cv2.waitKey(30) & 0xff
                    if k == 27:
                        cv2.imwrite(path + '/' + str(enrol) + '_' + fname + '_' + lname + '.jpg',
                                    frame)  # press 'ESC' to quit
                        break
                cap.release()
                cv2.destroyAllWindows()
                self.pushButton_2.show()
                self.lineEdit_5.setText(''.join(random.choice(string.ascii_lowercase) for i in range(10)))
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Enrollment already exists!")
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setWindowIcon(QtGui.QIcon('icon48.png'))
                x = msg.exec_()

    def submit(self):
        fname, lname, email, enrol, sem, branch, classs = self.fetch_data()
        passwd = self.lineEdit_5.text()

        custor.execute('insert into students_info values("",%s,%s,%s,%s,%s,%s,%s,%s,"active")', (fname,lname,email,passwd,enrol,sem,branch,classs))
        custor.execute("commit")

        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
        self.lineEdit_5.setText("")
        self.comboBox.setCurrentText("Select Semester")
        self.comboBox_2.setCurrentText("Select Branch")
        self.comboBox_3.setCurrentText("Select Class")

    def fetch_data(self):
        fname = self.lineEdit.text()
        lname = self.lineEdit_2.text()
        email = self.lineEdit_3.text()
        enrol = self.lineEdit_4.text()
        sem = str(self.comboBox.currentText())
        branch = str(self.comboBox_2.currentText())
        classs = str(self.comboBox_3.currentText())
        return (fname,lname,email,enrol,sem,branch,classs)

    def validation(self):
        enrol = self.lineEdit_4.text()
        custor.execute('select * from students_info')
        temp = custor.fetchall()

        for i in temp:
            if str(i[5]) == str(enrol):
                return False
        return True


class Secondwindow(QtWidgets.QMainWindow, Ui_registerWindow):
    def __init__(self, parent=None):
        super(Secondwindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon48.png'))
        self.pushButton_2.clicked.connect(self.hide)
        self.pushButton.clicked.connect(self.signup)

    def signup(self):
        fname = self.lineEdit.text()
        lname = self.lineEdit_2.text()
        uname = self.lineEdit_3.text()
        passwd = self.lineEdit_4.text()

        if(fname=="" or lname=="" or uname=="" or passwd==""):
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("All Fields are required !")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setWindowIcon(QtGui.QIcon('icon48.png'))
            x = msg.exec_()
        else:
            custor.execute('insert into faculty_info values("",%s,%s,%s,%s)', (fname, lname, uname, passwd))
            custor.execute("commit")

            choice = QtWidgets.QMessageBox.question(self,'Successfull!',"Faculty Added, Want to go Back?",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

            if choice==QtWidgets.QMessageBox.Yes:
                self.hide()
                self.first = Firstwindow()
                self.first.show()
            else:
                self.lineEdit.setText("")
                self.lineEdit_2.setText("")
                self.lineEdit_3.setText("")
                self.lineEdit_4.setText("")


class Manager:
    def __init__(self):
        self.first = Firstwindow()
        self.second = Secondwindow()

        self.first.pushButton_2.clicked.connect(self.second.show)
        self.second.pushButton_2.clicked.connect(self.first.show)
        self.first.show()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    manager = Manager()
    sys.exit(app.exec_())