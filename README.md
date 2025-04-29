# 🎼 Dashboard de Orquestras do Estado de São Paulo

Este projeto é um dashboard interativo feito com [Streamlit](https://streamlit.io/) para visualizar e explorar dados sobre orquestras nas cidades do Estado de São Paulo, com base na aba **"base SP"** de uma planilha Excel fornecida.

## 📊 Funcionalidades

- Indicadores gerais: número total de cidades, cidades com orquestra e percentual.
- Gráficos interativos com [Plotly](https://plotly.com/python/):
  - Quantidade de orquestras por estado.
  - Distribuição por modelo de gestão.
- Filtros por estado e modelo de gestão.
- Tabela com os dados filtrados.

## ▶️ Como executar

1. Clone este repositório:
```bash
git clone https://github.com/seu-usuario/dashboard_orquestras_sp.git
cd dashboard_orquestras_sp
````
2. Crie um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv .venv
source .venv/bin/activate  # ou .venv\\Scripts\\activate no Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute o Streamlit:
```bash
streamlit run app.py
```

## 📂 Estrutura

```
dashboard_orquestras_sp/
├── app.py               # Código principal do dashboard
├── requirements.txt     # Dependências do projeto
└── README.md            # Este arquivo
```

## 📎 Observações

- Certifique-se de que o arquivo Excel possui a aba `base SP`, iniciando os dados na linha 7 (linha 6 como cabeçalho).
- O projeto utiliza `openpyxl` para leitura de arquivos `.xlsx`.

---

Desenvolvido com ❤️ usando Streamlit e Python.
