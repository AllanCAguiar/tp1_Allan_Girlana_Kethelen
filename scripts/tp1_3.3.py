import sys
import psycopg2
from prettytable import PrettyTable

## Realização das consultas do Dashboard

host="localhost"
database="amazon_agk"
user="postgres"
password="postgres"
outputFile = "resultados.txt"

def writeFile(table,query):
    with open(outputFile, "a") as f:
        f.write(f"\n\nResultados da Consulta {query}\n\n")
        f.write(str(table))
        f.close()
    
def queryA(cur, asin):
    try:
        cur.execute(f'''(
                        SELECT * 
                        FROM ProductsReviews
                        WHERE asin = '{asin}'
                        ORDER BY  helpful DESC, rating DESC
                        LIMIT 5) 
                    UNION ALL
                        (
                        SELECT * 
                        FROM ProductsReviews 
                        WHERE asin = '{asin}'
                        ORDER BY  rating ASC, helpful DESC
                        LIMIT 5); 
                    ''')
        results = cur.fetchall()
        table = PrettyTable()
        table.field_names = ["id","asin", "customer", "date", "rating", "votes", "helpful"]
        if(len(results)==0):
            print("Nenhum comentário encontrado")
            return
        for row in results:
            table.add_row(row)

        writeFile(table, f'A para o código {asin}')

    except (Exception, psycopg2.DatabaseError) as error:
        print ("Erro ao tentar realizar a consulta A", error)
   

def queryB(cur, asin):
    try:
        cur.execute(f'''SELECT P.id_product, P.Original_asin, P.title, P.group_name, P.salesrank
                        FROM (
                        SELECT Original.id_product, Original.asin AS Original_asin, Original.title, Original.group_name, Original.salesrank
                        FROM Products Original
                        JOIN (
                            SELECT asin_similar AS ASIN
                            FROM ProductsSimilar
                            WHERE asin_initial = '{asin}'
                        ) AS Similares ON Original.ASIN = Similares.ASIN
                    ) AS P
                    WHERE P.salesrank < (
                        SELECT salesrank
                        FROM Products
                        WHERE ASIN = '{asin}'
                    );''')
        results = cur.fetchall()
        if len(results) == 0:
            print("\nNenhum produto similar mais vendido\n")
            return
            
        table = PrettyTable()
        table.field_names = ['ID_product', 'ASIN', 'title','group', 'salesrank']
        for row in results:
            table.add_row(row)

        writeFile(table, f'B para o código {asin}')


    except (Exception, psycopg2.DatabaseError) as error:
        print("Erro ao tentar realizar a consulta B", error)


def queryC(cur, asin):
    try:
        cur.execute(f'''SELECT DISTINCT date, ROUND(AVG(rating) OVER (PARTITION BY asin ORDER BY date),2) 
                        FROM ProductsReviews 
                        WHERE ASIN = '{asin}'
                        ORDER BY date;
                    ''')
        queries = cur.fetchall()
        if(len(queries)==1):
            print("\nProduto com menos de uma avaliação\n")
            return
        table = PrettyTable()
        table.field_names = ['Date', 'Average Rating']
        for line in queries: 
            table.add_row(line)
        writeFile(table, f'C para o código {asin}')
    except (Exception, psycopg2.DatabaseError) as error:
        print ("Erro ao tentar realizar a consulta C", error)


# Listar os 10 produtos líderes de venda em cada grupo de produtos
def queryD(cur):
    try:
        cur.execute('''
                    SELECT ASIN, title, group_name, salesrank
                    FROM (
                        SELECT *, 
                        ROW_NUMBER() OVER (PARTITION BY group_name ORDER BY salesrank) as row_num
                        FROM products
                        WHERE group_name IN ('Book', 'Music', 'DVD', 'Video', 'Toy', 'VideoGames', 'Software', 'BabyProduct', 'CE', 'Sports')
                    ) AS Subquery
                    WHERE row_num <= 10
                    ORDER BY group_name, salesrank;
                    ''')
        
        results = cur.fetchall()
        table = PrettyTable()
        table.field_names=['ASIN', 'title', 'group_name', 'salesrank']
        for row in results:
            table.add_row(row)

        writeFile(table, 'D')

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error ao tentar realizar a consulta D", error)


# Listar os 10 produtos com a maior média de avaliações úteis positivas por produto
def queryE(cur):
    try:
        cur.execute('''
                    SELECT ASIN, ROUND(avg(rating),2) as average_rating
                    FROM ProductsReviews WHERE helpful >= (votes/2) AND rating >=3
                    GROUP BY ASIN
                    ORDER BY average_rating DESC LIMIT 10;
                    ''')
        results = cur.fetchall()
        table = PrettyTable()
        table.field_names=['ASIN', 'average_rating']
        for row in results:
            table.add_row(row)

        writeFile(table, 'E')

    except (Exception, psycopg2.DatabaseError) as error:
        print("Erro ao tentar realizar a consulta E", error)
    
# Listar a 5 categorias de produto com a maior média de avaliações úteis positivas por produto
def queryF(cur):
    try:
        cur.execute('''
                    SELECT ProductsCategories.category_name, ROUND(AVG(ProductsReviews.rating),2) AS average_rating
                    FROM ProductsReviews
                    JOIN ProductsCategories ON ProductsReviews.ASIN = ProductsCategories.ASIN
                    WHERE ProductsReviews.helpful >= (ProductsReviews.votes / 2) AND ProductsReviews.rating >= 3
                    GROUP BY ProductsCategories.category_name
                    ORDER BY average_rating DESC
                    LIMIT 5;
                    ''')
        results = cur.fetchall()
        table = PrettyTable()
        table.field_names=['category_name', 'average_rating']
        for row in results:
            table.add_row(row)

        writeFile(table, 'F')

    except (Exception, psycopg2.DatabaseError) as error:
        print("Erro ao tentar realizar a consulta E", error)

# Listar os 10 clientes que mais fizeram comentários por grupo de produto
def queryG(cur):
    try:
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
        
        writeFile(table, 'G')

    except (Exception, psycopg2.DatabaseError) as error:
        print("Erro ao tentar realizar a consulta G", error)
    


def showMenu():
    print("----------------------------------------------------------------------------")
    print("\t\tEscolha uma opção de Consulta\t\t")
    print("----------------------------------------------------------------------------")
    
    print("a. Dado um produto, listar os 5 comentários mais úteis e com maior avaliação e os 5 comentários mais úteis e com menor avaliação\n")

    print("b. Dado um produto, listar os produtos similares com maiores vendas do que ele\n")

    print("c. Dado um produto, mostrar a evolução diária das médias de avaliação ao longo do intervalo de tempo coberto no arquivo de entrada\n")

    print("d. Listar os 10 produtos líderes de venda em cada grupo de produtos\n")

    print("e. Listar os 10 produtos com a maior média de avaliações úteis positivas por produto\n")

    print("f. Listar a 5 categorias de produto com a maior média de avaliações úteis positivas por produto\n")

    print("g. Listar os 10 clientes que mais fizeram comentários por grupo de produto\n")

    print("l. Limpar o arquivo de saída\n")

    print("q. Sair\n")

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
    print("Conexão com o PostgreSQL efetivada")
    print(f"Os resultados das consultas estarão no arquivo '{outputFile}' ")
    while(True):
        showMenu()
        option = input("DIGITE AQUI SUA OPCAO DE CONSULTA: ")

        if (option == 'a' or option == 'A'):
            asin = input("\nDigite o código ASIN do produto desejado: ")
            queryA(cur, asin)

        elif (option == 'b' or option == 'B'):
            asin = input("\nDigite o código ASIN do produto desejado: ")
            queryB(cur, asin)

        elif (option == 'c' or option == 'C'):
            asin = input("\nDigite o código ASIN do produto desejado: ")
            queryC(cur, asin)

        elif (option == 'd' or option == 'D'):
            queryD(cur)

        elif (option == 'e' or option == 'E'):
            queryE(cur)

        elif (option == 'f' or option == 'F'):
            queryF(cur)

        elif (option == 'g' or option == 'G'):
            queryG(cur)

        elif (option == 'q' or option == 'Q' ):
            sys.exit()
        elif (option == 'l' or option == 'L'):
            with open(outputFile, "w") as f:
                f.close()
        else:   
            print("\n**************Escolha  uma opção válida!!!**************\n")  
        
 

if __name__=='__main__':
    chooseQuery()

