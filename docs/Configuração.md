### Configuração

O arquivo Config.json talvez seja um dos mais importantes desse código, é ele quem rege quem é o modelo. 

Temos a seguinte estrutura:

- system_prompt
- max_tokens
- temperature
- stop
- echo

## System_Prompt, o que é?

O Sistem prompt serve para dar personalidade ao modelo de I.A, por exemplo "Você é (apelido para seu modelo) e seu trabalho é
me ajudar me dando suporte.". Pense em um cachorrinho, você adota e já o ensina desde filhote como se portar e ser, assim é o modelo,
só que instantâneamente rápido.

## max_tokens

É o máximo de palavras que seu modelo pode gerar, é um limite imposto, pois o modelo só saberá a hora de parar vindo dessa configuração
em específico.

## temperature

Temperature é o nível máximo de criatividade e liberdade que o modelo tem. Geralmente se você quer estudar e não quer algo muito narrativo
e mais direto, use entre 0.4 à 0.8. Para Roleplay vai depender da narrativa e do System_Prompt, se o System_Prompt dá muita liberdade, mas
o temperature não, é capaz do modelo não fazer o que você deseja para aquilo, pode-se dizer que entre 0.9 à 1.8 dependendo do modelo, aí vale
testar.

## Stop

Controla até aonde vai o chat, geralmente usado para interromper o modelo.

## Echo

É um eco, digamos que todo system prompt que foi inserido e temperature e afins, tudo que está rodando no contexto vai aparecer ali.

# Atenção:

Não recomendo a ativação do Echo, ele vai poluir seu chat.
