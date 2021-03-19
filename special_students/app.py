import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

from special_students.settings import settings

sns.set_theme(style="whitegrid")


approvals = pd.read_csv(settings.processed_approvals_path)


st.write("# Special students basic EDA")

# aprovacoes por disciplina
st.write("## Qual a quantidade de aprovações por disciplina?")
approvals_by_course = (
    approvals.groupby(["codigo_curso"])
    .agg({"nome_aluno": "count"})
    .reset_index()
    .rename(columns={"nome_aluno": "alunos"})
    .sort_values(by=["alunos"], ascending=False)
)

fig, ax = plt.subplots(figsize=(18, 12))
sns.barplot(x="alunos", y="codigo_curso", data=approvals_by_course, orient="h", ax=ax)
ax.set_title("Contagem de alunos aprovados por disciplina")
st.pyplot(fig=fig)

# aprovacoes por curso
st.write("## Qual a quantidade de aprovações por área de concentração?")
approvals_by_concentration_area = (
    approvals.groupby(["nome_area_concentracao"])
    .agg({"nome_aluno": "count"})
    .reset_index()
    .rename(columns={"nome_aluno": "alunos"})
    .sort_values(by=["alunos"], ascending=False)
)
fig, ax = plt.subplots(figsize=(18, 12))
sns.barplot(
    x="alunos",
    y="nome_area_concentracao",
    data=approvals_by_concentration_area,
    orient="h",
    ax=ax,
)

ax.set_title("Contagem de alunos aprovados por área de atuação")
st.pyplot(fig=fig)

# Como o número de aprovações se relaciona com as areas de concentração?
st.write("## Como o número de aprovações se relaciona com as áreas de concentração?")
area_concentracao_disciplinas_aprovadas = approvals[
    ["nome_aluno", "disciplinas_aprovadas", "nome_area_concentracao"]
].drop_duplicates()
fig, ax = plt.subplots(figsize=(9, 16))

sns.violinplot(
    y="nome_area_concentracao",
    x="disciplinas_aprovadas",
    data=area_concentracao_disciplinas_aprovadas,
    orient="h",
    showfliers=False,
    ax=ax,
)

ax.set_title(
    "Distribuição de quantidade de disciplinas aprovadas por área de concentração"
)
st.pyplot(fig=fig)

# Como o numero de aprovacoes se relaciona com as disciplinas?
st.write("## Como o numero de aprovacoes se relaciona com as disciplinas?")
curso_disciplinas_aprovadas = approvals[
    ["nome_aluno", "disciplinas_aprovadas", "codigo_curso"]
].drop_duplicates()
fig, ax = plt.subplots(figsize=(9, 25))

sns.violinplot(
    y="codigo_curso",
    x="disciplinas_aprovadas",
    data=curso_disciplinas_aprovadas,
    orient="h",
    showfliers=False,
    ax=ax,
)

ax.set_title("Distribuição de quantidade de disciplinas aprovadas por curso")
st.pyplot(fig=fig)
