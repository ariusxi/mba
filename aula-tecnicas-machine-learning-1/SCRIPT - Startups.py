# -*- coding: utf-8 -*-

# Técnicas de Machine Learning
# MBA em Engenharia de Software USP ESALQ

# Prof. Dr. Wilson Tarantin Jr.

#%% Instalando os pacotes necessários

!pip install pandas
!pip install numpy
!pip install statsmodels
!pip install matplotlib
!pip install seaborn
!pip install pingouin
!pip install statstests
!pip install scipy

#%% Importando os pacotes

import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import pingouin as pg
from statstests.process import stepwise

#%% Importando o banco de dados

startup = pd.read_csv("startups.csv")
## Fonte: Startup - Multiple Linear Regression: https://www.kaggle.com/karthickveerakumar/datasets

#%% Estatísticas descritivas

# Variáveis métricas
print(startup.drop(columns=['State']).describe())

# Matriz de correlações
pg.rcorr(startup.drop(columns=['State']),
         method = 'pearson', upper = 'pval', 
         decimals = 4, 
         pval_stars = {0.01: '***', 0.05: '**', 0.10: '*'})

# Variáveis categóricas
print(startup['State'].value_counts())

#%% Análise por estados

lucro_medio = startup[['State', 'Profit']].groupby(by=['State']).mean()

sns.barplot(data=lucro_medio, x='State', y='Profit', palette='rocket')
plt.title("Lucro Médio por Estado")
plt.xlabel('Estado',fontsize=12)
plt.ylabel('Lucro',fontsize=12)
plt.tick_params(labelsize=6)
plt.show()

#%% Criação das variáveis binárias

startup_dummy = pd.get_dummies(data=startup, 
                               columns=['State'], 
                               drop_first=False,
                               dtype='float')

#%% Regressão Linear Múltipla

# Estimação do modelo
reg_startup = sm.OLS.from_formula(formula = 'Profit ~ RDSpend + Administration + MarketingSpend + State_California + State_Florida',
                                  data=startup_dummy).fit()

# Obtenção dos outputs
reg_startup.summary()

#%% Aplicando o stepwise ao modelo

# Procedimento stepwise para a remoção de variáveis não significativas
modelo_step = stepwise(reg_startup, pvalue_limit=0.05)

modelo_step.summary()

#%% Valores preditos pelo modelo para as observações da amostra

startup['fitted'] = modelo_step.fittedvalues

#%% Analisando os resíduos do modelo

# resíduos = valores observados - valores preditos
modelo_step.resid

#%% Analisando graficamente o resultado: gráfico 1

sns.scatterplot(data=startup, x='RDSpend', y='Profit', size='MarketingSpend', hue='State')
plt.title("Análise das Startups")
plt.xlabel('Investimento P&D',fontsize=10)
plt.ylabel('Lucro',fontsize=10)
plt.tick_params(labelsize=6)
plt.legend(bbox_to_anchor=(1,1), fontsize='7')
plt.show()

#%% Analisando graficamente o resultado: gráfico 2

sns.scatterplot(data=startup, x='RDSpend', y='Profit', size='Administration', hue='State', palette='viridis')
plt.title("Análise das Startups")
plt.xlabel('Investimento P&D',fontsize=10)
plt.ylabel('Lucro',fontsize=10)
plt.tick_params(labelsize=6)
plt.legend(bbox_to_anchor=(1,1), fontsize='7')
plt.show()

#%% Predict

# Em média, qual é o lucro estimado da startup que investe $100.000 em P&D?

# Utilizando a função "predict"
obs_simples = pd.DataFrame({'RDSpend': [100000]})
print(f'lucro predito: {round(modelo_step.predict(obs_simples)[0],0)}')

# Equivale ao cálculo manual
modelo_step.params.iloc[0] # intercepto
modelo_step.params.iloc[1] # beta RDSpend
round(49032.899 + (0.85429*100000),0)

#%% Fim!