    import sys 
sys.path.append(r'C:\Users\aleja\Documents\J288 Gregory Data\Photos Week 1 Sojitz\Not_grating')
from _engine import SingleMeasurement, FFTDomain, DataVisualizer
from pathlib import Path
from serviceability_vib import Service_assessment


# %% B4C5 Z
path = Path(r"C:\Users\aleja\Documents\J288 Gregory Data\healt_data_iso2631\EqualizedFile.dat")
name = '27_05_2023-grid B4-C5'
measurement = SingleMeasurement(name,128,path).load_asc(cols=[0,1,2,3,4,5])
acc_m_s2 = measurement.data[:,5]*9.81/1000
Service_assessment(acc_m_s2,128,'Z',8).BS_6472()

# %% B4C5 Y
name = 'A5 26/05/2023'
path = Path(r"C:\Users\aleja\Documents\J288 Gregory Data\healt_data_iso2631\HERE_001part1\EqualizedFile.dat")
measurement = SingleMeasurement(name,128,path).load_asc(cols=[0,1,2,3,4,5])
acc_m_s2 = measurement.data[:,4]*9.81/1000
Service_assessment(acc_m_s2,128,'Y',8).BS_6472()


# %% screen flooor 
        # F2-F3
name = 'Vibrations screens F2-F3 27/05/2023'
path =Path(r"C:\Users\aleja\Documents\J288 Gregory Data\data_check_2023_27\27_06_2023_044part1\EqualizedFile.dat")
measurement = SingleMeasurement(name,128,path).load_asc(cols=[0,1,2,3,4,5])
acc_m_s2 = measurement.data[:,5]*9.81/1000
Service_assessment(acc_m_s2,128,'Z',8).BS_6472()
        # tromino 5 - set up 3 - FG/45
name = 'Vibrations screens FG/45 26/05/2023'
path =Path(r"C:\Users\aleja\Documents\J288 Gregory Data\data_check_2022_26\24_06_2023_024part1\EqualizedFile.dat")
measurement = SingleMeasurement(name,128,path).load_asc(cols=[0,1,2,3,4,5])
acc_m_s2 = measurement.data[:,5]*9.81/1000
Service_assessment(acc_m_s2,128,'Z',8).BS_6472()
        # tromino 5 - set up 3 - D5-E5
name = 'Vibrations screens D5-E5 26/05/2023'
path =Path(r"C:\Users\aleja\Documents\J288 Gregory Data\data_check_2022_26\24_06_2023_025part1\EqualizedFile.dat")
measurement = SingleMeasurement(name,128,path).load_asc(cols=[0,1,2,3,4,5])
acc_m_s2 = measurement.data[:,5]*9.81/1000
Service_assessment(acc_m_s2,128,'Z',8).BS_6472()


