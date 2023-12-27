import sys
import psycopg2
from prettytable import PrettyTable

import matplotlib.pyplot as plt
import numpy as np

## Realização das consultas do Dashboard

host="localhost"
database="amazon_agk"
user="postgres"
password="postgres"
inputFile = "../postgres-data/amazon-meta.txt"

def conectDB():
    try:
        print("Conectando ao PostgreSQL...")
        conn = psycopg2.connect(
            "host=" + host +
            " dbname=" + database +
            " user=" + user +
            " password=" + password
        )

        cur = conn.cursor()

        # Adicione as instruções SQL para criar tabelas aqui
        # Exemplo:
        # cur.execute("CREATE TABLE IF NOT EXISTS ProductsReviews (...);")

        conn.commit()

        return conn, cur  # Retornar a conexão e o cursor

    except (Exception, psycopg2.DatabaseError) as error:
        print("Erro ao tentar conectar e criar tabelas", error)
        sys.exit()


def queryA(cur, asin):
    try:
        cur.execute(f'''
                    (SELECT * 
                    FROM ProductsReviews
                    WHERE asin = '{asin}'
                    ORDER BY  helpful DESC, rating DESC
                    LIMIT 5) UNION (SELECT * 
                    FROM ProductsReviews 
                    WHERE asin = '{asin}'
                    ORDER BY  rating ASC, helpful DESC
                    LIMIT 5); ''')
         
        results = cur.fetchall()
        table = PrettyTable()
        table.field_names = ["asin", "customer", "date", "rating", "votes", "helpful"]

        for row in results:
            table.add_row(row)

        print("Os 5 comentários mais úteis e com maior avaliação\n")
        print(table)
        print('\n\n')
        
        
    except (Exception, psycopg2.DatabaseError) as error:
        print ("Erro ao tentar realizar a consulta A", error)
   

def queryB(cur, asin):
    similar=[]
    try:
        cur.execute('''
                    SELECT *
                    FROM 
                    (
                    SELECT *
                    FROM Products
                    JOIN (
                        SELECT asin_similar AS ASIN
                        FROM ProductsSimilar
                        WHERE asin_initial = %s
                    ) AS Similares
                    ON Products.ASIN = Similares.ASIN
                    ) AS P
                    WHERE P.salesrank<(
                        SELECT salesrank
                        FROM Products
                        WHERE ASIN = %s
                    ); 
                    ''', (asin, asin,))
        similar=cur.fetchall()
        if(len(similar)==0):
            print("\nNenhum produto similar mais vendido ou não se sabe a posição de vendas do produto\n")
            return
        print("\nProdutos similares mais vendidos:")
        for i in similar:
            print(i)
        print()
    except (Exception, psycopg2.DatabaseError) as error:
        print ("Erro ao tentar realizar a consulta B", error)

def queryC(cur, asin):
    dates = []
    avegareScores = []
    count=1
    sum=0
    try:
        cur.execute('''SELECT * FROM ProductsReviews WHERE ASIN = %s;''', (asin,))
        queries = cur.fetchall()
        if(len(queries)<1):
            print("\nProduto com nehuma avaliação\n")
            return
        '''
        for line in queries:
            dates = np.append(dates, line[2])
            sum+=line[3]
            avegareScores= np.append(avegareScores, sum/count)
            count+=1
        
        plt.plot(dates, avegareScores)
        plt.xlabel("Datas")
        plt.ylabel("Média de Avaliação")
        plt.ylim(1, 5.5)
        plt.title("Média de Avaliação do Produto")
        plt.show()
        '''    
        print("Evolução da média de avaliação:")
        for line in queries: 
            print(line[2], end=' | ')
            sum+=line[3]
            print(round(sum/count,2))
            count+=1
    except (Exception, psycopg2.DatabaseError) as error:
        print ("Erro ao tentar realizar a consulta C", error)


# Listar os 10 produtos líderes de venda em cada grupo de produtos
def queryD(cur):
    try:
        # cur.execute('''
        #         SELECT ASIN, title, group_name, salesrank FROM((SELECT * FROM products WHERE group_name='Book' ORDER BY salesrank limit 10) UNION 
        #         (SELECT * FROM products WHERE group_name='Music' ORDER BY salesrank limit 10)UNION 
        #         (SELECT * FROM products WHERE group_name='DVD' ORDER BY salesrank limit 10) UNION 
        #         (SELECT * FROM products WHERE group_name='Video' ORDER BY salesrank limit 10)UNION 
        #         (SELECT * FROM products WHERE group_name='Toy' ORDER BY salesrank limit 10) UNION 
        #         (SELECT * FROM products WHERE group_name='VideoGames' ORDER BY salesrank limit 10)UNION 
        #         (SELECT * FROM products WHERE group_name='Software' ORDER BY salesrank limit 10) UNION 
        #         (SELECT * FROM products WHERE group_name='BabyProduct' ORDER BY salesrank limit 10)UNION 
        #         (SELECT * FROM products WHERE group_name='CE' ORDER BY salesrank limit 10) UNION 
        #         (SELECT * FROM products WHERE group_name='Sports' ORDER BY salesrank limit 10)) AS Subquery ORDER BY group_name;''')
        cur.execute('''
                SELECT ASIN, title, group_name, salesrank
                FROM (
                    SELECT *, 
                    ROW_NUMBER() OVER (PARTITION BY group_name ORDER BY salesrank) as row_num
                    FROM products
                    WHERE group_name IN (
                        SELECT DISTINCT group_name
                        FROM Products
                    )
                ) AS Subquery
                WHERE row_num <= 10
                ORDER BY group_name, salesrank;
        ''')
        

        results = cur.fetchall()
        table = PrettyTable()
        table.field_names=['ASIN', 'title', 'group_name', 'salesrank']
        for row in results:
            table.add_row(row)

        print("Os 10 produtos líderes de venda em cada grupo de produtos: \n")
        print(table)
        print('\n\n')

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error ao tentar realizar a consulta D", error)

def queryE(cur):
    try:
        cur.execute('''
                    SELECT ASIN, avg(rating) as average_rating
                    FROM ProductsReviews WHERE helpful >= (votes/2) AND rating >=3
                    GROUP BY ASIN
                    ORDER BY average_rating DESC LIMIT 10;
                ''')
        results = cur.fetchall()
        table = PrettyTable()
        table.field_names=['ASIN', 'average_rating']
        for row in results:
            table.add_row(row)

        print("Listar os 10 produtos com a maior média de avaliações úteis positivas por produto\n")
        print(table)
        print('\n\n')

    except (Exception, psycopg2.DatabaseError) as error:
        print("Erro ao tentar realizar a consulta E", error)
    
    

def queryF():
    print("Você escolheu a consulta F!!!")

# Listar os 10 clientes que mais fizeram comentários por grupo de produto
def queryG(cur):
    try:
        print("Carregando...")
        cur.execute('''
                SELECT customer, group_name, cont
                FROM (
                SELECT customer, group_name, COUNT(*) AS cont, 
                    ROW_NUMBER() OVER (PARTITION BY group_name ORDER BY COUNT(*) DESC) as rnk
                    FROM productsreviews
                    JOIN products ON productsreviews.asin = products.asin
                    GROUP BY customer, group_name
                ) AS ranked
                WHERE rnk <= 10;
        ''')
        results = cur.fetchall()
        table = PrettyTable()
        table.field_names=['customer', 'group_name', 'cont']
        for row in results:
            table.add_row(row)

        print("Listar os 10 clientes que mais fizeram comentários por grupo de produto\n")
        print(table)
        print('\n\n')
    except (Exception, psycopg2.DatabaseError) as error:
        print("Erro ao tentar realizar a consulta E", error)
    


def showMenu():
    print("\nEscolha uma opção de Consulta\t")
    
    print("a. Dado um produto, listar os 5 comentários mais úteis e com maior avaliação e os 5 comentários mais úteis e com menor avaliação")

    print("b. Dado um produto, listar os produtos similares com maiores vendas do que ele")

    print("c. Dado um produto, mostrar a evolução diária das médias de avaliação ao longo do intervalo de tempo coberto no arquivo de entrada")

    print("d. Listar os 10 produtos líderes de venda em cada grupo de produtos")

    print("e. Listar os 10 produtos com a maior média de avaliações úteis positivas por produto")

    print("f. Listar a 5 categorias de produto com a maior média de avaliações úteis positivas por produto")

    print("g. Listar os 10 clientes que mais fizeram comentários por grupo de produto")

    print("q. Sair")

def chooseQuery():
    try:
        print("Conectando com o PostgreSql...")
        conn = psycopg2.connect(
            "host="+host+
            " dbname=" + database +
            " user=" + user + 
            " password=" + password
        )
        cur = conn.cursor()
    except (Exception, psycopg2.DatabaseError) as error:
        print ("Erro ao conectar com o PostgreSQL", error)

    while(True):
        showMenu()
        option = input("Digite uma opcao de consulta: ")

        if (option == 'a'):
            asin = input("Digite o código ASIN do produto desejado: ")
            queryA(cur, asin)

        elif (option == 'b'):
            asin = input("Digite o código ASIN do produto desejado: ")
            queryB(cur, asin)

        elif (option == 'c'):
            asin = input("Digite o código ASIN do produto desejado: ")
            queryC(cur, asin)

        elif (option == 'd'):
            queryD(cur)

        elif (option == 'e'):
            queryE(cur)

        elif (option == 'f'):
            queryF()

        elif (option == 'g'):
            queryG(cur)

        elif (option == 'q'):
            sys.exit()
        else:
            print("Escolha  uma opção válida!!!")  
        
 

if __name__=='__main__':
    chooseQuery()

