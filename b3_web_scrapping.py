from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
from datetime import datetime
from s3_uploader import S3Uploader

# Configurar as opções do Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')  # Opcional, para executar o navegador em modo headless
chrome_options.add_argument('--disable-web-security')
chrome_options.add_argument('--allow-running-insecure-content')
chrome_options.add_argument('--log-level=3')  # Desativa logs de nível INFO e abaixo
chrome_options.add_argument('--output=/dev/null')  # Redireciona a saída para /dev/null no Linux/Mac


# Configurar o webdriver
driver = webdriver.Chrome(options=chrome_options)

# Listas para armazenar os dados
header_data = []
rows_data = []



def get_teoric_date():
    try:
        date_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//form/h2"))
        )
        date_text = date_element.text
        print(f"data:{date_text}")
        # Extrair e converter a data
        date_str = date_text.split('-')[-1].strip()
        date_obj = datetime.strptime(date_str, "%d/%m/%y")
        formatted_date = date_obj.strftime("%Y-%m-%d")
        print("Data extraída e formatada:", formatted_date)
    except Exception as e:
        print(f"Erro ao extrair a data: {e}")
        driver.quit()
        exit()
    return formatted_date

def scrape_header():
    # Extraia os dados do cabeçalho da tabela
    header = driver.find_elements(By.XPATH, "//table/thead/tr/th")

    if not header_data:  # Apenas adicionar cabeçalho uma vez
        for th in header:
            if th.get_attribute("colspan") == "2":
                continue  # Ignorar a coluna
            header_data.append(th.text)
        header_data.append("data")
        print('--------------HEADER ---------------------')
        print(header_data)
def scrape_page():
    try:
        datatheo = get_teoric_date()
        # Aguarde até que os dados da tabela sejam carregados
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//table"))
        )

        # Extraia os dados do corpo da tabela
        rows = driver.find_elements(By.XPATH,
                                    "//table/tbody/tr")
        for row in rows:
            row_data = [cell.text.replace(".","").replace(",",".") for cell in row.find_elements(By.XPATH, "td")]
            row_data.append(datatheo)
            rows_data.append(row_data)
            print(row_data)
    except Exception as e:
        print(f"Erro ")

def scrape_page_next():
    # Loop para navegação através das páginas
    while True:
        try:
            # Localizar e clicar no botão de próxima página
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "li.pagination-next a"))
            )
            next_button.click()

            # Pausar para garantir que a página foi carregada
            time.sleep(1)

            # Raspar a próxima página
            scrape_page()
        except Exception as e:
            print(f"Fim da paginação")
            break

def select_sector_combobox():
    # Selecionar "Setor de Atuação" no dropdown
    try:
        select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "segment"))
        )
        select = Select(select_element)
        select.select_by_visible_text("Setor de Atuação")
        # Aguarde até que a página atualize com a seleção
        time.sleep(2)  # Ajuste o tempo conforme necessário
    except Exception as e:
        print(f"-")
        driver.quit()
        exit()

def create_data_parquet():
    # Criar um DataFrame do pandas com os dados raspados
    df = pd.DataFrame(rows_data, columns=header_data)
    filename = f'b3_theorical_{get_teoric_date()}.parquet'
    # Salvar o DataFrame em um arquivo .parquet
    df.to_parquet(filename, engine='pyarrow')
    print(f"Dados salvos em {filename}")
    return filename
def upload_to_s3(filename):
    uploader = S3Uploader()
    if not uploader.load_env_variables():
        return

    bucket_name = "mlet40-data"
    object_name = f"raw/{filename}"  # Opcional, pode ser None
    uploader.upload_to_s3(filename, bucket_name, object_name)

# Navegar até a página inicial
driver.get("https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br")

#webscraping

select_sector_combobox()
scrape_header()
scrape_page()
scrape_page_next()
filename = create_data_parquet()
upload_to_s3(filename)

# Fechar o navegador
driver.quit()






