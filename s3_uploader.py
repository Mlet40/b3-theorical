import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

class S3Uploader:
    def __init__(self, env_path='s3.env'):
        self.env_path = env_path
        self.aws_access_key_id = None
        self.aws_secret_access_key = None
        self.aws_default_region = None
        self.aws_session_token = None
        self.load_env_variables()

    def load_env_variables(self):
        # Carregar variáveis do arquivo .env
        load_dotenv(dotenv_path=self.env_path)

        # Atribuir variáveis de ambiente
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.aws_default_region = os.getenv('AWS_DEFAULT_REGION')
        self.aws_session_token = os.getenv('AWS_SESSION_TOKEN')

        # Verificar se as variáveis estão carregadas
        if not self.aws_access_key_id or not self.aws_secret_access_key or not self.aws_default_region:
            print("Por favor, configure as variáveis de ambiente corretamente.")
            return False
        return True

    def upload_to_s3(self, file_name, bucket, object_name=None):
        """
        Carrega um arquivo para um bucket S3.

        :param file_name: Caminho do arquivo a ser carregado
        :param bucket: Nome do bucket S3
        :param object_name: Nome do objeto no S3. Se não for especificado, o nome do arquivo será usado
        :return: True se o arquivo foi carregado com sucesso, caso contrário False
        """
        # Se o nome do objeto não for especificado, usa o nome do arquivo
        if object_name is None:
            object_name = file_name

        # Cria uma sessão S3
        s3_client = boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            aws_session_token=self.aws_session_token,
            region_name=self.aws_default_region
        )

        try:
            # Carrega o arquivo
            s3_client.upload_file(file_name, bucket, object_name)
            print(f"Arquivo {file_name} carregado com sucesso para {bucket}/{object_name}")
            return True
        except FileNotFoundError:
            print(f"O arquivo {file_name} não foi encontrado")
            return False
        except NoCredentialsError:
            print("Credenciais não encontradas")
            return False
        except PartialCredentialsError:
            print("Credenciais incompletas")
            return False
        except Exception as e:
            print(f"Erro ao carregar o arquivo: {e}")
            return False


def main():
    uploader = S3Uploader()
    if not uploader.load_env_variables():
        return

    # Exemplo de uso do upload_to_s3
    file_name = "C:/Users/binho/Documents/develop/b3/teste/teste.txt"
    bucket_name = "mlet40-datalake"
    object_name = "Gold/testeg.txt"  # Opcional, pode ser None
    uploader.upload_to_s3(file_name, bucket_name, object_name)


if __name__ == "__main__":
    main()
