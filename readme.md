PC2 daily prediction from monthly value

The easiest approach is to consider constant dialy value within a month by dividing monthly value to the month duration. Then we would have a step function where auc within each step would be PC2 value. But this approach lacks continiueity of the function which makes it quite non-applicale. 

Another approach is to claculate a curve with one vital constrain: "area under the curve for each month has to be PC2". Also, for the sake of continueity, we modify the value of the function at adjescent of months to be the average of two values; last day of prevoius month, and first day of the next one. Then we calculate the formula of the function in each month using second order polynomial
