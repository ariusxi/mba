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

casas = pd.read_excel("preco_casas.xlsx")
## Fonte: https://www.kaggle.com/datasets/elakiricoder/jiffs-house-price-prediction-dataset

#%% Estatísticas descritivas

# Variáveis métricas
tab_desc = casas[['land_size_sqm',
                  'house_size_sqm',
                  'no_of_rooms',
                  'no_of_bathrooms',
                  'distance_to_school',
                  'house_age',
                  'distance_to_supermarket_km',
                  'crime_rate_index',
                  'property_value']].describe().T

# Variáveis categóricas
print(casas['large_living_room'].value_counts())
print(casas['parking_space'].value_counts())
print(casas['front_garden'].value_counts())
print(casas['swimming_pool'].value_counts())
print(casas['wall_fence'].value_counts())
print(casas['water_front'].value_counts())
print(casas['room_size_class'].value_counts())

#%% Criação das variáveis binárias

casas_dummy = pd.get_dummies(data=casas, 
                             columns=['large_living_room',
                                      'parking_space',
                                      'front_garden',
                                      'swimming_pool',
                                      'wall_fence',
                                      'water_front',
                                      'room_size_class'], 
                             drop_first=True,
                             dtype='float')

#%% Criando o texto da fórmula

def texto_formula(df, var_dependente, excluir_cols):
    variaveis = list(df.columns.values)
    variaveis.remove(var_dependente)
    for col in excluir_cols:
        variaveis.remove(col)
    return var_dependente + ' ~ ' + ' + '.join(variaveis)

texto_regressao = texto_formula(casas_dummy, 'property_value', '')

#%% Regressão Linear Múltipla

# Estimação do modelo
reg_casas = sm.OLS.from_formula(formula = texto_regressao,
                                data=casas_dummy).fit()

# Obtenção dos outputs
reg_casas.summary()

#%% Valores preditos pelo modelo para as observações da amostra

casas['fitted'] = reg_casas.fittedvalues

#%% Analisando os resíduos do modelo

# resíduos = valores observados - valores preditos
reg_casas.resid

#%% Alguns coeficientes podem apresentar uma interpretação "inesperada"

# Exemplos:
    ## quanto maior o tamanho da casa, menor o preço (ceteris paribus)
    ## quanto mais quartos, menor o preço (ceteris paribus)
    
# É importante notar que os resultados são interpretados de forma multivariada
    ## o resultado ocorre na presença das demais variáveis
    
#%% Matriz de correlações de Pearson entre variáveis métricas

df_quanti = casas[['land_size_sqm',
                   'house_size_sqm',
                   'no_of_rooms',
                   'no_of_bathrooms',
                   'distance_to_school',
                   'house_age',
                   'distance_to_supermarket_km',
                   'crime_rate_index',
                   'property_value']]

# Criando a matriz de correlações
correl = df_quanti.corr()

# Gerando o gráfico
sns.heatmap(correl, 
            annot=True, annot_kws={'size':8}, fmt=".2f", 
            cmap = plt.cm.viridis,
            square=True, linewidths=0.1)
plt.tick_params(labelsize=6)
plt.title('Correlações de Pearson', fontsize=10)
plt.show()

#%% Criando nova da fórmula

# 'land_size_sqm' tem correlação elevada com 'house_size_sqm' e 'no_of_rooms'
# Vamos remover o tamanho do terreno do modelo

novo_modelo = texto_formula(casas_dummy, 'property_value', ['land_size_sqm'])
## Nota: o 3º argumento contém as variáveis excluídas - entrar como lista

#%% Novo modelo

# Estimação do modelo
reg_casas_novo = sm.OLS.from_formula(formula = novo_modelo,
                                     data=casas_dummy).fit()

# Obtenção dos outputs
reg_casas_novo.summary()

#%% Coeficientes

# Note que o 'house_size_sqm' e 'no_of_rooms' agora têm impactos positivos

#%% Realizando predições para outras observações (modelo original)

# Qual é o preço médio estimado para uma casa com:
    # tamanho do terreno (m²) = 350
    # tamanho da casa (m²) = 200
    # quantidade de quartos = 3
    # quantidade de banheiros = 3
    # distância até a escola (km) = 4.5
    # idade da casa (anos) = 5
    # distância até o mercado (km) = 1.0
    # indicador de criminalidade da região = 1.20
    # sala ampla: sim
    # garagem: sim
    # jardim frontal: sim
    # piscina: sim
    # cercado: não
    # vista para lagos/rios: não
    # classificação dos quartos: classe 2

# Utilizando a função "predict"
obs_predict = pd.DataFrame({'land_size_sqm': [350],
                            'house_size_sqm': [200], 
                            'no_of_rooms': [3], 
                            'no_of_bathrooms': [3],
                            'distance_to_school': [4.5], 
                            'house_age': [5], 
                            'distance_to_supermarket_km': [1.0],
                            'crime_rate_index': [1.2], 
                            'large_living_room_Yes': [1],
                            'parking_space_Yes': [1], 
                            'front_garden_Yes': [1], 
                            'swimming_pool_Yes': [1],
                            'wall_fence_Yes': [0],
                            'water_front_Yes': [0], 
                            'room_size_class_Three': [0],
                            'room_size_class_Two': [1], 
                            'room_size_class_Zero': [0]})

print(f'preço estimado: {round(reg_casas.predict(obs_predict)[0],2)}')

#%% Comparando graficamente os ajustes dos modelos

sns.regplot(casas, x='property_value', y='fitted', marker='o', color='purple', scatter_kws={'s':0.50}, line_kws={'color':'red', 'lw':2})
plt.title('Análise Gráfica do Ajuste', fontsize=10)
plt.xlabel('Preço Observado', fontsize=10)
plt.ylabel('Preço Previsto pelo Modelo', fontsize=10)
plt.tick_params(labelsize=6)
plt.axline((0, 0), (max(casas['property_value']), max(casas['property_value'])), linewidth=1, color='grey')
plt.show()

#%% Fim!