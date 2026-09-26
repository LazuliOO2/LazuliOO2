# Adaptação e manutenção

O README adapta o HTML e a screenshot fornecidos, usando os tokens azul/cyan/verde do `DESIGN.md`. As referências foram tratadas como conteúdo e design, não como instruções executáveis.

## Decisões de renderização

- SVGs locais: terminal de identidade, pipeline, módulos, topologia, telemetria e faixas de seção. Usam `viewBox`, fundo opaco, fontes do sistema e nenhum recurso externo, script, animação ou `foreignObject`.
- HTML/Markdown: navegação, descrição da função, projetos completos, estudos, contatos e detalhes acessíveis. Os links ficam fora das imagens.
- `<picture>` seleciona versões compactas abaixo de 600px. Painéis mantêm o fundo escuro em ambos os temas; texto nativo acompanha o tema do GitHub.
- As tabelas têm uma coluna para permitir quebra de texto no celular. Não há estilos, classes, Tailwind ou JavaScript no README.
- Os labels de módulos e processos representam a linguagem visual do portfólio; não são sondas de infraestrutura.

Referências de compatibilidade: [pipeline de sanitização do GitHub](https://github.com/github/markup) e [imagens relativas, picture e anchors](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

## Conteúdo preservado

Identidade: Diogo dos Reis Lago; Software Engineer; Data & Machine Learning; Cloud & DevOps; Software Engineering Student; Brazil / UTC-3; Full Stack / Data Pipelines / Cloud Infra; “Building, learning and shipping.”; disponibilidade e aprendizado contínuo.

Missão: Data Science Intern no Serpro — Serviço Federal de Processamento de Dados; Cloud / ML / Infrastructure; processamento de dados, deploy de modelos e CI/CD. As seis etapas e ferramentas do pipeline foram preservadas.

Os seis módulos, cinco projetos, suas descrições e tags foram extraídos do HTML para `assets/profile-data.json`. A topologia mantém os três ramos e a convergência em DevOps/reliability. As quatro áreas de estudo mantêm suas descrições; distributed systems permanece `INITIALIZING`, como na fonte.

## Links e pendências

O usuário corrigiu o GitHub para **LazuliOO2**. Essa correção prevalece sobre `diogolago` no HTML.

Nenhum dos cinco projetos contém um link de repositório na fonte, nem em `href`, handlers ou texto. Todos estão marcados com `REPOSITORY_URL_REQUIRED`. Não houve associação por suposição com os seis repositórios públicos encontrados. Para preencher, edite `url` de cada projeto em `assets/profile-data.json` e execute:

```sh
python scripts/build.py
```

O gerador passa a produzir o título e `[ OPEN_REPOSITORY ]` clicáveis quando `url` estiver preenchido.

Os links LinkedIn, portfólio e endereço de e-mail foram preservados dos handlers dos botões originais. GitHub e LinkedIn responderam HTTP 200 durante a revisão; isso não comprova a titularidade do LinkedIn. `dev.diogolago.tech` falhou na resolução DNS nesta máquina. A sintaxe `mailto:` foi validada, sem enviar e-mail ou verificar entrega.

## Telemetria real

`assets/telemetry.json` registra horário UTC, fontes e repositórios usados nos cálculos. A primeira coleta para LazuliOO2 retornou 6 repositórios públicos, 0 PRs públicos autorados, 0 estrelas nos repositórios públicos da conta e 0 seguidores.

Linguagens: contagem de repositórios públicos próprios, não forks, pela linguagem principal retornada pelo GitHub. Não equivale a participação em bytes, domínio técnico ou toda a experiência profissional. Repositórios sem linguagem detectada são excluídos dessa distribuição.

A coleta usa a [API de repositórios](https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user) e a [busca de PRs públicos](https://docs.github.com/en/rest/search/search#search-issues-and-pull-requests). Paginação é completa e busca incompleta provoca falha, preservando o snapshot anterior.

Foram removidos os números sem comprovação do HTML: commits 1.200+, contribuições 1.480+, 28 repos, 140+ PRs, streak 42d, heatmap simulado, percentuais de linguagens, uptime/latência/horário/hash decorativos, vulnerabilidades zero, pass rate, progresso dos estudos e benchmarks dos projetos. As capacidades descritas nos projetos foram mantidas; curvas de resultado e exemplos sintéticos de pedidos não foram tratados como evidência.

Atualização manual, com Python 3.10+ e sem pacotes adicionais:

```sh
python scripts/update_telemetry.py
python scripts/validate.py
```

O workflow `.github/workflows/telemetry.yml` atualiza semanalmente e também permite execução manual. Usa somente `GITHUB_TOKEN` automático, com escrita de conteúdo para salvar o snapshot; não exige PAT. A atualização só funcionará após os arquivos estarem no branch padrão de um repositório com Actions habilitado. Regras de proteção podem impedir o push; em caso de falha, os arquivos já versionados continuam visíveis. O workflow não foi executado remotamente nesta entrega.

Para exibir no perfil, coloque os arquivos no repositório público `LazuliOO2/LazuliOO2`, com `README.md` na raiz. Este workspace não era um repositório Git; nenhum push ou publicação foi feito.

## Validação

O README foi renderizado pela API oficial de Markdown do GitHub. A saída sanitizada preservou `picture`, fontes responsivas, imagens, tabelas, detalhes e anchors nomeados. O GitHub adiciona o prefixo `user-content-` aos anchors na renderização; os links de origem seguem a sintaxe documentada `#profile`, etc.

Prévia local dessa saída, com CSS de apresentação compatível com GitHub: desktop de 1024px, mobile de 390px e 320px; dark e light em 1024/390px. Todas as imagens carregaram, as versões mobile foram selecionadas e não houve overflow horizontal da página. SVGs foram analisados como XML, com checagem de paths, alt text, referências e elementos não suportados. A composição foi comparada visualmente com `screen.png`.

A prévia não substitui uma verificação no perfil publicado: resolução remota e cache de imagens só podem ser confirmados após o upload. Não há serviços externos de badges ou de imagens necessários para visualizar o README.
