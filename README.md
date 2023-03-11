# LRGD_NFL
Logistic Regression Gradient Descent (LRGD)
This is a model worked on during the 2022 NFL season to calculate win percentages
Today is the day I decided to dump the code to my github (3/11/2023)

TODO/Issues:
The algorithm was fairly effective, but during the later part of the season, I saw a decrease in reliableness in the algorithm.
I believe a big part of this was due to key player injuries which the algorithm couldn't quite adjust too.
To remedy this, the best way to solve this issue is to modify the data during the preprocessing step, as variables could be added
such that the logistic regression equation could reliably indicate a player injury (mainly QBs).
This would add another step to data collection which is very time consuming.
Another step would be to modify the variables to be more flexible by setting the varibles to a certain exponent x (c^x, where c is an independednt variable)
This would require extensive testing, reasoning, and experimenting to find what value x would need to be, and to find
which independent variables would benefit the most with an exponenet.


