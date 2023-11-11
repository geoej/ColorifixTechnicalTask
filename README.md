# Colorifix Technical Test
#### Ebrahim Jahanshiri


#### :computer: The setup
Due to time constraints, I am going to build the app with Dash :blush:.
There are two apps app1.py and app2.py corresponding to the two parts of the assignment. To run the apps, you will need to setup your enviornment make sure you have dash, dash_bootstrap_components, pandas, plotly.graph_objs, requests, and dash_table installed. The environment is set with poetry to make it easier to track the versions and packages. 

:bell: App1 requires two inputs from the user, "Calibration" and "Sample" in CSV format. The user will upload calibration and sample data, and the app will then calculates the concetrations in the 'Output' tab. The charts in the "Modelling" tab show Absorptivity coefficient as a fuction of wavelengths per each dilusion level. 
The system will then calculate absorption coeficient and plots them against different dilutions in the sample. It will also draw a coeificent plot for the Blanks. The 

:bell: App2 requires one input from the user (calibration data) and it will fetch and parse data automatically form Colorifix Notion API. There is a new tab in this app to shows the parse data. 
:warning: App2 fetches a 'NoneType error'. However, the app can still run and show the result of parsing information from the API in the "Parsed data" tab. Also the app is incomplete due to a error in the pigment concentration calculation section. 

:rainbow: #### Under the hood!
The concentration is not given in the Calibration dataset and therefore we will need to find a way to find the absorption coeficient for each dilustion, and then calculate the concentration for the corresponding sample. The absorbsion coeficient (E) can be calculated as : E = ln(1-A)/l = 2.303 A/l. E = Absorption / ( log e) * Thickness , 
E = 2,302585 Absorption / thickness, Where log e = 0.4342944819.
The app will calculate E for each dilusion and plot them against the wavelength to find the maximum absorption for that dilusion (it can absorb light more efficiently). 
it will then take the value for E and calculate the pigment concentration for the corresponding dilusion in the sample dataset. 

:information_source: Representative wavelength is chosen a the wavelenght that has the highest absorptivity. 

Since the pigment is the same for both calibration and sample data, we can then calculate the coeficient for each wavelength and each dilusion. Then given that E is know for each dilusion, we will calculate the concentration value for each sample based on the E value for each dilusion and the creates the results as a table. 

We will then use the calibrated model to calculate the concentration (c) for each sample. 

:information_source: ### issues 
The app2 needs to be optimised and debugged to ratify the issue of non-conformity with the data.

https://study.com/academy/lesson/the-absorption-coefficient-definition-calculation.html#:~:text=The%20absorption%20coefficient%20is%20calculated,%2F(thickness%20of%20material).
https://www.youtube.com/watch?v=rmDUBdf-6_8 
https://www.researchgate.net/post/How_can_I_calculate_absorption_coefficient_from_absorbance
https://www.youtube.com/watch?v=rmDUBdf-6_8
https://www.researchgate.net/post/How_can_I_calculate_the_Absorption_coefficient_from_Absorbance2#:~:text=Absorption%20coefficient%20k%20%3D%20A%2Fd,get%20k%20in%20cm%2D1.&text=and%20the%20coeficient%202.303%20arises,conversion%20factor%20ln(10).

