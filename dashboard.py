import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("C:/Users/kevin/Downloads/world_cup_results.csv")

df['TotalGols'] = df['HomeGoals'] + df['AwayGoals']

st.title("🏆 Dashboard da Copa do Mundo")

anos = df['Year'].sort_values().unique()
ano_escolhido = st.selectbox("Selecione o ano da Copa", anos)

df_ano = df[df['Year'] == ano_escolhido]

st.subheader(f"Jogos da Copa de {ano_escolhido}")
tabela_jogos = df_ano[['Date', 'Round', 'HomeTeam', 'HomeGoals', 'AwayGoals', 'AwayTeam', 'Stadium', 'City', 'Country']]
tabela_jogos.columns = ['Data', 'Fase', 'Seleção Mandante', 'Gols Mandante', 'Gols Visitante', 'Seleção Visitante', 'Estádio', 'Cidade', 'País']
st.dataframe(tabela_jogos)

gols_por_ano = df.groupby("Year")["TotalGols"].sum().reset_index()
fig1 = px.bar(gols_por_ano, x='Year', y='TotalGols', title='Total de Gols por Edição da Copa')
fig1.update_layout(xaxis_title='Ano', yaxis_title='Total de Gols')
st.plotly_chart(fig1)

jogos_por_pais = df['Country'].value_counts().reset_index()
jogos_por_pais.columns = ['País-sede', 'Quantidade de Jogos']
fig2 = px.bar(jogos_por_pais, x='País-sede', y='Quantidade de Jogos', title='Quantidade de Jogos por País-sede')
st.plotly_chart(fig2)

maiores_goleadas = df.sort_values(by='TotalGols', ascending=False).head(10)
tabela_goleadas = maiores_goleadas[['Year', 'HomeTeam', 'HomeGoals', 'AwayGoals', 'AwayTeam']]
tabela_goleadas.columns = ['Ano', 'Mandante', 'Gols Mandante', 'Gols Visitante', 'Visitante']
st.subheader("🔝 Maiores Goleadas da História da Copa")
st.dataframe(tabela_goleadas)

st.subheader("⚽ Comparativo entre Seleções")
selecoes = sorted(set(df['HomeTeam'].unique()) | set(df['AwayTeam'].unique()))
time1 = st.selectbox("Seleção 1", selecoes)
time2 = st.selectbox("Seleção 2", selecoes)

confrontos = df[
    ((df['HomeTeam'] == time1) & (df['AwayTeam'] == time2)) |
    ((df['HomeTeam'] == time2) & (df['AwayTeam'] == time1))
]

if not confrontos.empty:
    tabela_confrontos = confrontos[['Year', 'HomeTeam', 'HomeGoals', 'AwayGoals', 'AwayTeam']]
    tabela_confrontos.columns = ['Ano', 'Mandante', 'Gols Mandante', 'Gols Visitante', 'Visitante']
    st.write(f"Histórico de confrontos entre **{time1}** e **{time2}**:")
    st.dataframe(tabela_confrontos)
else:
    st.write(f"Essas seleções nunca se enfrentaram na Copa do Mundo.")

