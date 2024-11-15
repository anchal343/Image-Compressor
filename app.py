import sys
from PyQt5.QtWidgets import QApplication,QFileDialog, QWidget,QInputDialog, QMainWindow, QFrame, QLabel, QLineEdit, QPushButton, QComboBox
from PyQt5.QtGui import QIcon
from PIL import Image
from PyQt5.QtCore import Qt
import os
import PIL

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Image Compressor'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 600
        self.statusBar().showMessage("Message:")
        self.statusBar().setObjectName("status")
        self.image_width = 0
        self.setFixedSize(self.width, self.height)
        self.setObjectName("main_window")
        stylesheet = ""
        with open("design.qss", "r") as f:
            stylesheet = f.read()
        self.setStyleSheet(stylesheet)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        
        #-----------main window----------------------
        
        self.single_bubble = QFrame(self)
        self.single_bubble.setObjectName("bubble")
        self.single_bubble.move(50, 100)
        self.single_bubble.mousePressEvent = self.single_bubble_clicked

        self.single_bubble_heading = QLabel(self.single_bubble)
        self.single_bubble_heading.setObjectName("bubble_heading")
        self.single_bubble_heading.setText("Compress Image")
        self.single_bubble_heading.move(90, 8)

        self.single_bubble_para = QLabel(self.single_bubble)
        self.single_bubble_para.setObjectName("bubble_para")
        self.single_bubble_para.setText("Click here to compress single image!")
        self.single_bubble_para.move(25,32)
        
        self.dir_bubble = QFrame(self)
        self.dir_bubble.setObjectName("bubble")
        self.dir_bubble.move(50, 275)
        self.dir_bubble.mousePressEvent = self.dir_bubble_clicked 

        self.dir_bubble_heading = QLabel(self.dir_bubble)
        self.dir_bubble_heading.setObjectName("bubble_heading")
        self.dir_bubble_heading.setText("Compress Multiple Images")
        self.dir_bubble_heading.move(55, 8)

        self.dir_bubble_para = QLabel(self.dir_bubble)
        self.dir_bubble_para.setObjectName("bubble_para")
        self.dir_bubble_para.setText("Want to compress multiple images at once!")
        self.dir_bubble_para.move(10,32) 


        #---------single bubble expanded------------------
        
        self.single_bubble_expanded = QFrame(self)
        self.single_bubble_expanded.setObjectName("bubble_expanded")
        self.single_bubble_expanded.move(50, 100)
        self.single_bubble_expanded.setVisible(False)

        self.back_arrow_s = QLabel(self.single_bubble_expanded)
        self.back_arrow_s.move(15, 0)
        self.back_arrow_s.setObjectName("back_arrow")
        self.back_arrow_s.setTextFormat(Qt.RichText)
        self.back_arrow_s.setText("&#8592;")
        self.back_arrow_s.mousePressEvent = self.back_arrow_clicked 

        self.single_bubble_heading = QLabel(self.single_bubble_expanded)
        self.single_bubble_heading.setObjectName("bubble_heading")
        self.single_bubble_heading.setText("Compress Image")
        self.single_bubble_heading.move(90, 8)

        self.select_image_label = QLabel(self.single_bubble_expanded)
        self.select_image_label.setObjectName("bubble_para")
        self.select_image_label.setText("Choose Image")
        self.select_image_label.move(30, 50)

        self.image_path = QLineEdit(self.single_bubble_expanded)
        self.image_path.setObjectName("path_text")
        self.image_path.move(60, 85)

        self.browse_button = QPushButton(self.single_bubble_expanded)
        self.browse_button.setText("...")
        self.browse_button.setObjectName("browse_button")
        self.browse_button.clicked.connect(self.select_file)
        self.browse_button.move(240, 85)

        self.select_image_quality = QLabel(self.single_bubble_expanded)
        self.select_image_quality.setObjectName("bubble_para")
        self.select_image_quality.setText("Choose Quality")
        self.select_image_quality.move(30, 130)

        self.quality_path = QLineEdit(self.single_bubble_expanded)
        self.quality_path.setObjectName("quality_path_text")
        self.quality_path.move(60, 160)

        self.quality_combo = QComboBox(self.single_bubble_expanded)
        self.quality_combo.addItem("High")
        self.quality_combo.addItem("Medium")
        self.quality_combo.addItem("Low")
        self.quality_combo.move(170, 160)
        self.quality_combo.currentIndexChanged.connect(self.quality_current_value)
        self.quality_combo.setObjectName("quality_combo")
        self.quality_combo.resize(90, 26)

        self.compress_image = QPushButton(self.single_bubble_expanded)
        self.compress_image.setText("Compress")
        self.compress_image.setObjectName("compress_button")
        self.compress_image.clicked.connect(self.resize_pic)
        self.compress_image.move(100, 260)

        #---------end single bubble expanded------------------


        #---------dir bubble expanded------------------
        
        self.dir_bubble_expanded = QFrame(self)
        self.dir_bubble_expanded.setObjectName("bubble_expanded")
        self.dir_bubble_expanded.move(50, 100)
        self.dir_bubble_expanded.setVisible(False)

        self.back_arrow_d = QLabel(self.dir_bubble_expanded)
        self.back_arrow_d.move(15, 0)
        self.back_arrow_d.setObjectName("back_arrow")
        self.back_arrow_d.setTextFormat(Qt.RichText)
        self.back_arrow_d.setText("&#8592;")
        self.back_arrow_d.mousePressEvent = self.back_arrow_clicked 

        self.dir_bubble_heading = QLabel(self.dir_bubble_expanded)
        self.dir_bubble_heading.setObjectName("bubble_heading")
        self.dir_bubble_heading.setText("Compress Mulitple Image")
        self.dir_bubble_heading.move(70, 8)

        self.select_source_label = QLabel(self.dir_bubble_expanded)
        self.select_source_label.setObjectName("bubble_para")
        self.select_source_label.setText("Choose Source Directory")
        self.select_source_label.move(30, 50)

        self.source_path = QLineEdit(self.dir_bubble_expanded)
        self.source_path.setObjectName("path_text")
        self.source_path.move(60, 85)

        self.browse_source_button = QPushButton(self.dir_bubble_expanded)
        self.browse_source_button.setText("...")
        self.browse_source_button.setObjectName("browse_button")
        self.browse_source_button.clicked.connect(self.select_folder_source)
        self.browse_source_button.move(240, 85)

        self.select_dest_label = QLabel(self.dir_bubble_expanded)
        self.select_dest_label.setObjectName("bubble_para")
        self.select_dest_label.setText("Choose Destination Directory")
        self.select_dest_label.move(30, 130)

        self.dest_path = QLineEdit(self.dir_bubble_expanded)
        self.dest_path.setObjectName("path_text")
        self.dest_path.move(60, 160)

        self.browse_dest_button = QPushButton(self.dir_bubble_expanded)
        self.browse_dest_button.setText("...")
        self.browse_dest_button.setObjectName("browse_button")
        self.browse_dest_button.clicked.connect(self.select_folder_dest)
        self.browse_dest_button.move(240, 160)

        self.select_dir_quality = QLabel(self.dir_bubble_expanded)
        self.select_dir_quality.setObjectName("bubble_para")
        self.select_dir_quality.setText("Choose Quality")
        self.select_dir_quality.move(30, 205)

        self.quality_dir_path = QLineEdit(self.dir_bubble_expanded)
        self.quality_dir_path.setObjectName("quality_path_text")
        self.quality_dir_path.move(60, 235)

        self.quality_dir_combo = QComboBox(self.dir_bubble_expanded)
        self.quality_dir_combo.addItem("High")
        self.quality_dir_combo.addItem("Medium")
        self.quality_dir_combo.addItem("Low")
        self.quality_dir_combo.move(170, 235)
        self.quality_dir_combo.currentIndexChanged.connect(self.quality_values)
        self.quality_dir_combo.setObjectName("quality_combo")
        self.quality_dir_combo.resize(96, 26)
        
        self.compress_dir = QPushButton(self.dir_bubble_expanded)
        self.compress_dir.setText("Compress")
        self.compress_dir.setObjectName("compress_button")
        self.compress_dir.clicked.connect(self.resize_folder)
        self.compress_dir.move(100, 290)
        
        #---------end dir bubble expanded------------------


        #----------end of main window-----------------
       
        self.show()
    
    #------------function-----------------------
    
    def select_file(self):
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);; JPEG (*.jpeg)")
        if fileName:
            print(fileName, _)
            self.image_path.setText(fileName)
            img = Image.open(fileName)
            self.image_width = img.width
            self.quality_path.setText(str(self.image_width))
    
    def select_folder_source(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        print(folder)
        self.source_path.setText(folder)
        files = os.listdir(folder)
        first_pic = folder + "/" + files[0]
        img = Image.open(first_pic)
        self.image_width = img.width
        self.quality_dir_path.setText(str(self.image_width))

    def select_folder_dest(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        print(folder)
        self.dest_path.setText(folder)          

    def quality_current_value(self):
        if self.quality_combo.currentText() == "High":
            self.quality_path.setText(str(self.image_width))
            
        if self.quality_combo.currentText() == "Medium":
            self.quality_path.setText(str(int(self.image_width/2)))

        if self.quality_combo.currentText() == "Low":
            self.quality_path.setText(str(int(self.image_width/4)))
            
    def quality_values(self):
        if self.quality_dir_combo.currentText() == "High":
            self.quality_dir_path.setText(str(self.image_width))
            
        if self.quality_dir_combo.currentText() == "Medium":
            self.quality_dir_path.setText(str(int(self.image_width/2)))
            
        if self.quality_dir_combo.currentText() == "Low":
            self.quality_dir_path.setText(str(int(self.image_width/4)))  

    def back_arrow_clicked(self, event):
        self.single_bubble.setVisible(True)
        self.dir_bubble.setVisible(True)
        self.single_bubble_expanded.setVisible(False)
        self.dir_bubble_expanded.setVisible(False)

    def single_bubble_clicked(self, event):
        print("single bubble clicked")
        self.single_bubble.setVisible(False)
        self.dir_bubble.setVisible(False)
        self.single_bubble_expanded.setVisible(True)
        self.dir_bubble_expanded.setVisible(False)

    def dir_bubble_clicked(self, event):
        print("dir bubble clicked")
        self.single_bubble.setVisible(False)
        self.dir_bubble.setVisible(False)
        self.dir_bubble_expanded.setVisible(True)
        self.single_bubble_expanded.setVisible(False)   
    
    def compression_code(self, old_pic, new_pic, quality):
        img = Image.open(old_pic)
        img.save(new_pic, quality=quality)
    
    def resize_pic(self):
        old_pic = self.image_path.text().strip()
        valid_extensions = ['.jpg', '.jpeg', '.png']
    
        if not any(old_pic.lower().endswith(ext) for ext in valid_extensions):
            self.statusBar().showMessage("Message: Please choose a valid image (.jpg, .jpeg, .png)")
            return

        if old_pic == "":
           self.statusBar().showMessage("Message: Please choose an image ")
           return

        print(old_pic)
        quality = int(self.quality_path.text())
        print(quality)

        # Get new image name from user
        new_pic_name, okPressed = QInputDialog.getText(self, "Save Image as", "Image Name:", QLineEdit.Normal, "")
    
        if okPressed and new_pic_name != '':
          # Determine the extension based on the old image
            extension = old_pic[old_pic.rfind('.'):].lower()  # Get the extension from the old pic
            if extension not in valid_extensions:
              extension = ".jpeg"  # Default to .jpeg if none matched
        
            new_pic_name += extension  # Append the extension to the new name
        
            # Create new file path
            new_pic = "/".join(old_pic.split("/")[:-1]) + "/" + new_pic_name
            print(new_pic)

        # Call your compression function
            self.compression_code(old_pic, new_pic, quality)
            self.statusBar().showMessage("Message: Compressed")
        
        else:
           self.statusBar().showMessage("Message: Operation cancelled")

    
    def resize_folder(self):
        source_directory = self.source_path.text()
        dest_directory = self.dest_path.text()

        if not source_directory or not dest_directory:
            self.statusBar().showMessage("Message: Please select source and destination directory")
            return

        try:
            files = os.listdir(source_directory)
        except FileNotFoundError:
            self.statusBar().showMessage("Message: Source directory not found")
            return
        
        i = 0
        for file in files:
            i+=1
            print(file)
            if file [-4:] == '.jpg' or file [-4:] == '.png' or file [-5:] == '.jpeg' or file [-4:] == '.JPG' or file [-4:] == '.PNG' or file [-5:] == '.JPEG':
                
                old_pic = source_directory + "/" + file
                new_pic = dest_directory + "/" + file
                
                img = Image.open(old_pic)
                self.image_widht = img.width
                self.quality_dir_path.setText(str(self.image_width))

                old_pic = source_directory + "/" + file
                new_pic = dest_directory + "/" + file
                
                
                print(old_pic)
                print(new_pic)

                self.compression_code(old_pic, new_pic, self.image_width)
                
                total_images = len(files)
                images_done = i
                percentage = int(images_done/total_images*100)
                
                self.statusBar().showMessage("Message: Compressed " + str(int(images_done/total_images*100)) + "%") 

            else:
                print("ignored" + file)
                continue
        self.statusBar().showMessage("Message: Compressed")        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())