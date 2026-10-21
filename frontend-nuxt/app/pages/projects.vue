<script setup lang="ts">
// Define a estrutura de dados que esperamos receber da FastAPI.
interface Projeto{
    id: number
    name: string
    description: string | null
    created_at: string
}

// Endereço da API Python que já testamos no passo anterior.
const apiBase = 'http://127.0.0.1:8000'

// Guarda os valores introduzidos pelo utilizador no formulário.
const formulario = reactive({
    name: '',
    description: ''
})

// Guarda a lista de projetos recebidos do backend
const projetos = ref<Projeto[]>([])

// Controla o estado do formulário e as mensagens apresentadas.
const aCarregar = ref(false)
const aCriar = ref(false)
const erro = ref('')
const sucesso = ref('')

// Pede à FastAPI a lista atualizada de projetos.
async function carregarProjetos(){
    aCarregar.value = true
    erro.value = ''

    try {
        projetos.value = await $fetch<Projeto[]>(
            `${apiBase}/api/taskflow/projects`
        )
    } catch (error) {
        console.error('Erro ao carregar projetos: ', error)
        erro.value = 'Não foi possivel carregar os projetos. Confirma se a FastAPI está ligada.'
    } finally {
        aCarregar.value = false
    }
}

// Envia os dados do formulário para criar um projeto na base de dados.
async function criarProjeto(){
    erro.value = ''
    sucesso.value = ''
    aCriar.value = true

    try {
        // O POST envia os campos em JSON para o endpoint da FastAPI.
        const novoProjeto = await $fetch<Projeto>(
            `${apiBase}/api/taskflow/projects`,
            {
                method: 'POST',
                body:{
                    name: formulario.name.trim(),
                    description: formulario.description.trim() || null,
                },
            }
        )
        // Mostra uma confirmação com o nome do projeto criado.
        sucesso.value = `Projeto "${novoProjeto.name}" Criado com Sucesso!`

        // limpa os campos para permitir criar outro projeto.
        formulario.name = ''
        formulario.description = ''

        // Atualiza a lista para mostrar o projeto acabado de criar.
        await carregarProjetos()
    } catch(error: any){
        console.error('Erro ao criar projeto: ', error)

        //A API pode devolver uma mensagem de validação ou outro detalhe.
        erro.value = 
            error?.data?.detail
            ? `Não foi possivel criar o projeto: ${JSON.stringify(error.data.detail)}`
            : 'Não foi possivel criar o projeto. Verifica a ligação à API.'
    }finally{
        aCriar.value = false
    }
}

// Carregar os projetos quando a página é aberta no navegador.
onMounted(() => {
    carregarProjetos()
})
</script>

<template>
    <main class="pagina">
        <header class="cabecalho">
            <h1>TaskFlow</h1>
            <p>Organiza os teus projetos num só lugar.</p>
        </header>

        <section class="cartao">
            <h2>Criar novo projeto</h2>

            <form @submit.prevent="criarProjeto">
                <div class="campo">
                    <label for="nome"> Nome do projeto</label>

                    <input
                        id="nome"
                        v-model="formulario.name"
                        type="text"
                        maxlength="120"
                        placeholder="Ex.: O meu primeiro projeto"
                        required
                    />
                </div>

                <div class="campo">
                    <label for="descricao">Descrição</label>

                    <textarea
                        id="descricao"
                        v-model="formulario.description"
                        rows="4"
                        placeholder="Descreve brevemente o projeto..."
                    />

                </div>

                <button type="submit" :disabled="aCarregar">
                    {{ aCriar ? 'A criar...' : 'Criar Projeto' }}
                </button>
            </form>

            <p v-if="sucesso" class="mensagem sucesso" role="status">
                {{ sucesso }}
            </p>

            <p v-if="erro" class="mensagem erro" role="alert">
                {{ erro }}
            </p>

        </section>
    </main>
</template>