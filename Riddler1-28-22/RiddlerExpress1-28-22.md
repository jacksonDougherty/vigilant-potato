# Riddler - Solutions to Riddler Express (Modified Game of Life)

The riddler for 1-28-21 is a [modified Game of Life](https://fivethirtyeight.com/features/can-you-tune-up-the-truck/) without overpopulation. Using the python script, we can (deterministically) simulate the growth to ten generations, where there are **89** living cells. 

For the extra credit, we are asked about long time population dynamics. By extending the simulation, we can observe the population extends to approximately form a circle. Moreover, the radius of the circle grows once every two generations. Therefore, as the generation $N \rightarrow \infty$, we have approximately $\lfloor \pi N^2/4 \rfloor$ living cells. 