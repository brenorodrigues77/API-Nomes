from pprint import pprint
import requests
import pandas as pd
import streamlit as st

#função de requisição aos dados da API do IBGE
def make_request(url, params=None):
  response = requests.get(url, params=params)
  try:
    response.raise_for_status()
  except requests.HTTPError as e:
    print(f'error in request: {e}')
    result = None
  else:
    result = response.json() 
  return(result)

#função de frequencia dos nomes
def get_name_in_decade(nome):
  url = f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}"

  date_decade = make_request(url=url)
  dict_decade = {}
  if not date_decade:
    return {}
  for date in date_decade[0]['res']:
    decade = date['periodo']
    quantity = date['frequencia']
    dict_decade[decade] = quantity
  return dict_decade

#front end da API do IBGE com Streamlit
def main():
  st.title('Name for Decade')
  st.write('date IBGE (Font: https://servicodados.ibge.gov.br/api/docs/nomes?versao=2)')
  
  name = st.text_input('Consult a Name:')
  if not name:
    st.stop()

  dict_decade = get_name_in_decade(name)
  if not dict_decade:
    st.warning(f'{name} search not found ')
    st.stop()
  
  df = pd.DataFrame.from_dict(dict_decade,orient='index')
  col1, col2 = st.columns([0.3, 0.7])
  with col1:
    st.write('Name by Decade')
    st.dataframe(df)
  with col2:
    st.write('Graphic Evolution')
    st.line_chart(df)

if __name__ == '__main__':
  main()