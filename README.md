# Colorifix Technical Test
##### Ebrahim Jahanshiri


#### :computer: The setup
The apps are built with Python `Dash`. There are two apps `app1.py` and `app2.py` corresponding to the two parts of the assignment. To run the apps, you will need to setup the enviornment and make sure you have `dash`, `dash_bootstrap_components`, `pandas`, `plotly.graph_objs`, `requests`, and `dash_table` installed. The environment is set with `poetry` to make it easier to track the versions and packages. 

:bell: App1 requires two inputs from the user, "Calibration" and "Sample" in CSV format (the system will fetch an error if a different file format is supplied). The user will upload calibration and sample data, and the app will then calculates the concetrations in the 'Output' tab. The charts in the 'Modelling' tab show Absorptivity coefficient as a fuction of wavelengths per each dilusion level. The system will then calculate absorption coeficient and plots them against different dilutions in the sample. It will also draw a coeificent plot for the Blanks.  

:bell: App2 requires one input from the user (calibration data) and it will fetch and parse data automatically form Colorifix Notion API. There is a new tab in this app to shows the parsed data that is obtained from API. 

:warning: App2 fetches a 'NoneType error' when it is run. However, the app can still run and show the result of parsing information from the API in the 'Parsed data' tab. Also the app is incomplete due to a error in the pigment concentration calculation section and therefore the 'Output' does not show any results. Please see below for a possible cause. 

:rainbow: Under the hood!
The concentration is not given in the Calibration dataset and therefore we will need to find a way to find the absorption coeficient and then calculate the concentration for the corresponding sample. In this app, I have conditioned the Coeficient on two parameter: 1- wavelength and 2- Dlution. 
The absorbsion coeficient (`E`) can be calculated as $E = ln(1-A)/l = 2.303 A/l$. $E = Absorption / (loge) * Thickness$ , 
$E = 2,302585 Absorption / thickness$, Where $loge = 0.4342944819$.
The app will calculate E for each dilusion and plot them against the wavelength to find the maximum absorption for that dilusion (it can absorb light more efficiently). 
it will then take the value for E and calculate the pigment concentration for the corresponding dilusion in the sample dataset. 

:information_source: Representative wavelength is chosen a the wavelenght that has the highest absorptivity. Since the pigment type is the same for both calibration and sample data, we can then calculate the coeficient for each wavelength and each dilusion. Then given that `E` is known for each dilusion, we will calculate the concentration value for each sample based on the `E` value for each dilusion and the creates the results as a table. 

We will then use the calibrated model to calculate the concentration (c) for each sample. 

:bug: Issues 
App2 needs to be optimised and debugged to ratify the issue of non-conformity with the data. There are some fundamental issues with the engine and results:

:one: it seems that the strategy to use maximum wavelength should be replaced by some other criteria. This is because the coeficient (`E`) is calculated the same as for every sample! :disappointed:. However, as we can see in the charts of E against wasvelengths, all of the samples (including Blank!) seem to absorb at the same range of wavelength!. It will be interesting to look at it further. 

:two: app2 doesn't produce the results of pigment concentrations for the API samples at the moment. What needs to be done is:  
- Recetify the issue of indexing the sample data (sample-db) fetched from the API: at the moment this bug prevents the development of other parts of app2. 
- Create a loop to caluclate the sample pigment concentration based on the Coeficient E that is calibrated from the calibration data. The output is a dataframe of shape(3, 3). 
- A good way to store the output is to create a `SQL` database with the following structure:
    - Slice the sample CSV files to contain only metadata information (sample, dilution, and pigment concentration)
    - Assign SampleID `primary key` in each of 27 sample datasets. 
    - Assign the Dye house name and Sample type as `foreign key`. 


:green_book: Refrences:

https://study.com/academy/lesson/the-absorption-coefficient-definition-calculation.html#:~:text=The%20absorption%20coefficient%20is%20calculated,%2F(thickness%20of%20material).
https://www.youtube.com/watch?v=rmDUBdf-6_8 
https://www.researchgate.net/post/How_can_I_calculate_absorption_coefficient_from_absorbance
https://www.youtube.com/watch?v=rmDUBdf-6_8
https://www.researchgate.net/post/How_can_I_calculate_the_Absorption_coefficient_from_Absorbance2#:~:text=Absorption%20coefficient%20k%20%3D%20A%2Fd,get%20k%20in%20cm%2D1.&text=and%20the%20coeficient%202.303%20arises,conversion%20factor%20ln(10).

