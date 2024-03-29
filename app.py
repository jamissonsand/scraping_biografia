import streamlit as st
import requests
from googlesearch import search
from bs4 import BeautifulSoup

def obter_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            st.error(f"Erro ao obter HTML: Status Code {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Erro ao obter HTML: {e}")
        return None

def extrair_conteudo(html):
    soup = BeautifulSoup(html, 'html.parser')
    biography_span = soup.find('span', {'class': 'mw-headline', 'id': 'Biography'})
    if biography_span:
        biography_content = []
        next_element = biography_span.find_next()
        while next_element and next_element.name != 'h2':
            if next_element.name == 'p':
                biography_content.append(next_element.get_text())
            next_element = next_element.find_next()
        return '\n'.join(biography_content).strip()
    else:
        st.warning("Biografia não encontrada.")
        return None

def main():
    st.title("Obter Biografia Política")

    # Entrada de texto para o nome político
    nome_politico = st.text_input('Digite o nome político')

    if nome_politico:
        # Termo de pesquisa
        query = "ballotpedia " + nome_politico

        try:
            # Faz a pesquisa no Google e obtém o primeiro resultado
            search_results = next(search(query, num_results=1), None)

            if search_results:
                st.write(f"URL: {search_results}")
                url = search_results
                # Chama a função para obter o HTML da página
                html = obter_html(url)

                # Extrai o conteúdo da biografia se o HTML for obtido com sucesso
                if html:
                    conteudo_biografia = extrair_conteudo(html)
                    if conteudo_biografia:
                        st.write(conteudo_biografia)
            else:
                st.warning("Nenhum resultado encontrado.")

        except Exception as e:
            st.error(f"Ocorreu um erro ao realizar a pesquisa: {e}")

if __name__ == "__main__":
    main()
