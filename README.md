# Similarity and Relatedness Measures

Biblioteca criada com o intuito de calcular a similaridade entre classes dentro de uma ontologia. 

# Documentação da Biblioteca owlsimilarity

## Descrição

A biblioteca `owlsimilarity` é uma ferramenta para calcular diversas medidas de similaridade e relacionamento em ontologias OWL (Web Ontology Language). Essas medidas podem ser classificadas em três categorias principais: medidas baseadas em caminho, medidas de conteúdo de informação e medidas híbridas.

A biblioteca utiliza uma ontologia específica fornecida pelo usuário (no exemplo, "animais.owl") para calcular as medidas de similaridade e relacionamento entre classes na ontologia.

## Instalação

```bash
pip install owlsimilarity
```

## Medidas Disponíveis

### Medidas Baseadas em Caminho

- `sim_path_df()`: Similaridade de caminho.
- `sim_wup_df()`: Similaridade Wu-Palmer.
- `sim_nguyan_df()`: Similaridade Nguyen.
- `sim_leacock_df()`: Similaridade Leacock-Chodorow.
- `sim_li_df()`: Similaridade Li.
- `sim_batet_df()`: Similaridade Batet.

### Medidas de Conteúdo de Informação

- `sim_resnik_df(seco)`: Similaridade Resnik.
- `sim_jiang_df(seco)`: Similaridade Jiang-Conrath.
- `sim_lin_df(seco)`: Similaridade Lin.
- `sim_jaccard_df(seco)`: Similaridade Jaccard.
- `sim_meng_df(seco)`: Similaridade Meng.

### Medidas Híbridas

- `sim_zhou_df()`: Similaridade Zhou.
- `sim_hasdj_df()`: Similaridade Hasdjian.

### Medidas de Relacionamento

- `rel_mazuel_df()`: Relacionamento de Mazuel.
- `rel_zhang_df()`: Relacionamento de Zhang.

## Parâmetros Adicionais

- `seco`: Um parâmetro possível para as medidas de conteúdo de informação (`sim_resnik_df`, `sim_jiang_df`, `sim_lin_df`, `sim_jaccard_df`, `sim_meng_df`).
- `sanchez`: Seria um segundo parâmetro possível para ser passado como parâmetro
- Nada mais são do que maneiras de calcular o information content dessas medidas

## Saída

Os resultados das medidas são armazenados em DataFrames do pandas e podem ser salvos em arquivos CSV para análise posterior.

## Exemplo de Uso

```python
import owlsimilarity as ow

# Carregar a ontologia passando o caminho do arquivo OWL como parâmetro
classe = ow.SimilarityOnto("animais.owl")

# Medidas Baseadas em Caminho
df = classe.sim_path_df()
df.to_csv("csvs/simPath")

df = classe.sim_wup_df()
df.to_csv("csvs/simWuP")

df = classe.sim_nguyan_df()
df.to_csv("csvs/simNguyan")

df = classe.sim_leacock_df()
df.to_csv("csvs/simLeacock")

df = classe.sim_li_df()
df.to_csv("csvs/simLi")

df = classe.sim_batet_df()
df.to_csv("csvs/simBatet")

print("#################")

# Medidas de Conteúdo de Informação
df = classe.sim_resnik_df("seco")
df.to_csv("csvs/simResnik")

df = classe.sim_jiang_df("seco")
df.to_csv("csvs/simJiang")

df = classe.sim_lin_df("seco")
df.to_csv("csvs/simLin")

df = classe.sim_jaccard_df("seco")
df.to_csv("csvs/simJaccard")

df = classe.sim_meng_df("seco")
df.to_csv("csvs/simMeng")

print("#################")

# Medidas Híbridas
df = classe.sim_zhou_df()
df.to_csv("csvs/simZhou")

df = classe.sim_hasdj_df()
df.to_csv("csvs/simHasdj")

# Medidas de Relacionamento
df = classe.rel_mazuel_df()
df.to_csv("csvs/relMazuel")

df = classe.rel_zhang_df()
df.to_csv("csvs/simZhang")
```

## Notas

Certifique-se de substituir "animais.owl" pelo caminho real do seu arquivo de ontologia OWL.

Este é um exemplo básico de uso da biblioteca `owlsimilarity`.
