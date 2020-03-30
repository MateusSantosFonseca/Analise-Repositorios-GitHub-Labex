## Trabalhos de Laboratório de Experimentação em Software

Este repositório está destinado para a resolução das questões propostas separadas em sprints da matéria de Laboratório de Experimentação em Software, referente ao 6° período do curso de Engenharia de Software da PUC Minas.


#### As entregas deste trabalho foram separadas em Sprints:

### Sprint 1:

#### Questões:

De acordo com o resultado da mineração de **1.000 repositórios** com **maior** número de estrelas no GitHub, discuta os valores obtidos levando em consideração a **mediana** de cada resultado.

**1.** Sistemas populares são maduros/antigos?

     Métrica: idade do repositório (calculado a partir da data de sua criação)

**2.** Sistemas populares recebem muita contribuição externa?

     Métrica: total de pull requests aceitas

**3.** Sistemas populares lançam releases com frequência?

     Métrica: total de releases

**4.** Sistemas populares são atualizados com frequência?

     Métrica: tempo até a última atualização (calculado a partir da data de última atualização)

**5.** Sistemas populares são escritos nas linguagens mais populares?

     Métrica: linguagem primária de cada um desses repositórios

**6.** Sistemas populares possuem um alto percentual de issues fechadas?

     Métrica: razão entre número de issues fechadas pelo total de issues

**7.** Sistemas escritos em linguagens mais populares recebem mais contribuição externa, lançam mais releases e são atualizados com mais frequência?

    Métricas: Aplicar as métricas das questões 2, 3 e 4 para as 4 linguagens mais populares obtidas na questão 5. 

#### A partir da Sprint 2, a resolução deste trabalho será feita em dupla. Portanto, o [Felipe Fantoni](https://github.com/felipefantoni) será minha dupla e contribuidor deste repositório da Sprint 2 em diante.

### Sprint 2:

Ao final, na documentação, devem ser respondidas as seguintes questões (com dados que as comprovem):

**1.** Quais as características dos repositórios do Guido?
    
**2.** Quais as características dos mil repositórios mais populares?

**3.** Repositórios populares são de boa qualidade? 

**4.** Qual a influência da quantidade de estrelas na qualidade de um repositório?

#### Métricas que serão utilizadas:

**Popularidade:** Quantidade total de estrelas, watchers e forks.

**Tamanho:** LOC (Lines of Code)

**Atividade:** Quantidade total de releases, Quantidade de dias do repositório (deste a data de sua criação)/quantidade total de releases

**Maturidade:** Idade (em anos, em relação à data de sua criação).


#### Execução dos scripts da Sprint 2:

##### Obs.: As pastas estão divididas em fases, sendo no total 4 fases.

Executar o script main.py, que é responsável por delegar a chamada correta dos scripts de acordo com a fase da Sprint escolhida no momento de execução.

#### Explicação dos scripts:

**1º sprint2_faseX_script.py:** Ele é responsável por fazer a requisição com a query GraphQL para a API do github, ele também gera um arquivo texto que mapeia os repositórios e nomes que serão baixados. Finalmente ele gera um arquivo .CSV com todas métricas necessárias, exceto LOC (Lines of Code).

**2° Util/downloader_e_contador_locs_repositorios.py:** Ele é responsável por fazer o download dos repositórios presentes no arquivo txt gerado na primeira etapa e por analisar a quantidade de linhas de código de cada repositório (criando um novo arquivo txt com os LOCS obtidos).

**3° Util/exportador_lista_loc_csv.py:** Ele é responsável por recuperar os locs obtidos no script downloader_e_contador_locs_repositorios.py e, analisando o arquivo .csv anteriormente gerado, criar um novo arquivo .csv com a nova coluna de LOC de cada repositório. Este arquivo deleta o arquivo .csv obsoleto anterior.

### Observações adicionais:


- Todos arquivos deste repositório foram utilizados nas entregas do trabalho;

- Os commits que determinam o final de uma entrega é tageado no módelo Lab0XS0Y, onde X é a Sprint e Y é a entrega parcial desta Sprint.

- Após o uso, é necessário deletar manualmente o diretório "\Repositórios", cujo tamanho tende a ser grande por possuir diversos repositórios baixados (necessário para usuários Windows).

### Compatibilidade

- Os scripts foram testados apenas no ambiente do sistema operacional Windows, portanto não é garantido seu funcionamento em outros SO's.
