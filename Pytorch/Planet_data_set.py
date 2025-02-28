import pandas as pd 
import numpy as np

#I found these in internet and they might be valid



valid_extra_planets = {
    "Planet Name": [
        "Kepler-22b", "TRAPPIST-1d", "TRAPPIST-1e", "TRAPPIST-1f", "TRAPPIST-1g",
        "Proxima Centauri b", "TOI-700d", "LHS 1140 b", "Ross 128 b", "Teegarden b",
        "Kepler-186f", "Kepler-62f", "Gliese 667 Cc", "GJ 1214 b", "Wolf 1061c",
        "Kapteyn b", "Kepler-442b", "Kepler-1652b", "GJ 1061 d", "YZ Ceti d"
    ],
    "Mass (Earth Masses)": [
        5.36, 0.388, 0.692, 1.04, 1.34,
        1.17, 2.1, 6.65, 1.35, 1.05,
        1.17, 2.8, 4.2, 8.3, 4.3,
        4.8, 2.34, 2.5, 1.6, 1.2
    ],
    "Distance from Star (AU)": [
        0.85, 0.022, 0.029, 0.037, 0.045,
        0.048, 0.067, 0.10, 0.05, 0.03,
        0.43, 0.71, 0.12, 0.05, 0.08,
        0.168, 0.41, 0.23, 0.08, 0.016
    ],
    "Stellar Flux (Earth Units)": [
        1.11, 0.86, 0.65, 0.38, 0.26,
        0.70, 0.85, 0.46, 1.38, 1.15,
        0.32, 0.41, 0.90, 1.1, 0.75,
        0.48, 0.63, 0.57, 0.34, 0.80
    ],
    "Radius (Earth Radii)": [
        2.4, 0.788, 0.92, 1.0, 1.15,
        1.1, 1.2, 1.43, 1.05, 1.02,
        1.11, 1.4, 1.52, 2.7, 1.6,
        1.2, 1.34, 1.3, 1.18, 1.08
    ],
    "Orbital Period (days)": [
        289.9, 4.05, 6.1, 9.2, 12.4,
        11.2, 37.4, 24.7, 9.9, 4.9,
        130, 267, 28.2, 38.0, 17.9,
        48.6, 112.3, 83.1, 44.1, 2.0
    ],
    "Eccentricity": [
        0.02, 0.04, 0.02, 0.03, 0.04,
        0.05, 0.02, 0.01, 0.06, 0.02,
        0.02, 0.03, 0.02, 0.04, 0.03,
        0.05, 0.02, 0.04, 0.06, 0.02
    ],
    "Surface Temperature (K)": [
        295, 230, 245, 220, 210,
        250, 265, 290, 280, 275,
        275, 265, 290, 400, 285,
        290, 260, 270, 250, 280
    ],
    "Atmospheric Pressure (bar)": [
        1.3, 0.9, 1.2, 1.1, 1.3,
        1.0, 1.1, 1.4, 1.2, 1.3,
        1.1, 1.0, 1.5, 2.0, 1.3,
        1.4, 1.1, 1.2, 1.0, 1.2
    ],
    "Water Presence (%)": [
        70, 65, 68, 72, 75,
        80, 78, 74, 66, 70,
        68, 72, 80, 50, 77,
        74, 66, 70, 75, 73
    ],
    "Target": [1] * 20  # all are considered potentially habitable
}




non_habitable_planets = {
    "Planet Name": [
        "KELT-9b", "WASP-12b", "HD 189733b", "55 Cancri e", "Gliese 1132 b",
        "Kepler-10b", "GJ 9827 d", "Kepler-70b", "CoRoT-7b", "LHS 3844b",
        "TOI-849b", "GJ 1252b", "Kepler-422b", "WASP-19b", "TOI-674b",
        "HD 209458b", "Kepler-78b", "Kepler-7b", "Kepler-13Ab", "WASP-103b"
    ],
    "Mass (Earth Masses)": [
        2.88, 1.46, 1.15, 8.63, 1.66,
        3.58, 4.65, 5.02, 7.4, 2.25,
        39.0, 2.7, 5.8, 1.1, 23.1,
        2.6, 1.7, 0.75, 3.8, 1.2
    ],
    "Distance from Star (AU)": [
        0.034, 0.0229, 0.031, 0.0156, 0.0163,
        0.0172, 0.034, 0.0076, 0.017, 0.006,
        0.015, 0.03, 0.021, 0.016, 0.025,
        0.045, 0.01, 0.04, 0.044, 0.024
    ],
    "Stellar Flux (Earth Units)": [
        6000, 9000, 2000, 1800, 1100,
        2200, 1500, 10000, 2500, 4000,
        3000, 2750, 5000, 3800, 1900,
        2600, 3200, 1600, 4000, 3300
    ],
    "Radius (Earth Radii)": [
        1.89, 1.91, 1.4, 1.85, 1.1,
        1.43, 1.54, 1.1, 1.58, 1.3,
        3.45, 1.25, 1.62, 1.67, 1.93,
        1.7, 1.2, 1.75, 1.55, 1.48
    ],
    "Orbital Period (days)": [
        1.48, 1.09, 2.22, 0.74, 1.63,
        0.84, 1.2, 0.34, 0.85, 0.75,
        0.9, 1.15, 1.45, 0.96, 1.2,
        3.52, 0.35, 2.89, 1.76, 2.12
    ],
    "Eccentricity": [
        0.01, 0.02, 0.03, 0.04, 0.01,
        0.05, 0.03, 0.06, 0.02, 0.01,
        0.02, 0.04, 0.05, 0.02, 0.03,
        0.04, 0.01, 0.02, 0.03, 0.02
    ],
    "Surface Temperature (K)": [
        4600, 4300, 2000, 2500, 1400,
        2100, 1800, 7000, 1900, 2200,
        3000, 2400, 3300, 2100, 1800,
        1600, 2600, 2400, 3200, 2700
    ],
    "Atmospheric Pressure (bar)": [
        0, 0, 0.2, 10, 5,
        0.1, 3, 0, 8, 1,
        20, 2, 4, 0.5, 15,
        2, 0.7, 1, 12, 1.5
    ],
    "Water Presence (%)": [
        0, 0, 2, 1, 3,
        0, 4, 0, 2, 5,
        0, 1, 2, 0, 6,
        0, 0, 3, 1, 2
    ],
    "Target": [0] * 20  # all are considered non-habitable
}


DATA_habitable = pd.DataFrame(valid_extra_planets)
DATA_NON_habitable = pd.DataFrame(non_habitable_planets)


DATA = pd.concat([DATA_habitable, DATA_NON_habitable], ignore_index=True)

file_path = "planets_data.csv"


DATA.to_csv(file_path, index=False)


