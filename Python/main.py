from fastapi import FastAPI, HTTPException
import pandas as pd
import requests
import matplotlib.pyplot as plt
import io
from fastapi.responses import StreamingResponse
import logging

# Configurar o backend do matplotlib para 'Agg'
import matplotlib
matplotlib.use('Agg')  

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)

@app.get("/taxaSelic")
def getTaxaSelic():
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4189/dados?formato=csv"
    response = requests.get(url)

    if response.status_code != 200:
        logging.error(f"Erro ao buscar dados do Banco Central. Status Code: {response.status_code}")
        raise HTTPException(status_code=response.status_code, detail="Erro ao buscar dados do Banco Central")

    try:
        csv_data = io.StringIO(response.text)
        df = pd.read_csv(csv_data, sep=";", header=0)
        df.columns = ['data', 'valor']

      
        logging.debug(f"Dados brutos:\n{df.head()}")

      
        df['valor'] = df['valor'].str.replace(',', '.').astype(float, errors='ignore')

    
        df = df.dropna()

        
        if df.empty:
            logging.error("Nenhum dado válido encontrado após a limpeza.")
            raise ValueError("Nenhum dado válido encontrado após a limpeza.")

    
        df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')

       
        logging.debug(f"Dados após a limpeza:\n{df.head()}")

        # Gerar gráfico
        plt.figure(figsize=(10, 6))
        plt.plot(df['data'], df['valor'], label='Taxa Selic', color='blue', marker='o', linestyle='-')
        plt.xlabel('Data')
        plt.ylabel('Taxa Selic (%)')
        plt.title('Taxa Selic ao Longo do Tempo')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Ajustar escala do eixo Y
        valor_max = df['valor'].max()
        valor_min = df['valor'].min()
        margem = (valor_max - valor_min) * 0.1
        plt.ylim(valor_min - margem, valor_max + margem)

        img_io = io.BytesIO()
        plt.savefig(img_io, format='png', dpi=300)  # Aumentar a resolução
        img_io.seek(0)

        
        plt.close()

        # Retornar o gráfico como imagem
        return StreamingResponse(img_io, media_type="image/png")
    except Exception as e:
        logging.error(f"Erro ao processar dados: {e}")
        raise HTTPException(status_code=500, detail=str(e))
