# The CAIO Lectures on Machine Learning

CAIO = Chief AI Officer.

Caio Gomes · Como pensar em aprendizado de máquina / How to Think About Machine Learning

Livro aberto para leitura em português brasileiro e inglês. As duas edições incluem os sete capítulos de **A aposta e a moeda** e o interlúdio que abre caminho para a regressão. O sumário traz o plano das cinco partes. A pasta **docs** contém o site pronto para publicar, com HTML, equações MathML, figuras vetoriais, índices de busca, PDFs e os fontes LaTeX de cada edição.

## Publicar no GitHub Pages

1. Crie um repositório público para o livro. Uma sugestão de nome é **learning-from-a-coin-toss**. Um repositório dedicado mantém o livro ao lado de uma página pessoal que já exista.
2. Extraia o ZIP e envie **o conteúdo** para a raiz da branch **main**. Ao abrir a raiz do repositório, você deve ver **docs/**, **content/**, **tools/** e este README. O arquivo **docs/.nojekyll** faz parte do pacote.
3. Abra **Settings → Pages → Build and deployment**. Em **Source**, selecione **Deploy from a branch**. Selecione **main** e **/docs** e clique em **Save**.
4. Depois do deploy, use **Visit site** na mesma tela. Os links relativos funcionam tanto na raiz de um domínio quanto no caminho de projeto que o GitHub atribui ao repositório.

A página inicial oferece os dois idiomas. A busca é local, e o controle PT-BR / EN leva ao capítulo correspondente. As definições de termos de reutilização do texto e do código ficam a cargo do autor.

[Documentação do GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

## Ler e testar no computador

Na raiz do pacote, rode o comando abaixo e abra <http://localhost:8000/>. O servidor também permite testar a busca, que carrega o índice de cada idioma por HTTP.

    python3 -m http.server 8000 --directory docs

## Atualizar as edições

Edite os capítulos em **content/pt-br/** e **content/en/**. Cada arquivo numerado tem o texto integral do capítulo e a mesma posição nos dois idiomas. Os preâmbulos tipográficos estão em **content/preamble-pt-br.tex** e **content/preamble-en.tex**. Os arquivos em **docs/** são a saída já construída. O CSS e o JavaScript do leitor vivem diretamente em **docs/assets/**.

A introdução de cada edição fica em **content/pt-br/introduction.tex** e **content/en/introduction.tex** e alimenta tanto o PDF quanto a página `introduction.html` do leitor. No PDF, a capa e a folha de rosto são seguidas pela página de créditos, pelo sumário e pela introdução. A página de créditos vem de `credits.tex` na pasta de cada idioma. As páginas preliminares usam algarismos romanos e o capítulo 1 começa na página 1. O sumário usa os títulos dos capítulos e referências de página calculadas pelo LaTeX. A tipografia dessa abertura está em **content/frontmatter.tex**.

O miolo dos PDFs usa páginas de **16,5 × 23,5 cm**, Palatino de **12 pontos**, entrelinha ampliada e uma pequena separação entre parágrafos. Quadros, tabelas e subtítulos têm espaçamento próprio. A edição em português usa a hifenização brasileira do Babel. Esses ajustes ficam nos preâmbulos de cada idioma.

Cada capítulo termina com um quadro de três ideias principais, uma síntese do que mudou no raciocínio e uma pergunta para levar adiante. Esses fechamentos ficam no final dos próprios arquivos de capítulo, nas duas línguas, e aparecem tanto no PDF quanto no site.

Entre duas partes há um interlúdio sem número, com página própria. Quem escreve pode partir de um objeto da parte anterior, entregá-lo a alguém que precisa tomar outra decisão e encerrar a cena no ponto em que o leitor também quer saber a resposta. Os arquivos `interlude-07.tex`, `interlude-09.tex`, `interlude-11.tex` e `interlude-13.tex` ficam nas duas pastas de idioma. Cada interlúdio entra no PDF e no leitor depois que o capítulo de mesmo número existe. Os três textos das partes em preparação podem ser revistos junto com os capítulos vizinhos.

Para ler os quatro interlúdios em sequência, abra a prova em [português](provas/interludios-pt-br.pdf) ou [inglês](provas/interludes-en.pdf). O comando `python3 tools/print_editions.py --interludes-only` atualiza as duas provas.

Para reconstruir, use Python 3.12+, Pandoc 3, TeX Live com latexmk, TikZ, standalone e fontes Palatino (mathpazo), e Poppler com pdftocairo. Os scripts Python usam a biblioteca padrão.

    python3 tools/print_editions.py
    python3 tools/build.py

O primeiro comando gera os dois PDFs, os fontes completos em LaTeX e as figuras. O segundo gera a capa bilíngue, as duas páginas de apresentação, as páginas dos capítulos e os índices de busca. Suba as mudanças nos fontes e em **docs/** para atualizar o site.

As capas dos PDFs usam a arte em **content/cover/coin-toss.png**, com tipografia editável em **content/cover/cover.tex** e subtítulos por idioma em **tools/print_editions.py**. O prompt da ilustração está em **content/cover/prompt.txt**. A construção também exporta as capas separadas como **docs/downloads/cover-pt-br.pdf** e **cover-en.pdf**, com prévias PNG em **docs/assets/**. Os links “Fonte LaTeX” baixam um ZIP com o manuscrito e a ilustração; extraia ambos na mesma pasta antes de compilar com `latexmk -pdf`. A capa não entra na numeração dos capítulos.

Para acrescentar um capítulo, crie o mesmo número nas duas pastas de idioma e reconstrua. As divisões entre partes ficam em **tools/manuscript.py**. Os nomes das partes, as descrições e os títulos provisórios ficam em **tools/layout.py**. Quando o capítulo fica pronto, os dois sumários passam a usar o título do manuscrito.

## English

This repository contains the seven completed chapters in Brazilian Portuguese and English. It includes both PDFs and the editable LaTeX sources. To publish the prebuilt reader, upload the contents to a repository and select **Settings → Pages → Deploy from a branch → main → /docs**. To work on the book locally, edit the numbered chapters under **content/** and run the two build commands above.

The chapter navigation, search and organization into parts take inspiration from Matheus Facure’s [Causal Inference for the Brave and True](https://matheusfacure.github.io/python-causality-handbook/landing-page.html).
