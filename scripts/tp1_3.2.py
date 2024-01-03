import psycopg2

#Mudar de acordo com as suas informações
host="localhost"
database="amazon_agk"
user="postgres"
password="postgres"
inputFile = "../postgres-data/amazon-meta.txt"

def createTables():
    try:
        print("Criando tabelas usando PostgreSQL...")
        conn = psycopg2.connect(
            "host=" + host +
            " dbname=" + database +
            " user=" + user +
            " password=" + password
        )
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS Products ( 
            ID_product INT NOT NULL UNIQUE,
            ASIN CHAR(10) PRIMARY KEY,
            title VARCHAR(500),
            group_name VARCHAR(20),
            salesrank INT);''' 
        )
        cur.execute('''CREATE TABLE IF NOT EXISTS ProductsSimilar ( 
                    ASIN_initial CHAR(10), 
                    ASIN_similar CHAR(10), 
                    PRIMARY KEY (ASIN_initial, ASIN_similar), 
                    FOREIGN KEY (ASIN_initial) REFERENCES Products(ASIN));''' 
        )
        cur.execute('''CREATE TABLE IF NOT EXISTS Categories ( 
                    category_name VARCHAR(250) PRIMARY KEY);'''
        ) 
        cur.execute('''CREATE TABLE IF NOT EXISTS ProductsCategories ( 
                    ASIN CHAR(10),
                    category_name VARCHAR(250),
                    PRIMARY KEY (ASIN, category_name),
                    FOREIGN KEY (ASIN) REFERENCES Products(ASIN),
                    FOREIGN KEY (category_name) REFERENCES Categories(category_name));'''
        )
        cur.execute('''CREATE TABLE IF NOT EXISTS ProductsReviews (
                    reviewID SERIAL PRIMARY KEY,
                    ASIN CHAR(10),
                    customer VARCHAR(20), 
                    date DATE,
                    rating INT,
                    votes INT,
                    helpful INT,
                    FOREIGN KEY (ASIN) REFERENCES Products(ASIN));'''
        )
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print ("Erro ao tentar criar tabelas", error)
        exit()
    if(conn):
        cur.close()
        conn.close()
    print("Tabelas criadas")
    
def insertCategories(cur, category):
    try:
        cur.execute(f'''INSERT INTO Categories(category_name) VALUES (%s) ON CONFLICT (category_name) DO NOTHING;''', (category,))
    except (Exception, psycopg2.DatabaseError) as error:
        print("Erro ao tentar inserir na tabela Categories", error)
        exit()

def insertProductsCategories(cur, ASIN, category):
    try:
        cur.execute(f'''INSERT INTO ProductsCategories(ASIN, category_name) VALUES ('{ASIN}', %s) ;''', (category,))
    except (Exception, psycopg2.DatabaseError) as error:
        print("Erro ao tentar inserir na tabela ProductsCategories", error)
        exit()
    
def insertProducts(cur, ID, ASIN, title, group_name, salesrank):
    try:
        cur.execute(f'''INSERT INTO Products(ID_product, ASIN, title, group_name, salesrank) VALUES ({ID}, '{ASIN}', %s, '{group_name}', %s);''', (title, salesrank))
    except (Exception, psycopg2.DatabaseError) as error:
        print("Erro ao tentar inserir na tabela Products", error)
        exit()
    
def insertProductsReviews(cur, ASIN, customer, date, rating, votes, helpful):
    try:
        cur.execute(f'''INSERT INTO ProductsReviews(ASIN, customer, date, rating, votes, helpful) VALUES ('{ASIN}', '{customer}', '{date}', '{rating}', '{votes}', '{helpful}');''')
    except (Exception, psycopg2.DatabaseError) as error:
        print("Erro ao tentar inserir na tabela ProductsReviews", error)
        exit()
    
def insertProductsSimilar(conn, cur, ASIN_initial, ASIN_similar):
    try:
        cur.execute(f'''INSERT INTO ProductsSimilar(ASIN_initial, ASIN_similar) VALUES ('{ASIN_initial}', '{ASIN_similar}') ON CONFLICT (ASIN_initial, ASIN_similar) DO NOTHING;''')
    except psycopg2.IntegrityError:
        conn.rollback()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Erro ao tentar inserir na tabela ProductsSimilar", error)
        exit()
    conn.commit()

def readFile():
    try:
        print("Conectando com o PostgreSQL...")
        conn = psycopg2.connect(
            "host=" + host +
            " dbname=" + database +
            " user=" + user +
            " password=" + password
        )
        cur = conn.cursor()
    except (Exception, psycopg2.DatabaseError) as error:
        print ("Erro ao conectar com o PostgreSQL", error)
    print("Conexão com o PostgreSQL efetivada")
    similares = []
    print('Lendo arquivo de entrada...')
    with open(inputFile) as f:
        #Pula o cabeçario
        f.readline()
        f.readline()
        f.readline()
        for line in f:
            #Ler ID
            line = line.split()
            ID = line[1]
            #Ler ASIN
            line = f.readline().split()
            ASIN = line[1]
            #Ler titulo ou informação que o produto foi descontinuado
            line = f.readline().split()
            if line[0] == 'discontinued' :
                ID = ''
                ASIN = ''
                f.readline()
            else:
                line = line[1:]
                title=' '.join(line)
                #Ler grupo
                line = f.readline().split()
                line = line[1:]
                group = ''.join(line)
                #Ler salesrank
                line = f.readline().split()
                salesrank = line[1]
                if (salesrank == "-1" or salesrank == "0"):
                    salesrank = None    
                insertProducts(cur, ID, ASIN, title, group, salesrank)
                #Ler produtos similares
                line = f.readline().split()
                for i in range(2, int(line[1])+2):
                    similar = line[i]
                    similares.append([ASIN, similar])
                #Ler Categorias
                line = f.readline().split()
                for i in range(int(line[1])):
                    category = f.readline()
                    category = str(category)
                    category = category.strip()
                    insertCategories(cur, category)
                    insertProductsCategories(cur, ASIN, category)
                #Ler avaliações
                line = f.readline().split()
                for i in range(int(line[4])):
                    review = f.readline().split()
                    insertProductsReviews(cur, ASIN, review[2], review[0], review[4], review[6], review[8])
                f.readline()
    f.close()
    print("Leitura Concluida")
    print("Inserindo produtos similares...")
    for item in similares:
        insertProductsSimilar(conn, cur, item[0], item[1])
    conn.commit()
    if(conn):
        cur.close()
        conn.close()
    print("Produtos similares inseridos")

if __name__ == '__main__':
   createTables()
   readFile()