# BikeCast — pacote de aplicação 9.5–9.10

Extraia o conteúdo deste ZIP na raiz DataPulse (onde estão app.py, preprocessamento.py, data/, models/ e reports/). Aceite substituir app.py, dashboard/ e .streamlit/. Não apague os arquivos existentes de ML. Não substituímos README.md nem requirements.txt.

## Windows PowerShell (venv ativa)

```powershell
python -m pip install -r requirements.txt -r requirements-app.txt
python -m pip check
python -m unittest discover -s tests -v
python -m streamlit run app.py
```

Teste as quatro páginas, alterne PT/EN em cada uma, teste filtros vazios, simule uma data histórica e confira o gráfico de 24 horas. A simulação usa condições normalizadas e não representa previsão atual. Alterar o idioma ou os parâmetros pode limpar o resultado do formulário; submeta novamente. Alguns rótulos técnicos nativos do Plotly/Streamlit podem permanecer em inglês.

## Deploy (9.10)

Após os testes locais, atualize requirements.txt com `python -m pip freeze | Set-Content -Encoding utf8 requirements.txt`. Confira `git status`, faça commit dos arquivos da aplicação, dependências e testes, e push para main. Não envie .venv, caches ou credenciais. Confirme que data/hour.csv, reports/, preprocessamento.py e models/bikecast_model.joblib estão no repositório. Carregue apenas o modelo confiável do próprio projeto.

No Streamlit Community Cloud, conecte o GitHub, selecione jtozzatti/BikeCast, branch main e app.py. Escolha Python 3.14 se disponível. Se a plataforma não suportar essa versão ou as dependências fixadas, não altere scikit-learn às cegas: use hospedagem compatível ou recrie e valide o modelo em ambiente suportado. A disponibilidade dessas versões na hospedagem não foi verificada. Após publicar, repita os testes manuais pelo link público. A etapa 9.10 só estará concluída após deploy funcional.

## Escopo e validação

Código compilado estaticamente e SVG validado como XML. O dataset, modelo e relatórios reais não estavam disponíveis no ambiente de geração; os testes de integração e a execução visual devem ocorrer no computador do projeto. A etapa 9.11 (README final e portfólio) permanece aberta.
