
# Trabalho Prático 1 de Bancos de Dados I 

Os detalhes sobre o trablho prático estão disponíveis [aqui](https://docs.google.com/document/d/1CXf_y392fJ_KNTZbdr5TWSRgEuYXFPyGTJOh4DcqOdA/edit): 

## Alunos

    Allan Carvalho de Aguiar    22153696
    Girlana Souza               22152263
    Kethelen do Carmo Souza     22152253

## Copiando esse repositorio

Você deve ter uma conta no github. A criação de contas é gratis e o GitHub é importante para sua visa profissional e carreira

Para fazer isso siga esses passos:

https://user-images.githubusercontent.com/118348/229365938-48d261c8-b569-463c-bc00-462eb218b423.mp4

Para entender melhor [git e github](https://www.alura.com.br/artigos/o-que-e-git-github).

## Configurando

### Docker e Docker Compose

Instalando o [docker desktop e docker compose (Windows, Linux e Mac)](https://www.docker.com/products/docker-desktop/)

Instalando na linha de comando

[Docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04-pt) e [Docker Compose Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04-pt)

#### Como funciona o docker compose

[Docker Compose - Explicado](https://blog.4linux.com.br/docker-compose-explicado/)

### Postgres

Criar pasta `postgres-data` na raiz do projeto. Essa pasta **não deve ser enviada** para o github.

Depois você deve subir o docker-compose com o postgres. Da primeira vez vai demorar um pouco, e fique de olho nos logs para qualquer erro.

```bash
docker-compose up -d
```

### Python

Criar o ambiente virtual

```bash
python3 -m venv .tp1
```

Ativar o ambiente virtual

```bash
source .tp1/bin/activate
```

## Usando o postgres na sua maquina

Após subir, você conseguirá conectar no banco. Ele vem vazio e você terá que preencher ele com o que o trabalho pede.

```bash
psql -h localhost -U postgres
```

As credenciais são:

```yaml
username: postgres
password: postgres
```

## Usando Python

Para instalar bibliotecas necessarias para o trabalho, execute o script [DEPOIS de ativar o ambiente](#python) virtual.

```bash
bash bib.sh
```

# Exemplos

### Resultados da Consulta A para o código 0738700797
 
|   id  |    asin    |    customer    |    date    | rating | votes | helpful |  
|-------|------------|----------------|------------|--------|-------|---------|  
| 33121 | 0738700797 | A1GIL64QK68WKL | 2002-05-23 |   5    |   8   |    8    |  
| 33116 | 0738700797 | A13SG9ACZ9O5IM | 2002-01-24 |   5    |   8   |    8    |  
| 33123 | 0738700797 | A3IGHTES8ME05L | 2003-11-25 |   5    |   5   |    5    |  
| 33122 | 0738700797 | AEOBOF2ONQJWV  | 2003-02-25 |   5    |   8   |    5    |  
| 33114 | 0738700797 | A11NCO6YTE4BTJ | 2001-12-16 |   5    |   5   |    4    |  
| 33124 | 0738700797 | A1CP26N8RHYVVO | 2004-02-11 |   1    |   13  |    9    |  
| 33118 | 0738700797 | A2P6KAWXJ16234 | 2002-02-06 |   4    |   16  |    16   |  
| 33120 | 0738700797 | A3GO7UV9XX14D8 | 2002-03-23 |   4    |   6   |    6    |  
| 33115 | 0738700797 | A9CQ3PLRNIR83  | 2002-01-07 |   4    |   5   |    5    |  
| 33119 | 0738700797 | AMACWC3M7PQFR  | 2002-02-14 |   4    |   5   |    5    |  

### Resultados da Consulta B para o código 0738700797


| ID_product |    ASIN    |                         title                          | group | salesrank |
|------------|------------|--------------------------------------------------------|-------|-----------|
|   170507   | 0738700525 | Midsummer: Magical Celebrations of the Summer Solstice |  Book |   159277  |
|   299250   | 0738700940 |                         Lammas                         |  Book |   58836   |
|   62291    | 1567184960 |        Yule: A Celebration of Light and Warmth         |  Book |   103012  |


### Resultados da Consulta C para o código 0738700797

|    Date    | Average Rating |
|------------|----------------|
| 2001-12-16 |      5.00      |
| 2002-01-07 |      4.50      |
| 2002-01-24 |      4.67      |
| 2002-01-28 |      4.75      |
| 2002-02-06 |      4.60      |
| 2002-02-14 |      4.50      |
| 2002-03-23 |      4.43      |
| 2002-05-23 |      4.50      |
| 2003-02-25 |      4.56      |
| 2003-11-25 |      4.60      |
| 2004-02-11 |      4.27      |
| 2005-02-07 |      4.33      |

### Resultados da Consulta D

|   ID   |    ASIN    |                                                 title                                                  |  group_name | salesrank |
|--------|------------|--------------------------------------------------------------------------------------------------------|-------------|-----------|
| 197564 | 0880881658 |                                  Baby'S Record Keeper And Memory Box                                   | BabyProduct |    1017   |
|  296   | 0385504209 |                                           The Da Vinci Code                                            |     Book    |     19    |
| 390452 | 0385730586 |                   Sisterhood of the Traveling Pants (Sisterhood of Traveling Pants)                    |     Book    |     21    |
| 89000  | 0316346624 |                     The Tipping Point: How Little Things Can Make a Big Difference                     |     Book    |     23    |
| 337971 | 0142001740 |                                        The Secret Life of Bees                                         |     Book    |     26    |
| 154855 | 0066620996 |                  Good to Great: Why Some Companies Make the Leap... and Others Don't                   |     Book    |     29    |
| 376858 | 0671027360 |                                            Angels & Demons                                             |     Book    |     31    |
| 312527 | 0310205719 |                         The Purpose-Driven Life: What on Earth Am I Here For?                          |     Book    |     32    |
| 162283 | 0446677450 | Rich Dad, Poor Dad: What the Rich Teach Their Kids About Money--That the Poor and Middle Class Do Not! |     Book    |     37    |
| 11638  | 1579546463 | The South Beach Diet: The Delicious, Doctor-Designed, Foolproof Plan for Fast and Healthy Weight Loss  |     Book    |     38    |
| 62424  | 0156027321 |                                               Life of Pi                                               |     Book    |     42    |
| 224434 | 1567120709 |                                           SPELLING CORRECTOR                                           |      CE     |   39367   |
| 253628 | 6305275149 |                  Hal Leonard Beginning Bass Guitar 1, Instructional Video, 30 Minutes                  |      CE     |   69089   |
| 228901 | 6305275173 |                    Hal Leonard Beginning Guitar 1, Instructional Video, 30 Minutes                     |      CE     |   71678   |
| 289495 | 1567125336 |                   FRANKLIN COMP. KJB-1440 Electronic Holy Bible (King James Version)                   |      CE     |   84976   |
| 193107 | B00003CX5P |                     Star Wars - Episode I, The Phantom Menace (Widescreen Edition)                     |     DVD     |     28    |
| 137401 | B00006CXSS |                                            Band of Brothers                                            |     DVD     |     47    |
| 104775 | B00001QEE7 |                                   The Little Mermaid (Limited Issue)                                   |     DVD     |     49    |
| 547782 | B00000JS62 |                                            The Wizard of Oz                                            |     DVD     |     55    |
| 544622 | B00006HBUJ |                   Star Wars - Episode II, Attack of the Clones (Widescreen Edition)                    |     DVD     |     85    |
| 136839 | B00005LC1H |                                Fawlty Towers - The Complete Collection                                 |     DVD     |     85    |
|  7524  | B00000JWVS |                   Jerry Seinfeld Live on Broadway: I'm Telling You for the Last Time                   |     DVD     |     88    |
| 544956 | B00005O3VC |                           Monty Python and the Holy Grail (Special Edition)                            |     DVD     |     89    |
| 545557 | B00005JKFR |                                     The Day the Earth Stood Still                                      |     DVD     |     90    |
| 369922 | B00004RFCM |                              Sex and the City - The Complete First Season                              |     DVD     |    102    |
| 370604 | B00004S36S |                                               Buzz Buzz                                                |    Music    |     27    |
| 536884 | B000069AUI |                                      A Rush of Blood to the Head                                       |    Music    |     33    |
| 450096 | B000088E6D |                                             Michael Bublé                                              |    Music    |     42    |
| 187690 | B00005YW4H |                                           Come Away with Me                                            |    Music    |     46    |
| 175533 | B00006879E |                                            Songs About Jane                                            |    Music    |     53    |
| 124898 | B00000JFG3 |                                             Facing Future                                              |    Music    |     55    |
| 370600 | B00004S36U |                                              Victor Vito                                               |    Music    |     62    |
| 505059 | B0000508U6 |                                               Parachutes                                               |    Music    |     67    |
| 270546 | B00008NG5V |                                               On And On                                                |    Music    |     68    |
| 54420  | B00004ZAV3 |                                             The Beatles 1                                              |    Music    |     69    |
| 527037 | 157264317X |                                 ClickArt Christian Publishing Suite 3                                  |   Software  |    200    |
| 96696  | B000001A3A |                                     RINGDISC Wagner: The Ring Disc                                     |   Software  |    327    |
| 456958 | 0310230691 |                          Zondervan Bible Study Library: Leader's Edition 5.0                           |   Software  |    1955   |
| 532431 | B0000897BV |                                   Just Enough Vocals The Learning Co                                   |   Software  |    3771   |
| 243257 | 0735608377 |                                    WINDOWS NT SERVER V4.0 RESOURCE                                     |   Software  |    3828   |
| 310467 | B00002EPXM |                                          Yoga Kit Living Arts                                          |    Sports   |    4684   |
| 257106 | 0963679600 |                                           IlluStory Book Kit                                           |     Toy     |     59    |
| 465900 | 1572810939 |                                        Wizard Card Game Deluxe                                         |     Toy     |    1890   |
| 305664 | 0963679678 |                                       Photostory Junior Book Kit                                       |     Toy     |    2288   |
| 327405 | B000059T05 |                                      Party Tyme Karaoke CD Oldies                                      |     Toy     |    4053   |
|  922   | B000075A8O |                                    Party Tyme Karaoke CD Kids Songs                                    |     Toy     |    7812   |
| 272037 | B000053W7W |                                  Party Tyme Karaoke CD: V2 Super Hits                                  |     Toy     |   10732   |
| 11660  | B000055XW3 |                            The Songs of Britney Spears & Christina Aguilera                            |     Toy     |   31296   |
| 421292 | 0963679627 |                                          R- Photostory Senior                                          |     Toy     |   45241   |
| 297444 | 6300215539 |                                         The War of the Worlds                                          |    Video    |     1     |
| 28339  | 6301627024 |                                           Shirley Valentine                                            |    Video    |     2     |
| 113500 | B00005T33H |                       Leslie Sansone - Walk Away the Pounds - Super Fat Burning                        |    Video    |     6     |
| 334784 | 6302946387 |                                       Robin Hood - Men in Tights                                       |    Video    |     7     |
| 486684 | 6301729897 |                                Richard Simmons - Sweatin' to the Oldies                                |    Video    |     8     |
| 112817 | 6300185788 |                                            Howard the Duck                                             |    Video    |     12    |
| 385458 | 6304015127 |                                            Charlotte's Web                                             |    Video    |     14    |
| 347515 | 6301773586 |                                        A Tree Grows in Brooklyn                                        |    Video    |     16    |
| 161229 | B00006RCT5 |                                           My Neighbor Totoro                                           |    Video    |     17    |
| 297480 | B00006HBUG |                              Star Wars - Episode II, Attack of the Clones                              |    Video    |     17    |
| 51902  | 0761542639 |                         PRIMA PUBLISHING Dark Cloud 2 Official Strategy Guide                          |  VideoGames |    339    |

### Resultados da Consulta E

|   ID   |    ASIN    |                                           title                                           | group | salesrank | average_rating |
|--------|------------|-------------------------------------------------------------------------------------------|-------|-----------|----------------|
| 40220  | 0002250357 |                                Texas the Beautiful Cookbook                               |  Book |   99082   |      5.00      |
| 398844 | 0002202085 |                          London 360: Views Around British Airways                         |  Book |  1109888  |      5.00      |
| 51604  | 0002193183 |             Reptiles and Amphibians of Britain & Europe (Collins Field Guide)             |  Book |  1416004  |      5.00      |
| 297259 | 000215949X |                    Mexico : The Beautiful Cookbook (Beautiful Cookbook)                   |  Book |   50829   |      5.00      |
|  1055  | 0001474103 |                                       Spirit World:                                       |  Book |   159239  |      5.00      |
| 388688 | 0001053744 |                                    Pearl and Sir Orfeo                                    |  Book |   500890  |      5.00      |
| 147139 | 0002159317 | California the Beautiful Cookbook: Authentic Recipes from California (Beautiful Cookbook) |  Book |   84210   |      5.00      |
| 275265 | 0002154463 |                    Italy : The Beautiful Cookbook (Beautiful Cookbook)                    |  Book |   34654   |      5.00      |
| 299097 | 0002154129 |                               France the Beautiful Cookbook                               |  Book |   76171   |      5.00      |
| 376666 | 0002250616 |                  Markets of Provence: A Culinary Tour of Southern France                  |  Book |   36821   |      5.00      |


### Resultados da Consulta F

|                                     category_name                                             | average_rating |
|----------------------------------------------------------------------------------------|----------------|
| \|[139452]\|DVD[130]\|Actors & Actresses[404278]\|( B )[411316]\|Beaudoin, Michelle[412334]   |      5.00      |
| \|[139452]\|DVD[130]\|Actors & Actresses[404278]\|( A )[409682]\|Adams, Robert[409842]        |      5.00      |
| \|[139452]\|DVD[130]\|Actors & Actresses[404278]\|( A )[409682]\|Adams, Ted[409848]           |      5.00      |
| \|[139452]\|DVD[130]\|Actors & Actresses[404278]\|( B )[411316]\|Baker, Jolyon[411518]        |      5.00      |
| \|[139452]\|DVD[130]\|Actors & Actresses[404278]\|( B )[411316]\|Birney, David[413132]        |      5.00      |

### Resultados da Consulta G

|    customer    |  group_name |  cont  |
|----------------|-------------|--------|
| AI9SB5VKUFXDC  | BabyProduct |   1    |
| A37TFIP0OMKGMW | BabyProduct |   1    |
| A2LAH8VX720175 | BabyProduct |   1    |
| ATVPDKIKX0DER  |     Book    | 643185 |
| A3UN6WX5RRO2AG |     Book    | 154531 |
| A14OJS0VWMOSWO |     Book    |  9589  |
|  AFVQZQ8PW0L   |     Book    |  5441  |
| A1K1JW1C5CUSUZ |     Book    |  3562  |
| A2NJO6YE954DBH |     Book    |  2055  |
| A3QVAKVRAH657N |     Book    |  1651  |
| A1NATT3PN24QWY |     Book    |  1535  |
| A1D2C0WDCSHUWZ |     Book    |  1508  |
| A2ODBHT4URXVXQ |     Book    |  1469  |
| A1SFX3CR838F36 |      CE     |   1    |
| A2IX9TMXDBUCYV |      CE     |   1    |
| A13JU90C7AU3RT |      CE     |   1    |
| A1328SYT22GA4U |      CE     |   1    |
| A1J62O1S6QTHZJ |      CE     |   1    |
| ATVPDKIKX0DER  |     DVD     | 63148  |
| A3UN6WX5RRO2AG |     DVD     | 15549  |
| A2NJO6YE954DBH |     DVD     |  1366  |
| AU8552YCOO5QX  |     DVD     |  1213  |
| A3P1A63Q8L32C5 |     DVD     |  859   |
| A3LZGLA88K0LA0 |     DVD     |  856   |
| A82LIVYSX6WZ9  |     DVD     |  683   |
| A152C8GYY25HAH |     DVD     |  675   |
| A16CZRQL23NOIW |     DVD     |  651   |
| A1CZICCYP2M5PX |     DVD     |  650   |
| ATVPDKIKX0DER  |    Music    | 166149 |
| A3UN6WX5RRO2AG |    Music    | 15875  |
| A9Q28YTLYREO7  |    Music    |  2760  |
| A2U49LUUY4IKQQ |    Music    |  1258  |
| A1GN8UJIZLCA59 |    Music    |  1154  |
| A2NJO6YE954DBH |    Music    |  1128  |
| A1J5KCZC8CMW9I |    Music    |  1031  |
| A3MOF5KF93Q6WE |    Music    |  989   |
| AXFI7TAWD6H6X  |    Music    |  814   |
| A38U2M9OAEJAXJ |    Music    |  780   |
| A1XQB8IU7S8WEU |   Software  |   1    |
| A23DFB8IUTIZM0 |   Software  |   1    |
| A1T6PXM2M3N84A |   Software  |   1    |
| A2I0ZWBVR0575O |   Software  |   1    |
| A183K8JAQJW8LZ |   Software  |   1    |
| A1F8RIBFWRYM3Y |   Software  |   1    |
| A1EIVBXG3RD150 |   Software  |   1    |
| A37UFPGDSSMEV  |   Software  |   1    |
| A39UZ9VVRJW4P8 |   Software  |   1    |
| A3D5ICIQ8STPCH |   Software  |   1    |
| AL62LOJKDES3M  |    Sports   |   1    |
| A3O8EZOX2P399L |    Sports   |   1    |
| A18ZVYTEDAOF9A |    Sports   |   1    |
| A2RHSQZ7MAKKCO |    Sports   |   1    |
| A1W180Y9O1FALI |    Sports   |   1    |
| A1SB7SB31ETYZH |     Toy     |   2    |
| ATVPDKIKX0DER  |     Toy     |   2    |
| AH4M07U4YC695  |     Toy     |   2    |
| AH16IHWEMA61J  |     Toy     |   1    |
| A1T3I4JU36IPM5 |     Toy     |   1    |
| A2JTMTR2BZGLX  |     Toy     |   1    |
| A2KTGCRR7UZRG7 |     Toy     |   1    |
| A2PJ7WLZ38F47S |     Toy     |   1    |
| A1OSHA4U8RABFY |     Toy     |   1    |
| A1QW8PHDJBH4IC |     Toy     |   1    |
| ATVPDKIKX0DER  |    Video    | 72581  |
| A3UN6WX5RRO2AG |    Video    | 15814  |
| A2NJO6YE954DBH |    Video    |  1775  |
| AU8552YCOO5QX  |    Video    |  1205  |
| A3P1A63Q8L32C5 |    Video    |  737   |
| A20EEWWSFMZ1PN |    Video    |  720   |
| A16CZRQL23NOIW |    Video    |  668   |
| A3LZGLA88K0LA0 |    Video    |  614   |
| A2QRB6L1MCJ53G |    Video    |  606   |
| A152C8GYY25HAH |    Video    |  583   |
| A3C811U31YG6FS |  VideoGames |   1    |
| A1M4NJYP0WNL8Q |  VideoGames |   1    |
| A226EDS7WDF7S1 |  VideoGames |   1    |