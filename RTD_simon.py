############ Packages ############
import pandas as pd
import functools as ft
import numpy as np
import matplotlib.pyplot as plt

############ Read in Data and rename ############
data_path = 'C:/Users/Simon/Desktop/ETH/Master/Labor/UWM/RTD/Data/'

data_rasp1 = pd.read_csv(data_path + "rasp1.csv")
data_rasp2 = pd.read_csv(data_path + "rasp2.csv")
data_rasp3 = pd.read_csv(data_path + "rasp3.csv")

rasp1 = pd.DataFrame(data_rasp1)
rasp2 = pd.DataFrame(data_rasp2)
rasp3 = pd.DataFrame(data_rasp3)

dfs = [rasp1, rasp2, rasp3]
i = 1 # counting variable for the three sensors
for r in dfs:
    r.drop(columns=["ISE pH", "Temperature AtlasScientific"], inplace=True)
    r.rename(columns = {"Conductivity AtlasScientific" : "Cond_" + str(i),
                            "ISE NH4 mV" : "NH4_" + str(i),
                            "ISE NO3 mV" : "NO3_" + str(i)}, inplace = True)
    i += 1


############ Merge data and datetime ############
rasps = ft.reduce(lambda left, right: pd.merge(left, right, on='Time'), dfs)
rasps.drop(rasps.index[0], inplace = True) # drop first row with units
rasps["datetime"] = pd.to_datetime(rasps["Time"])
rasps.set_index("Time", inplace = True)


############ Concentrations ############
c1 = 3   # mg/l
c2 = 30  # mg/l
c_log = np.array([np.log10(c1),np.log10(c2)])
c_cond = [5, 10, 15, 20, 25, 30] # concentration steps during conductivity calibration
c_cond = [float(s) for s in c_cond]


############ Times of adding solution for ISE measurement ############
times_ise =     ['2022-10-13 11:17:15', '2022-10-13 11:27:00']

############ ISE NH4 calibrations and plot ############
nh4s = ["NH4_1", "NH4_2", "NH4_3"]
i = 1 # counting variable
for nh4 in nh4s: # iterate sensors 1 to 3 for nh4
    e1 = float(rasps[nh4][times_ise[0]])
    e2 = float(rasps[nh4][times_ise[1]])
    
    e = np.array([e1, e2])
    nh4_lin_reg = np.polyfit(c_log, e, deg = 1, rcond = None)
    fig = plt.figure("NH4")
    plt.plot([c1, c2], [e1, e2], 
             label="Sensor " + str(i) + ": Y = " + "{:.2f}".format(nh4_lin_reg[0]) + "*X "+ "{:.2f}".format(nh4_lin_reg[1]))
    plt.title("ISE NH4")
    plt.xlabel("Concentration [mg/L]")
    plt.ylabel("Signal [mV]")
    plt.legend(loc = "lower right", fontsize = "small")
    i+=1


############ ISE NO3 calibrations and plot ############
no3s = ["NO3_1", "NO3_2", "NO3_3"]
i = 1 # counting variable
for no3 in no3s: # iterate sensors 1 to 3 for no3
    e1 = float(rasps[no3][times_ise[0]])
    e2 = float(rasps[no3][times_ise[1]])
    
    e = np.array([e1, e2])
    no3_lin_reg = np.polyfit(c_log, e, deg = 1, rcond = None)
    fig = plt.figure("NO3")
    plt.plot([c1, c2], [e1, e2], 
             label="Sensor " + str(i) + ": Y = " + "{:.2f}".format(no3_lin_reg[0]) + "*X "+ "{:.2f}".format(no3_lin_reg[1]))
    plt.title("ISE NO3")
    plt.xlabel("Concentration [mg/L]")
    plt.ylabel("Signal [mV]")
    plt.legend(loc = "lower right", fontsize = "small")
    i+=1
    
    
############ Cond calibrations and plot ############
times_cond =    ['2022-10-13 12:07:45', '2022-10-13 12:14:00', # Times of adding solution to measure conductivity
                 '2022-10-13 12:16:00', '2022-10-13 12:17:50', 
                 '2022-10-13 12:19:40', '2022-10-13 12:21:30']
conds = ["Cond_1", "Cond_2", "Cond_3"] # conductivity of sensor 1-3
i = 1 # iterating variable
for cond in conds:
    cond_list = [float(rasps[cond][times_cond[j]]) for j in range(6)] # list comprehension, get cond values at the given times
    cond_lin_reg = np.polyfit(c_cond, cond_list, deg = 1, rcond = None)
    trend = np.poly1d(cond_lin_reg)
    fig = plt.figure("Cond")
    plt.plot(c_cond, trend(c_cond), 
             label="Sensor " + str(i) + ": Y = " + "{:.2f}".format(cond_lin_reg[0]) + "*X +"+ "{:.2f}".format(cond_lin_reg[1]))
    #plt.plot(c_cond, cond_list, label="Sensor " + str(i) + ": Y =" + "{:.2f}".format(lin_reg[0]) + "*X + "+ "{:.2f}".format(lin_reg[1]))
    plt.title("Conductivity")
    plt.xlabel("Concentration [mg/L]")
    plt.ylabel("Conductivity [uS/cm]")
    plt.legend(loc = "lower right", fontsize = "small")
    i+=1

"""
############ New df with calibrated values ############
ts_vars = ["NH4_1", "NO3_2", "Cond_3"]
fig = plt.figure("TS")
for var in ts_vars:
    plt.plot(rasps["datetime"], rasps[i].astype(float)) #typproblem! spalten sind nicht floats sondern iwas anderes



### Plot
fig, ax = plt.subplots()
ax.plot(rasps["datetime"], rasps["NH4_1"].astype(float), label = "NH4_1", color = "mediumblue", linewidth=1)
ax.set_title("Siuu")
ax.legend(loc='lower left', prop={'size': 6})
ax.set_ylabel("Temperature [°C]")
ax.set_xlabel("Time")
#plt.savefig("H:\Diverses\ICOS-PAUL\Sensortest\Plots/" + "BOXTEMP " +  i, dpi = 1200)
#sns.lineplot(x="datetime", y="NH4_1",
          #   data=rasps)
"""