#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 23:24:26 2019
@author: wadat
"""
import pandas as pd
import requests
import matplotlib.pyplot as plt

# Pubmed search
def getPubmed(drugs, start=2004, end=2019):
    years = [year for year in range(start, end)]
    df_counts = pd.DataFrame(columns=drugs, index=years)
    for drug in drugs:
        print('Processing: {}'.format(drug))
        counts = []
        for year in years:
            searchURL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={}+AND+{}[DP]&retmode=json'.format(drug, year)
            result = requests.get(searchURL)
            data = result.json()
            count = int(data['esearchresult']['count'])
            counts.append(count)
        df_counts[drug] = counts

    # Return data as DataFrame
    return df_counts

def plotLine(df, savefig=False, fname='pubmed_hit'):
    # Visualization
    df.plot()
    plt.xlabel("Year", fontsize=18)
    plt.ylabel("Hit count in Pubmed", fontsize=18)
    plt.legend(fontsize=14)
    plt.tick_params(labelsize=16)
    if savefig:
        plt.savefig('{}.pdf'.format(fname), bbox_inches="tight", dpi=600, figsize=(16,14))
    plt.show()

if __name__ == '__main__':

    ici = ['ipilimumab','nivolumab','pembrolizumab','atezolizumab','durvalumab','tremelimumab','spartalizumab']
    df_ici = getPubmed(drugs=ici)
    plotLine(df_ici, savefig=True, fname='pubmed_ici')
