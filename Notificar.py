import os
import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CANAL_NOTIFICACOES = int(os.getenv('CANAL_NOTIFICACOES'))

# Configuração do bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

# Database simples para lembretes
lembretes = []

# Datas comemorativas (atualize conforme necessário)

datas_comemorativas = [

    # Janeiro
    {"nome": "Dia do Marketing", "data": "2025-01-14", "tags": ["marketing"], "prioridade": "Média"},
    {"nome": "Dia do Instagram", "data": "2025-01-20", "tags": ["Social media"], "prioridade": "Alta"},
    
    # Fevereiro
    {"nome": "Dia da Internet Segura", "data": "2025-02-06", "tags": ["tecnologia"], "prioridade": "Média"},
    {"nome": "Carnaval", "data": "2025-02-12", "tags": ["festa", "brasil"], "prioridade": "Altíssima"},
    {"nome": "Dia dos Namorados (BR)", "data": "2025-02-14", "tags": ["Comercial", "Social"], "prioridade": "Altíssima"},
    
    # Março
    {"nome": "Dia Internacional da Mulher", "data": "2025-03-08", "tags": ["Social", "empoderamento"], "prioridade": "Altíssima"},
    {"nome": "Dia do Consumidor", "data": "2025-03-15", "tags": ["Comercial"], "prioridade": "Alta"},
    {"nome": "Dia do Marketing Digital", "data": "2025-03-21", "tags": ["marketing"], "prioridade": "Alta"},
    
    # Abril
    {"nome": "Dia da Mentira", "data": "2025-04-01", "tags": ["Engajamento"], "prioridade": "Média"},
    {"nome": "Dia do Jornalista", "data": "2025-04-07", "tags": ["comunicação"], "prioridade": "Média"},
    {"nome": "Páscoa", "data": "2025-04-21", "tags": ["religioso", "Comercial"], "prioridade": "Alta"},
    
    # Maio
    {"nome": "Dia do Trabalho", "data": "2025-05-01", "tags": ["Social"], "prioridade": "Alta"},
    {"nome": "Dia das Mães", "data": "2025-05-12", "tags": ["Comercial", "Social"], "prioridade": "Altíssima"},
    {"nome": "Dia do Marketing de Conteúdo", "data": "2025-05-27", "tags": ["marketing"], "prioridade": "Alta"},
    
    # Junho
    {"nome": "Dia dos Namorados (Internacional)", "data": "2025-06-12", "tags": ["Comercial", "Social"], "prioridade": "Altíssima"},
    {"nome": "Dia do Influenciador Digital", "data": "2025-06-30", "tags": ["Social media"], "prioridade": "Alta"},
    
    # Julho
    {"nome": "Dia do Emoji", "data": "2025-07-17", "tags": ["Engajamento"], "prioridade": "Média"},
    
    # Agosto
    {"nome": "Dia dos Pais", "data": "2025-08-11", "tags": ["Comercial", "Social"], "prioridade": "Altíssima"},
    {"nome": "Dia do Estudante", "data": "2025-08-11", "tags": ["Social"], "prioridade": "Média"},
    {"nome": "Dia Internacional da Juventude", "data": "2025-08-12", "tags": ["Social"], "prioridade": "Média"},
    
    # Setembro
    {"nome": "Dia do Cliente", "data": "2025-09-15", "tags": ["Comercial"], "prioridade": "Alta"},
    {"nome": "Dia do Influenciador Cristão", "data": "2025-09-20", "tags": ["nicho"], "prioridade": "Média"},
    
    # Outubro
    {"nome": "Dia das Crianças (BR)", "data": "2025-10-12", "tags": ["Comercial"], "prioridade": "Alta"},
    {"nome": "Dia do Professor", "data": "2025-10-15", "tags": ["Social"], "prioridade": "Média"},
    {"nome": "Halloween", "data": "2025-10-31", "tags": ["Engajamento"], "prioridade": "Alta"},
    
    # Novembro
    {"nome": "Black Friday", "data": "2025-11-29", "tags": ["Comercial"], "prioridade": "Altíssima"},
    {"nome": "Cyber Monday", "data": "2025-12-02", "tags": ["Comercial"], "prioridade": "Alta"},
    
    # Dezembro
    {"nome": "Natal", "data": "2025-12-25", "tags": ["Comercial", "Social"], "prioridade": "Altíssima"},
    {"nome": "Ano Novo", "data": "2025-12-31", "tags": ["Social"], "prioridade": "Alta"},
]

# Ordenação corrigida - converte para datetime antes de ordenar
datas_comemorativas = sorted(
    datas_comemorativas,
    key=lambda x: datetime.strptime(x["data"], "%Y-%m-%d")
)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user} (ID: {bot.user.id})')
    verificar_datas.start()  # Inicia a verificação diária

@tasks.loop(hours=24)
async def verificar_datas():
    hoje = datetime.now().date()
    canal = bot.get_channel(CANAL_NOTIFICACOES)
    
    # Verifica datas comemorativas
    for evento in datas_comemorativas:
        data_evento = datetime.strptime(evento["data"], "%Y-%m-%d").date()
        
        if data_evento == hoje:
            embed = discord.Embed(
                title=f"🎉 HOJE É {evento['nome'].upper()}",
                description=f"Data: {data_evento.strftime('%d/%m/%Y')}\nPrioridade: {evento['prioridade']}",
                color=0x2ecc71
            )
            await canal.send(embed=embed)
        
        elif data_evento == hoje + timedelta(days=1):
            embed = discord.Embed(
                title=f"⏰ AMANHÃ É {evento['nome'].upper()}",
                description=f"Data: {data_evento.strftime('%d/%m/%Y')}\nPrepare os posts!",
                color=0xe67e22
            )
            await canal.send(embed=embed)
    
    # Verifica lembretes personalizados
    for lembrete in lembretes:
        if lembrete['data'] == hoje:
            await canal.send(
                f"🔔 LEMBRETE: {lembrete['mensagem']}\n"
                f"📅 Data: {lembrete['data'].strftime('%d/%m/%Y')}"
            )

@bot.command(name='proximadata')
async def proxima_data(ctx):
    hoje = datetime.now().date()
    proximo_evento = None
    
    for evento in sorted(datas_comemorativas, key=lambda x: x['data']):
        data_evento = datetime.strptime(evento["data"], "%Y-%m-%d").date()
        if data_evento >= hoje:
            proximo_evento = evento
            break
    
    if proximo_evento:
        dias_restantes = (datetime.strptime(proximo_evento["data"], "%Y-%m-%d").date() - hoje).days
        embed = discord.Embed(
            title="📅 Próxima Data Comemorativa",
            description=(
                f"**{proximo_evento['nome']}**\n"
                f"📅 Data: {proximo_evento['data']}\n"
                f"⏳ Faltam {dias_restantes} dias\n"
                f"🔝 Prioridade: {proximo_evento['prioridade']}"
            ),
            color=0x3498db
        )
    else:
        embed = discord.Embed(
            title="📅 Próximas Datas",
            description="Nenhuma data futura cadastrada",
            color=0x95a5a6
        )
    
    await ctx.send(embed=embed)

@bot.command(name='lembrete')
async def criar_lembrete(ctx, data: str, *, mensagem: str):
    try:
        data_obj = datetime.strptime(data, "%d/%m/%Y").date()
        lembretes.append({
            "data": data_obj,
            "mensagem": mensagem,
            "autor": ctx.author.id
        })
        
        embed = discord.Embed(
            title="✅ Lembrete Criado",
            description=(
                f"**Mensagem:** {mensagem}\n"
                f"**Data:** {data_obj.strftime('%d/%m/%Y')}\n"
                f"🔔 Será notificado no dia"
            ),
            color=0x00ff00
        )
        await ctx.send(embed=embed)
    
    except ValueError:
        await ctx.send("❌ Formato de data inválido! Use `/lembrete DD/MM/AAAA Mensagem`")

@bot.command(name='datas')
async def listar_datas(ctx):
    hoje = datetime.now().date()
    embed = discord.Embed(title="📅 Todas as Datas Comemorativas", color=0x9b59b6)
    
    for evento in sorted(datas_comemorativas, key=lambda x: x['data']):
        data_evento = datetime.strptime(evento["data"], "%Y-%m-%d").date()
        status = "✅ Passou" if data_evento < hoje else "🟢 Futura"
        embed.add_field(
            name=f"{evento['nome']}",
            value=(
                f"📅 {data_evento.strftime('%d/%m/%Y')}\n"
                f"Status: {status}\n"
                f"Prioridade: {evento['prioridade']}"
            ),
            inline=True
        )
    
    await ctx.send(embed=embed)

bot.run(TOKEN)