# Colorifix Technical Test
#### Ebrahim Jahanshiri


#### :computer: The setup
Due to time constraints, I am going to build the app with <code> Dash </code> :blush: There are two apps app1.py and app2.py corresponding to the two parts of the assignment. To run the apps, you will need to setup your enviornment make sure you have dash, dash_bootstrap_components, pandas, plotly.graph_objs and dash_table installed. The environment is set with poetry to make it easier to track the versions and packages. 

:bell: The app1 application requires two inputs from the user, "Calibration" and "Sample" in CSV format. 
The system will then calculate absorption coeficient and plots them against different dilutions in the sample. It will also draw a coeificent plot for the Blanks. The 

:rainbow: The concentration is not given in the Calibration dataset and therefore we will need to find a way to find the absorption coeficient for each dilustion, and then calculate the concentration for the corresponding sample
The absorbsion coeficient (E) can be calculated based on the formula that is presented here: E = ln(1-A)/l = 2.303 A/l. E = Absorption / ( log e) * Thickness 
E = 2,302585 Absorption / thickness, Where log e = 0.4342944819
We will calculate E for each dilusion and plot them against the wavelength to find the maximum absorption for that dilusion (it can absorb light more efficiently). 
We will then take the value for E and calculate the pigment concentration for the corresponding dilusion in the sample dataset. 


After accepting the files, the app will do a simple EDA by making a bar chart of Absorbance against the wavelengths. This will allow us to visulise the responsoe against the wavelengths and possibly will be helpful for choosing a representative length. We could also do a more thorogh analysis for choosing the representative wavelength. 
After this, the app will do the modelling. Here we will use the absorbance data of the chosen wavelength to calibrate a model (possibly regression) to derive the concentration. 

t

We must add another row to the calibration dataset and calculate E based on A and l for each wavelenght. This will give us a graph of Wavelength against E from which we can get a constant value for each sample and also a reprsentative wavelength to calculate the concentration. 

Since the pigment is the same for both calibration and sample data, we can then calculate the coeficient for each wavelength and each dilusion. Then given that E is know for each dilusion, we will calculate the concentration value for each sample based on the E value for each dilusion and the creates the results as a table. 

We will then use the calibrated model to calculate the concentration (c) for each sample. 



https://study.com/academy/lesson/the-absorption-coefficient-definition-calculation.html#:~:text=The%20absorption%20coefficient%20is%20calculated,%2F(thickness%20of%20material).
https://www.youtube.com/watch?v=rmDUBdf-6_8 
https://www.researchgate.net/post/How_can_I_calculate_absorption_coefficient_from_absorbance
https://www.youtube.com/watch?v=rmDUBdf-6_8
https://www.researchgate.net/post/How_can_I_calculate_the_Absorption_coefficient_from_Absorbance2#:~:text=Absorption%20coefficient%20k%20%3D%20A%2Fd,get%20k%20in%20cm%2D1.&text=and%20the%20coeficient%202.303%20arises,conversion%20factor%20ln(10).

