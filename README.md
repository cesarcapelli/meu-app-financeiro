#  My Grana - Controle Financeiro Pessoal

O **My Grana** é um dashboard interativo que estou desenvolvendo com ajuda de IA para desenvolver utilizando Python e streamlit, sem Ctrl c/ Ctrl v.
Ele permite o acompanhamento de gastos variáveis e fixos, oferecendo visualizações claras para auxiliar na tomada de decisão financeira.

##  Funcionalidades

- **Lançamento de Gastos:** Interface intuitiva para cadastrar despesas diárias.
- **Gestão de Gastos Fixos:** Seção dedicada para cadastrar contas recorrentes e lançá-las automaticamente no mês atual com um clique.
- **Dashboard Interativo:** Gráficos de "rosquinha" (donut) e barras utilizando **Plotly** para visualizar a distribuição de gastos por categoria e forma de pagamento.
- **Filtros Inteligentes:** Navegação por mês e ano para análise histórica.
- **Integração com Excel:** 
    - Download de modelo padrão para preenchimento offline.
    - Upload de gastos via arquivos `.xlsx`.
- **Edição em Tempo Real:** Tabelas editáveis que permitem ajustar ou excluir registros instantaneamente.

##  Tecnologias Utilizadas

- Python (Linguagem principal)
- Streamlit (Interface Web e Dashboard)
- Pandas (Manipulação e análise de dados)
- Plotly Express (Gráficos interativos)
- Openpyxl (Suporte para arquivos Excel)

##  Como Executar o Projeto

1. Certifique-se de ter o Python instalado.
2. Instale as dependências necessárias:
   ```bash
   pip install streamlit pandas plotly openpyxl
   ```
3. Execute o aplicativo:
   ```bash
   streamlit run app.py
   ```

## 📈 Próximos Passos (Roadmap)

- [ ] Implementação de lógica para compras parceladas no cartão.
- [ ] Persistência de dados em banco de dados ou integração com Google Sheets API.
- [ ] Sistema de autenticação de usuários.
