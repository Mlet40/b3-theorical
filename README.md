#versão do python 3.10

#inicie um ambiente virtual

#verifique se seu python é 3.10, senão instale essa versão e deixa como principal no path no ambiente do windows

#depois segue os seguintes passos

pip install python-dotenv

#cria uma pasta de ambiente b3_env - pode ser qualquer nome xpto_venv - depois starta o ambiente virtual b3_env\Scripts\activate

python -m venv b3_env

b3_env\Scripts\activate

#instalação de bibliotecas necessárias

pip install --upgrade pip

pip install -r requirements.txt

#configuração - alterar o arquivo s3.env, pegar o aws access key, secret,session token na aba iAWS Details de https://awsacademy.instructure.com/courses/84696/modules/items/7696432 

--s3.env--
AWS_ACCESS_KEY_ID=ALtera a key 

AWS_SECRET_ACCESS_KEY=altera o secret 

AWS_DEFAULT_REGION=us-east-1

AWS_SESSION_TOKEN=Altera o session token


#para execução

python b3_web_scrapping.py
