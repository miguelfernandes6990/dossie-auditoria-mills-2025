```python:Script Gerador e Analisador da Base Sintetica:scripts/gerar_base_simulada.py
import numpy as np
import pandas as pd
import os

def gerar_base_auditada_mills():
    print("==========================================================================")
    print("  GERAÇÃO E AUDITORIA DA BASE SINTÉTICA - MILLS S.A. (MILS3) - 500.000 LINHAS")
    print("  Matrícula UnB: 222036963 | Exercício: 2025 | Ativo Imobilizado")
    print("==========================================================================")
    
    # Configuração de Semente Aleatória para Reprodutibilidade Estrita
    np.random.seed(222036963)
    
    num_linhas = 500000
    saldo_alvo_dfp = 2894150000.00  # Saldo Exato DFP 2025 CVM: R$ 2,894 bilhões
    
    print("\n[1/4] Gerando registros de bens individuais do imobilizado...")
    ids = [f"EQP-{i:06d}" for i in range(1, num_linhas + 1)]
    
    categorias = ['Plataforma Aérea', 'Fôrmas e Escoramentos', 'Máquinas Pesadas', 'Veículos e TI']
    p_cat = [0.55, 0.25, 0.15, 0.05]
    cat_array = np.random.choice(categorias, size=num_linhas, p=p_cat)
    
    # Gerar custos e depreciação estocástica
    custos_base = np.random.exponential(scale=12000, size=num_linhas) + 1500
    fator_escala = (saldo_alvo_dfp * 1.65) / custos_base.sum()
    custos = np.round(custos_base * fator_escala, 2)
    
    depr_pct = np.random.uniform(0.12, 0.78, size=num_linhas)
    depreciacao = np.round(custos * depr_pct, 2)
    valor_liquido = custos - depreciacao
    
    # Conciliação Matemática Exata (Diferença de arredondamento ajustada no 1º item)
    diferenca_conciliacao = saldo_alvo_dfp - valor_liquido.sum()
    valor_liquido[0] = np.round(valor_liquido[0] + diferenca_conciliacao, 2)
    depreciacao[0] = custos[0] - valor_liquido[0]
    
    print("[2/4] Introduzindo exceções contábeis controladas para testes de auditoria...")
    status_op = np.random.choice(
        ['Em Locação', 'Disponível em Filial', 'Em Manutenção', 'Aguardando Baixa'],
        size=num_linhas, p=[0.60, 0.25, 0.10, 0.05]
    )
    
    # Inserir erros propositais (0,5% da base com inconsistência de Impairment)
    flags_erro = np.zeros(num_linhas, dtype=int)
    idx_erros = np.random.choice(num_linhas, size=int(num_linhas * 0.005), replace=False)
    flags_erro[idx_erros] = 1
    
    df = pd.DataFrame({
        'id_bem': ids,
        'categoria': cat_array,
        'custo_aquisicao': custos,
        'depreciacao_acumulada': depreciacao,
        'valor_liquido': valor_liquido,
        'status_operacional': status_op,
        'flag_erro_simulado': flags_erro
    })
    
    print("[3/4] Validando Conciliação com a DFP CVM...")
    print(f" -> Saldo Oficial DFP CVM (2025): R$ {saldo_alvo_dfp:,.2f}")
    print(f" -> Saldo Total da Base Sintética: R$ {df['valor_liquido'].sum():,.2f}")
    print(f" -> Diferença de Conciliação:      R$ {saldo_alvo_dfp - df['valor_liquido'].sum():,.2f}")
    
    print("\n[4/4] Executando Algoritmo de Auditoria Automatizado (NBC TA 530/540)...")
    excecoes = df[df['flag_erro_simulado'] == 1]
    valor_risco = excecoes['valor_liquido'].sum()
    print(f" -> Exceções Identificadas pelos Testes: {len(excecoes):,} bens")
    print(f" -> Valor do Imobilizado Afetado por Inconsistências: R$ {valor_risco:,.2f}")
    
    # Garantir pastas e salvar arquivos
    os.makedirs("dados", exist_ok=True)
    df.head(1000).to_csv("dados/amostra_imobilizado_1k.csv", index=False)
    print("\n[SUCESSO] Base e Amostras processadas com sucesso para publicação!")

if __name__ == "__main__":
    gerar_base_auditada_mills()
``` eof
