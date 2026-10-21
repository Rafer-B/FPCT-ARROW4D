from taskflow_database import testar_ligacao

try:
    resultado = testar_ligacao()

    if resultado == 1:
        print("Ligação ao PostgreSQL realizada com sucesso!")

except Exception as erro:
    print("Não foi possivel ligar à base de dados.")
    print("Tipo de erro: ", type(erro).__name__)
    print("Detalhes: ", erro)