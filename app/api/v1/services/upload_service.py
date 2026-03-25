# app/api/v1/services/upload_service.py
import pandas as pd
import numpy as np
from fastapi import UploadFile, HTTPException

def read_excel(file: UploadFile, taxa_comissao: float) -> dict:
    """Lê um arquivo Excel e retorna algumas informações"""
    if not file.filename.endswith((".xls", ".xlsx")):
        raise HTTPException(status_code=400, detail="Arquivo deve ser XLS ou XLSX")
    
    try:
        df = pd.read_excel(file.file)

        df['taxa_comissao'] = taxa_comissao
        df['comissao_calculada'] = df['taxa_comissao'] * df['Total']
        # Condições de pagamento atualizadas
        condicoes_pagamento = {
            "75": [75],
            "OPERAÇÃO BV 30/45/60 DIAS": [30, 45, 60],
            "14 A 49 CADA 7": [14, 21, 28, 35, 42, 49],
            "14 DDL": [14],
            "21,28,35,42,49,56,63,70 DOX PAY": [21, 28, 35, 42, 49, 56, 63, 70],
            "21/28/35 DDL": [21, 28, 35],
            "21/28/35 DOX PAY": [21, 28, 35],
            "21/28/35/42": [21, 28, 35, 42],
            "28 A 63 CADA 7": [28, 35, 42, 49, 56, 63],
            "28 DDL": [28],
            "28D DOX PAY": [28],
            "30/40/50/60 DDL": [30, 40, 50, 60],
            "30/45  DOX PAY": [30, 45],
            "30/45 DDL": [30, 45],
            "30/45/60 DDL": [30, 45, 60],
            "30/45/60 DOX PAY": [30, 45, 60],
            "30/45/60/75 DDL": [30, 45, 60, 75],
            "30/60/90": [30, 60, 90],
            "30/60/90 DOX PAY": [30, 60, 90],
            "30/60/90/120 DD": [30, 60, 90, 120],
            "30/60/90/120 DOX PAY": [30, 60, 90, 120],
            "3X CARTÃO DE CRÉDITO": [30, 60, 90],
            "45 DDL": [45],
            "45/55/65/75 DDL": [45, 55, 65, 75],
            "45/60/75 DDL": [45, 60, 75],
            "45/60/75/90/105 DDL": [45, 60, 75, 90, 105],
            "4X CARTÃO DE CRÉDITO": [30, 60, 90, 120],
            "60 DDL": [60],
            "6X CARTÃO DE CRÉDITO": [30, 60, 90, 120, 150, 180],
            "90 DD RISCO SACADO": [90],
            "90 DDL": [90],
            "A VISTA": [30],  # À vista = 1 parcela com 30 dias
            "OPERAÇÃO BV 30/60/90 DIAS": [30, 60, 90]
        }
        df['COND PGTO'] = df['COND PGTO'].str.strip().str.upper()
        df['prazo_pagamento'] = df['COND PGTO'].map(condicoes_pagamento)

        def get_numero_parcelas(prazo_pagamento_list):
            if isinstance(prazo_pagamento_list, list):
                return len(prazo_pagamento_list)
            return 'Não encontrado'

        df['numero_parcelas'] = df['prazo_pagamento'].apply(get_numero_parcelas)

        def calculate_comissao_parcela(comissao, parcelas):
            if parcelas == 'Não encontrado' or parcelas == 0:
                return 'Não encontrado'
            return comissao / parcelas

        df['comissao_parcela'] = df.apply(lambda row: calculate_comissao_parcela(row['comissao_calculada'], row['numero_parcelas']), axis=1)
        # First, ensure the column is string type and strip any whitespace
        df['EMISSAO NF'] = df['EMISSAO NF'].astype(str).str.strip()

        # Then, convert to datetime, explicitly specifying the format and coercing errors
        df['EMISSAO NF'] = pd.to_datetime(df['EMISSAO NF'], format='%d/%m/%Y', errors='coerce')

        # Check if there are any remaining NaT values after conversion attempt
        remaining_nat_count = df['EMISSAO NF'].isna().sum()

        if remaining_nat_count > 0:
            print(f"Aviso: Ainda existem {remaining_nat_count} valores 'NaT' na coluna 'EMISSAO NF' após a tentativa de conversão. Estes valores podem indicar formatos de data inválidos. Preenchendo 'NaT' com 1900-01-01.")
            # Fill NaT values with a default date to ensure no NaT remains
            df['EMISSAO NF'] = df['EMISSAO NF'].fillna(pd.Timestamp('1900-01-01'))
        else:
            print("Todos os valores da coluna 'EMISSAO NF' foram convertidos para o formato de data com sucesso.")

        # Convert 'numero_parcelas' to numeric, handling 'Não encontrado'
        comissao_parcela_numeric = pd.to_numeric(df['numero_parcelas'], errors='coerce')

        max_parcelas = comissao_parcela_numeric.max()

        # Ensure max_parcelas is an integer for iteration
        max_parcelas_int = int(max_parcelas)

        def calculate_parcela_details(row, max_parc):
            prazo_pagamento_list = row['prazo_pagamento']
            emissao_nf = row['EMISSAO NF']
            comissao_parcela = row['comissao_parcela']

            result = {}
            for i in range(max_parc):
                valor_col_name = f'valor_parcela_{i+1}'
                mes_col_name = f'mes_parcela_{i+1}'

                # Initialize with NaN, which will be overwritten if valid
                result[valor_col_name] = np.nan
                result[mes_col_name] = np.nan

                if isinstance(prazo_pagamento_list, list) and i < len(prazo_pagamento_list):
                    days = prazo_pagamento_list[i]

                    # Calculate due date, handling NaT from 'EMISSAO NF'
                    if pd.notna(emissao_nf):
                        data_vencimento = emissao_nf + pd.to_timedelta(days, unit='D')
                        if pd.notna(data_vencimento):
                            result[mes_col_name] = data_vencimento.month

                    # Assign comissao_parcela, handling 'Não encontrado'
                    if comissao_parcela != 'Não encontrado':
                        result[valor_col_name] = comissao_parcela

            return pd.Series(result)

        # Apply the function to each row to generate new columns
        new_cols_df = df.apply(calculate_parcela_details, axis=1, max_parc=max_parcelas_int)

        # Concatenate the new columns with the original DataFrame
        df = pd.concat([df, new_cols_df], axis=1)
        




        temp_dfs = []

        for i in range(1, max_parcelas_int + 1):
            valor_col_name = f'valor_parcela_{i}'
            mes_col_name = f'mes_parcela_{i}'

            # Check if columns exist before trying to select them
            if valor_col_name in df.columns and mes_col_name in df.columns:
                temp_df = df[[valor_col_name, mes_col_name]].copy()
                temp_df.rename(columns={valor_col_name: 'valor_total_parcelas', mes_col_name: 'mês'}, inplace=True)
                temp_dfs.append(temp_df)

        # Concatenate all temporary DataFrames
        df_consolidado = pd.concat(temp_dfs, ignore_index=True)

        # Remove rows with NaN in 'mês' or 'valor_total_parcelas'
        df_consolidado.dropna(subset=['mês', 'valor_total_parcelas'], inplace=True)

        # Convert 'mês' to integer type
        df_consolidado['mês'] = df_consolidado['mês'].astype(int)

        # Group by 'mês' and sum 'valor_total_parcelas'
        analise_por_mes = df_consolidado.groupby('mês')['valor_total_parcelas'].sum().reset_index()

        # Order by 'mês'
        analise_por_mes = analise_por_mes.sort_values(by='mês')

        print("Análise consolidada do valor total das parcelas por mês:")
        print(analise_por_mes)

        df.head()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ler o arquivo: {e}")
    
    return {
        "filename": file.filename,
        "rows": df.shape[0],
        "columns": df.shape[1],
        "preview": df.head(5).to_dict(orient="records")
    }

