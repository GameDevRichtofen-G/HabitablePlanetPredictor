import sys
import math
import random
import numpy as np
import keras as keras
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtWidgets import QLabel



class GLWidget(QOpenGLWidget):
    #setting up
    global Distances
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.angle = 0  
        self.stars = []
        self.num_stars = 200
        self.distance = 1
        self.mass = 1
        self.planet_distance = 0
        self.sun_position = [300.0 , 5.0, 0.0, 1.0]
        self.generateStars()
        self.timer = QTimer()
        self.planet_material = [0.7, 0, 0, 1.0]
        self.timer.timeout.connect(self.update_camera)
        self.timer.start(16)  

    #creating the starss
    def generateStars(self):
    
        for _ in range(self.num_stars):
            theta = random.uniform(0, math.pi)
            phi = random.uniform(0, 2 * math.pi)
            radius = random.uniform(200,400)
            x = radius * math.sin(theta) * math.cos(phi)
            y = radius * math.sin(theta) * math.sin(phi)
            z = radius * math.cos(theta)
            #had a really hard time with spawning the stars, but it turn out well :D 
            self.stars.append((x, y, z))
            

    #setting up opengl
    def initializeGL(self):
        #setting up, lights and materials
        glClearColor(0.05, 0.05, 0.05, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT7)
        glLightfv(GL_LIGHT7, GL_DIFFUSE, [1, 1, 1, 1])
        glLightfv(GL_LIGHT7, GL_SPECULAR, [1,1, 1, 1])
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_NORMALIZE)
        
    
    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, w / float(h if h != 0 else 1), 1.0, 100000.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        #creating a orbit around the planet
        orbit_radius = 3.0
        #changing the rotation of camera base on planet
        rad = math.radians(self.angle)
        camera_x = (orbit_radius * self.mass) * math.sin(rad)
        camera_z = (orbit_radius * self.mass) * math.cos(rad)
        
        camera_y = 0.0  
        # setting up a simple camera
        gluLookAt(camera_x, camera_y, camera_z,
                  0, 0, 0,
                  0, 1, 0)

        
   
        #fix the light, so it stays in place
        glLightfv(GL_LIGHT7, GL_POSITION, [self.sun_position[0] * self.distance,self.sun_position[1],self.sun_position[2]])
        
        #creating the sun
        
        glPushMatrix()
        glTranslatef(self.sun_position[0] * self.distance, self.sun_position[1], self.sun_position[2])
        glScalef(33,33,33)
        #adding the material to the sun
        glMaterialfv(GL_FRONT, GL_EMISSION, [1.0, 1.0, 0.0, 1.0])
        quadric = gluNewQuadric()
        gluSphere(quadric, 0.5, 30, 30)
        gluDeleteQuadric(quadric)
        #reset material for others
        glMaterialfv(GL_FRONT, GL_EMISSION, self.planet_material)
        glPopMatrix()

        #create the planet
        glPushMatrix()
        glScalef(1 * self.mass,1 * self.mass,1 * self.mass)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [0.2, 0.5, 0.8, 1.0])
        quadric = gluNewQuadric()
        gluSphere(quadric, 0.5, 50, 50)
        gluDeleteQuadric(quadric)
        glPopMatrix()
        
        #create the stars
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        #disable light on stars
        glDisable(GL_LIGHTING) 
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)  
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glPointSize(3.0)
        glBegin(GL_POINTS)
        for star in self.stars:
            glVertex3f(star[0], star[1], star[2])
        glEnd()
        glPopAttrib()

    #update the camera
    def update_camera(self):
        self.angle = (self.angle + 0.5) % 360
        
        self.update()

class MainWindow(QWidget):
    def __init__(self):
        #setting up some of the essentials. not really :/
        super().__init__()
        self.setWindowTitle("PREDICT PLANET")
        self.setMinimumSize(800, 600)
        self.initUI()
        
        

    def initUI(self):
        
        main_layout = QHBoxLayout(self)

        # add widget for opengl 
        self.glWidget = GLWidget(self)
        main_layout.addWidget(self.glWidget, 2)

        # add a panel for right side
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # creating the fields.
        form_layout = QFormLayout()
        self.field1 = QLineEdit()
        self.field2 = QLineEdit()
        self.field3 = QLineEdit()
        self.field4 = QLineEdit()
        self.field5 = QLineEdit()
        self.field6 = QLineEdit()
        self.field7 = QLineEdit()
        self.field8 = QLineEdit()
        form_layout.addRow("DAILY HOUR :", self.field1)
        form_layout.addRow("MASS(EARTH) :", self.field2)
        form_layout.addRow("DISTANCE(AU) :", self.field3)
        form_layout.addRow("ECCENTRICITY :", self.field4)
        form_layout.addRow("WATER PRESENCE(%) :", self.field5)
        form_layout.addRow("STELLAR FLUX(EARTH) :", self.field6)
        form_layout.addRow("SURFACE TEMPERATURE(K) :", self.field7)
        form_layout.addRow("ATMOSPHERIC PRESSURE(bar) :", self.field8)
        
        self.field1.textChanged.connect(self.update_values)
        self.field2.textChanged.connect(self.update_values)
        self.field3.textChanged.connect(self.update_values)
        self.field4.textChanged.connect(self.update_values)
        self.field5.textChanged.connect(self.update_values)
        self.field6.textChanged.connect(self.update_values)
        self.field7.textChanged.connect(self.update_values)
        self.field8.textChanged.connect(self.update_values)

        
        #add layout 
        right_layout.addLayout(form_layout)

        
        # Add the Predict button.
        self.predict_button = QPushButton("PREDICT")

        self.predict_button.pressed.connect(self.Predit)


        
        right_layout.addWidget(self.predict_button)


        self.result_label = QLabel("")
        right_layout.addWidget(self.result_label)

        # stretch to push the controls to the top.
        right_layout.addStretch()
        main_layout.addWidget(right_panel, 1)

        # applying a dark theme 
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #dcdcdc;
                font-size: 14px;
            }
            QLineEdit, QCheckBox, QPushButton {
                background-color: #3c3f41;
                border: 1px solid #565656;
                padding: 5px;
            }
            QPushButton {
                background-color: #4c5052;
                
            }
                           
            QPushButton:hover 
            {
                background-color: #0055b3; 
                border: 2px solid #002f7f;
                
            }
                           
        """)
    
    def update_values(self):
       
        
        distance_value = float(self.field3.text()) if self.field3.text() else 0.0
        mass_value = float(self.field2.text()) if self.field2.text() else 0.0

        if distance_value < 0.1 or distance_value == None: 
            self.glWidget.distance = 1
        else :
            self.glWidget.distance = distance_value
        
        if mass_value < 0.2 or mass_value == None :
            self.glWidget.mass = 1
        else :

            self.glWidget.mass = mass_value
        
        self.glWidget.planet_material = self.UpdateMaterial()


    def UpdateMaterial(self):
        distance_value = float(self.field3.text()) if self.field3.text() else 0.0 
        mass_value = float(self.field2.text()) if self.field2.text() else 0.0
        if distance_value <= 0 :
            distance_value = 1

        if mass_value < 24 :
            redCH = min(1,mass_value/22 + 0.2 / distance_value)
            greeenCH =  (1 - redCH) / 2
            blueCH = min(1,distance_value/5)

            return [redCH,greeenCH,blueCH]
        else :
            if mass_value >= 24 :
                return [1,1,0,1]
            
    def Predit(self) :
        mass = float(self.field2.text()) if self.field2.text() else 0.0
        distance  = float(self.field3.text()) if self.field3.text() else 0.0
        StF = float(self.field6.text()) if self.field6.text() else 0.0
        OrDays = float(self.field1.text()) if self.field1.text() else 0.0
        Eccentricity = float(self.field4.text()) if self.field4.text() else 0.0
        Temp = float(self.field7.text()) if self.field7.text() else 0.0
        atm = float(self.field8.text()) if self.field8.text() else 0.0
        water = float(self.field5.text()) if self.field5.text() else 0.0
        Model = keras.models.load_model("Train.h5")
        sample_input = np.array([[mass,distance,StF,OrDays,Eccentricity,Temp,atm,water]])
        print(sample_input)
        prediction = Model.predict(sample_input,verbose=0)
        Result =  round(prediction[0][0])
        printedRESULT = "Habitable" if Result == 1 else "Not-Habitable"
        self.result_label.setText(f"PREDICTED OUTPUT: {printedRESULT}")

    
        

       
        
    
    
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
