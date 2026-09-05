<!-- page 1 -->

## **Sunitinib for GIST: additional notes for the ACD meeting from PenTAG** 

By Martin Hoyle 

The purpose of this note is to provide further explanation (in addition to our report) of the Rank Preserved Structural Failure Time (RPSFT) model for the analysis of crossover data from the RCT by Demetri et al. 2006/2008. 

## **1. RPSFTM.** 

- As far as we know, this method has never been used in published cost-effectiveness analyses. 

- We are not experts in the method.  Also, we do not have the required IPD to re-run the analysis. 

- Ian White (an unpaid independent statistician from the MRC Biostatistics Unit, University of Cambridge), who has published on this method, has endorsed the use of the RPSFT method for the analysis of the crossover data from the Demetri et al. 2006/08 trial. 

- However, he did not actually perform the analysis. 

## **Simple method explanation** 

• Problem: In the RCT, 84% of patients randomised to placebo crossed over to sunitinib at the moment of disease progression. 

• OPTION 1: Use the unadjusted ITT data.  Problem is that this underestimates the true treatment effect of sunitinib, due to patients crossing over from placebo to sunitinib. 

• OPTION 2: Censor placebo arm patients at the point of crossover.  Problem is that this introduces bias, because the 84% of patients who cross over are unlikely to be comparable to those who do not. 

For example, they may have been healthy enough to be judged to withstand treatment with sunitinib.  The remaining 16% of patients may have been too ill to withstand sunitinib, and therefore, they may have had a shorter life expectancy than those patients who crossed over to sunitinib, even if the patients who crossed over were not to take sunitinib.  If we censored those healthier patients who crossed over at the time of crossover, we would underestimate the true survival of placebo patients. 

• OPTION 3: The RPSFT method estimates the times of death of patients of all individuals randomised to placebo assuming they had not crossed over, i.e. had stayed on placebo.  We then create a Kaplan-Meier curve from these estimated times of death. 

1 



<!-- page 2 -->

The beauty of the RPSFT method is that it is unbiased because it is based on comparisons of groups as randomised. 

The model assumes treatment increases survival by an unknown x% over the period that the treatment is applied. 

x% is calculated as follows.  For each individual (in placebo arm and in sunitinib arm), you estimate the survival time of that individual as if he/she had always been on placebo. This is done by reducing the survival time of that individual by x% for the portion of time the individual is on sunitinib treatment.  For example, for patients randomised to sunitinib, you reduce their whole survival time by x%.  For patient randomised to placebo, you reduce only that portion of their survival time for which they took sunitinib. You leave unchanged that portion of their survival time for which they did not take sunitinib. 

Finally, you chose x% so that the mean of these times, the estimated survival times assuming patients had always been on placebo, in the two treatment arms are equal. 

## **Assumptions** 

- Treatment has the same effect on survival for everyone, regardless of when and under what circumstances treatment is started.  This is not necessarily true, but minor departures probably won't matter much. 

- No assumptions about how treated people's survival relates to that of untreated people: instead the model relates treated people's survival to THEIR OWN survival if they hadn't been treated. 

## **Results** 

- Method appropriately increases the treatment effect of sunitinib, i.e. it makes the sunitinib HR more favourable. 

- Method does not change the level of evidence against the null hypothesis. As a result, the 95% confidence interval is wide. 

## **Technical method explanation** 

- U = Tstart + exp( ψ )(T-Tstart) where; 

   - T is the observed time of death, 

   - Tstart is the time of starting treatment, 

   - U is the death time that would have been observed if no treatment had been given, 

   - ψ is the causal effect of having started treatment. 

- ψ is estimated by computing U for a range of possible values of ψ and finding the value for which a log rank test of the equality of U across the two groups (placebo and sunitinib) gives a zero test statistic. 

2 

