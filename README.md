# HABITABLE PLANET PREDICTOR

## ABOUT

Made model using `tensorflow` that can predict whether planet is habtiable or not-habitable base on provided values.
These values or parameters can be use to predict upcoming outcome. This project meant to teach me how to use PyQt5.
### `PARAMETERS : `

* `MASS(EARTH)` : The mass of the planet in Earth units
* `SURFACE TEMPERATURE` : The planets surface temperture
* `ATMOSPHERIC PRESSURE(bar)` : the force exerted by a planet's atmosphere
* `DISTANCE(AU)` : The distance between planet and its host star in astronomical unit
* `ORBITAL(D)` : How long does it take for planet to does full orbit around its host star

* `ECCENTRICITY` : describes the extent to which an orbit is elliptical or deviates from a perfect circle
* `WATER PRESENCE(%)` : the percentage of the planet's total mass or surface area that is composed of water
* `STELLAR FLUX(EARTH)` : the amount of solar energy (or radiation) a planet receives from its star, relative to the amount Earth receives from the Sun


![Example Image](https://github.com/GameDevRichtofen-G/HabitablePlanetPredictor/blob/main/image-s.PNG)






## DATA-SET : 

I made a data-set containing 40 different habitable and non-habitable planets.
| Planet Name  | Mass (Earth Masses) | Distance from Star (AU) | Stellar Flux (Earth Units) | Radius (Earth Radii) | Orbital Period (days) | Eccentricity | Surface Temperature (K) | Atmospheric Pressure (bar) | Water Presence (%) | Target |
|-------------|--------------------|-------------------------|----------------------------|----------------------|----------------------|-------------|-------------------------|---------------------------|--------------------|--------|
| TRAPPIST-1e | 0.692              | 0.029                   | 0.65                       | 0.92                 | 6.1                  | 0.02        | 245                     | 1.2                       | 68                 | 1      |
| Kepler-10b  | 3.33               | 0.0168                  | 16.0                       | 1.47                 | 0.837                | 0.05        | 1833                    | 0.0                       | 0                  | 0      |

The task is to see whether Target is 1(Habitable) or 0(Non-habitable)


## MODEL : 
I used Torch and tensorFlow to train a NN binary classification model based on the dataset. The model predicts whether a given planet is habitable or not based on the provided input.

----------------------------
----------------------------

## HOW TO USE 
1. Install Dependencies  
       Run the following command to install all required packages:  
       ```
       pip install -r requirements.txt
       ```
2. Run the Prediction Script  
       Execute the script with:  
       ```
       python Predict.py
       ```
