import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# 1. Carregar dados fictícios de casos jurídicos em um DataFrame
data = {
    'Número do Caso': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115],
    'Cliente': ['Empresa A', 'Empresa B', 'Pessoa C', 'Empresa D', 'Pessoa E', 'Empresa F', 'Pessoa G', 'Empresa H', 'Empresa I', 'Pessoa J', 'Empresa K', 'Empresa L', 'Pessoa M', 'Empresa N', 'Pessoa O'],
    'Área do Direito': ['Trabalhista', 'Cível', 'Criminal', 'Cível', 'Trabalhista', 'Cível', 'Criminal', 'Trabalhista', 'Cível', 'Criminal', 'Cível', 'Trabalhista', 'Cível', 'Trabalhista', 'Criminal'],
    'Status': ['Em andamento', 'Finalizado', 'Em andamento', 'Finalizado', 'Finalizado', 'Em andamento', 'Finalizado', 'Em andamento', 'Finalizado', 'Finalizado', 'Finalizado', 'Em andamento', 'Finalizado', 'Finalizado', 'Em andamento'],
    'Valor da Causa': [50000, 120000, 30000, 150000, 80000, 45000, 60000, 75000, 90000, 110000, 130000, 55000, 60000, 95000, 30000],
    'Data de Abertura': ['2022-01-10', '2021-12-15', '2023-02-20', '2021-10-30', '2022-05-20', '2022-04-15', '2021-09-25', '2022-07-18', '2021-08-05', '2022-03-15', '2021-11-20', '2022-06-22', '2022-05-05', '2021-07-15', '2023-01-10'],
    'Data de Conclusão': ['2023-06-15', '2022-03-10', None, '2022-08-10', '2023-01-15', None, '2022-12-01', None, '2022-05-15', '2023-02-18', '2022-09-20', None, '2022-12-30', '2022-10-15', None]
}

df = pd.DataFrame(data)

# 2. Converter colunas de datas para formato datetime
df['Data de Abertura'] = pd.to_datetime(df['Data de Abertura'])
df['Data de Conclusão'] = pd.to_datetime(df['Data de Conclusão'])

# 3. Filtrar os casos em andamento
casos_em_andamento = df[df['Status'] == 'Em andamento']

# 4. Analisar a média do valor das causas finalizadas
media_valor_causas = df[df['Status'] == 'Finalizado']['Valor da Causa'].mean()

# 5. Gerar um resumo por área do direito
resumo_area_direito = df.groupby('Área do Direito')['Valor da Causa'].sum()

# 6. Gráfico 1: Valor total das causas por área do direito
plt.figure(figsize=(8, 6))
plt.bar(resumo_area_direito.index, resumo_area_direito.values, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
plt.title('Valor Total das Causas por Área do Direito')
plt.xlabel('Área do Direito')
plt.ylabel('Valor Total das Causas (R$)')
plt.tight_layout()
graph_image_1 = 'grafico_valor_causas_area.png'
plt.savefig(graph_image_1)
plt.close()

# 7. Gráfico 2: Distribuição de status dos casos
plt.figure(figsize=(8, 6))
status_counts = df['Status'].value_counts()
plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', colors=['#1f77b4', '#ff7f0e', '#2ca02c'])
plt.title('Distribuição de Status dos Casos')
plt.tight_layout()
graph_image_2 = 'grafico_status_casos.png'
plt.savefig(graph_image_2)
plt.close()

# 8. Gráfico 3: Média do valor das causas por área do direito
media_valor_area = df.groupby('Área do Direito')['Valor da Causa'].mean()
plt.figure(figsize=(8, 6))
plt.bar(media_valor_area.index, media_valor_area.values, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
plt.title('Média do Valor das Causas por Área do Direito')
plt.xlabel('Área do Direito')
plt.ylabel('Média do Valor das Causas (R$)')
plt.tight_layout()
graph_image_3 = 'grafico_media_valor_causas.png'
plt.savefig(graph_image_3)
plt.close()

# 9. Gerar um relatório em PDF usando a biblioteca FPDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 51, 102)  # Cor Azul para o cabeçalho
        self.cell(0, 10, 'Relatório de Análise de Casos Jurídicos', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(169, 169, 169)  # Cinza para o rodapé
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(0, 51, 102)  # Azul para títulos de capítulo
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.set_text_color(0)  # Preto para o corpo do texto
        self.multi_cell(0, 10, body)
        self.ln()

    def add_chapter(self, title, body):
        self.add_page()
        self.chapter_title(title)
        self.chapter_body(body)

# Inicializar PDF
pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)

# Adicionar página inicial e cabeçalho
pdf.add_page()

# Adicionar introdução
pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, 'Relatório de Análise de Casos Jurídicos', 0, 1, 'C')
pdf.ln(10)

pdf.set_font('Arial', '', 12)
pdf.set_text_color(0)  # Preto para corpo do texto
intro = ("Este relatório contém uma análise detalhada dos casos jurídicos, incluindo "
         "informações sobre os casos em andamento, média do valor das causas finalizadas, "
         "e um resumo por área do direito. Esses dados são essenciais para compreender "
         "as principais tendências do escritório e identificar áreas de foco estratégico.")
pdf.multi_cell(0, 10, intro)
pdf.ln(10)

# Adicionar seção "Casos em andamento"
casos_text = casos_em_andamento.to_string(index=False)
pdf.add_chapter('Casos em Andamento', casos_text)

# Adicionar seção "Média do valor das causas finalizadas"
media_text = f"A média do valor das causas finalizadas é: R${media_valor_causas:,.2f}"
pdf.add_chapter('Média do Valor das Causas Finalizadas', media_text)

# Adicionar seção "Resumo por área do direito"
resumo_text = resumo_area_direito.apply(lambda x: f'R${x:,.2f}').to_string()
pdf.add_chapter('Resumo por Área do Direito', resumo_text)

# Adicionar gráficos gerados
pdf.add_page()
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Gráfico: Valor Total das Causas por Área do Direito', 0, 1)
pdf.image(graph_image_1, x=15, y=30, w=180)
pdf.ln(60)

pdf.add_page()
pdf.cell(0, 10, 'Gráfico: Distribuição de Status dos Casos', 0, 1)
pdf.image(graph_image_2, x=15, y=30, w=180)
pdf.ln(60)

pdf.add_page()
pdf.cell(0, 10, 'Gráfico: Média do Valor das Causas por Área do Direito', 0, 1)
pdf.image(graph_image_3, x=15, y=30, w=180)

# Adicionar conclusão
pdf.add_page()
conclusion = ("Este relatório oferece uma visão abrangente sobre os processos jurídicos "
              "em andamento e finalizados. Ele pode ser utilizado para a tomada de decisões "
              "estratégicas no escritório, com base na performance de cada área de direito "
              "e no valor envolvido nas causas.")
pdf.add_chapter('Conclusão', conclusion)

# Salvar o PDF
pdf_file = 'relatorio_casos_juridicos.pdf'
pdf.output(pdf_file)

print(f"Relatório salvo como {pdf_file}")

