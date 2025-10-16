import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os
import smtplib
from email.message import EmailMessage
import schedule
import time

# Caminhos
DATA_PATH = "data/vendas.csv"
REPORTS_PATH = "reports"

# Configuração do e-mail
EMAIL_ORIGEM = "testespython4@gmail.com"
EMAIL_SENHA = "ravxfpoxetddxhgy"  # Lembrar de usar senha de app do Gmail
EMAIL_DESTINO = "viniciosevan@gmail.com"  # Destinatário padrão

def gerar_relatorio(destinatarios=None):
    """Gera relatórios Excel e PDF e envia por e-mail."""
    if destinatarios is None:
        destinatarios = [EMAIL_DESTINO]

    # 1️⃣ Ler os dados
    df = pd.read_csv(DATA_PATH)

    # 2️⃣ Calcular métricas
    faturamento_total = (df['Quantidade'] * df['Preco Unitario']).sum()
    produto_top = df.groupby('Produto')['Quantidade'].sum().idxmax()
    ticket_medio = faturamento_total / df['Produto'].nunique()

    resumo = {
        "Faturamento Total": [faturamento_total],
        "Produto Mais Vendido": [produto_top],
        "Ticket Médio": [ticket_medio]
    }

    resumo_df = pd.DataFrame(resumo)

    # 3️⃣ Gerar nomes dos arquivos
    data_hoje = datetime.now().strftime("%d%m%Y")
    nome_pdf = os.path.join(REPORTS_PATH, f"relatorio_{data_hoje}.pdf")
    nome_excel = os.path.join(REPORTS_PATH, f"relatorio_{data_hoje}.xlsx")

    # 4️⃣ Criar relatório Excel
    with pd.ExcelWriter(nome_excel, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Vendas')
        resumo_df.to_excel(writer, index=False, sheet_name='Resumo')

    print(f"📊 Relatório Excel gerado: {nome_excel}")

    # 5️⃣ Criar relatório PDF
    c = canvas.Canvas(nome_pdf, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, f"Relatório de Vendas - {datetime.now().strftime('%d/%m/%Y')}")
    c.setFont("Helvetica", 12)
    c.drawString(100, 770, f"Faturamento Total: R$ {faturamento_total:,.2f}")
    c.drawString(100, 750, f"Produto Mais Vendido: {produto_top}")
    c.drawString(100, 730, f"Ticket Médio: R$ {ticket_medio:,.2f}")
    c.save()

    print(f"📄 Relatório PDF gerado: {nome_pdf}")

    # 6️⃣ Enviar e-mail com os relatórios anexados
    enviar_email(nome_pdf, nome_excel, faturamento_total, destinatarios)

def enviar_email(arquivo_pdf, arquivo_excel, faturamento_total, destinatarios):
    """Envia e-mail com anexos PDF e Excel para uma lista de destinatários."""
    msg = EmailMessage()
    msg['Subject'] = f"Relatório Diário de Vendas - {datetime.now().strftime('%d/%m/%Y')}"
    msg['From'] = EMAIL_ORIGEM
    msg['To'] = ", ".join(destinatarios)

    corpo = f"""
Olá,

Segue em anexo o relatório diário de vendas.

Faturamento total do dia: R$ {faturamento_total:,.2f}

Atenciosamente,
Sistema Automático de Relatórios
"""
    msg.set_content(corpo)

    # Anexar PDF
    with open(arquivo_pdf, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename=os.path.basename(arquivo_pdf))

    # Anexar Excel
    with open(arquivo_excel, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='vnd.ms-excel', filename=os.path.basename(arquivo_excel))

    # Enviar e-mail
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ORIGEM, EMAIL_SENHA)
        smtp.send_message(msg)

    print(f"📨 E-mail enviado com sucesso para {', '.join(destinatarios)}")

# 7️⃣ Agendamento diário
def tarefa_diaria():
    print("⏰ Iniciando execução diária do relatório...")
    gerar_relatorio()  # Destinatários padrão
    print("⏰ Execução concluída!")

# Agendar para rodar todo dia às 18:00
schedule.every().day.at("18:00").do(tarefa_diaria)

print("📝 Sistema de relatórios iniciado. Aguarde o horário programado...")

while True:
    schedule.run_pending()
    time.sleep(60)  # Verifica a cada 60 segundos

# Executar manualmente na primeira vez (opcional)
# gerar_relatorio()