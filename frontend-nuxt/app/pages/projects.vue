
<script setup lang="ts">
interface Projeto {
  id: number
  name: string
  description: string | null
  created_at: string
}

// Endereço da API FastAPI
const apiBase = 'http://127.0.0.1:8000'

const formulario = reactive({
  name: '',
  description: ''
})

const projetos = ref<Projeto[]>([])

const aCarregar = ref(false)
const aCriar = ref(false)
const erro = ref('')
const sucesso = ref('')

// Carregar os projetos existentes
async function carregarProjetos() {
  aCarregar.value = true
  erro.value = ''

  try {
    projetos.value = await $fetch<Projeto[]>(
      `${apiBase}/api/taskflow/projects`
    )
  } catch (error) {
    console.error('Erro ao carregar projetos:', error)
    erro.value =
      'Não foi possível carregar os projetos. Confirma se a FastAPI está ligada.'
  } finally {
    aCarregar.value = false
  }
}

// Criar um novo projeto
async function criarProjeto() {
  erro.value = ''
  sucesso.value = ''

  if (!formulario.name.trim()) {
    erro.value = 'O nome do projeto é obrigatório.'
    return
  }

  aCriar.value = true

  try {
    const novoProjeto = await $fetch<Projeto>(
      `${apiBase}/api/taskflow/projects`,
      {
        method: 'POST',
        body: {
          name: formulario.name.trim(),
          description: formulario.description.trim() || null
        }
      }
    )

    sucesso.value =
      `Projeto "${novoProjeto.name}" criado com sucesso!`

    formulario.name = ''
    formulario.description = ''

    await carregarProjetos()
  } catch (error: any) {
    console.error('Erro ao criar projeto:', error)

    erro.value = error?.data?.detail
      ? `Não foi possível criar o projeto: ${
          typeof error.data.detail === 'string'
            ? error.data.detail
            : JSON.stringify(error.data.detail)
        }`
      : 'Não foi possível criar o projeto. Verifica a ligação à API.'
  } finally {
    aCriar.value = false
  }
}

// Carregar os projetos quando a página é montada
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
          <label for="nome">Nome do projeto</label>

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
          ></textarea>
        </div>

        <button type="submit" :disabled="aCriar || aCarregar">
          {{ aCriar ? 'A criar...' : 'Criar projeto' }}
        </button>
      </form>

      <p
        v-if="sucesso"
        class="mensagem sucesso"
        role="status"
      >
        {{ sucesso }}
      </p>

      <p
        v-if="erro"
        class="mensagem erro"
        role="alert"
      >
        {{ erro }}
      </p>
    </section>

    <section class="cartao">
      <h2>Os meus projetos</h2>

      <p v-if="aCarregar">
        A carregar projetos...
      </p>

      <p v-else-if="projetos.length === 0">
        Ainda não existem projetos para mostrar.
      </p>

      <ul v-else class="lista-projetos">
        <li
          v-for="projeto in projetos"
          :key="projeto.id"
        >
          <h3>{{ projeto.name }}</h3>

          <p>
            {{ projeto.description || 'Sem descrição.' }}
          </p>

          <small>Projeto #{{ projeto.id }}</small>
        </li>
      </ul>
    </section>
  </main>
</template>

<style scoped>
.pagina {
  max-width: 760px;
  margin: 40px auto;
  padding: 0 20px;
  font-family: Arial, Helvetica, sans-serif;
  color: #222;
}

.cabecalho {
  margin-bottom: 28px;
}

.cabecalho h1 {
  margin-bottom: 8px;
}

.cabecalho p {
  color: #666;
}

.cartao {
  margin-bottom: 24px;
  padding: 24px;
  border: 1px solid #ddd;
  border-radius: 12px;
  background: white;
}

.campo {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 18px;
}

input,
textarea {
  box-sizing: border-box;
  width: 100%;
  padding: 12px;
  border: 1px solid #bbb;
  border-radius: 6px;
  font: inherit;
}

button {
  padding: 12px 18px;
  border: none;
  border-radius: 6px;
  background: #2563eb;
  color: white;
  font: inherit;
  cursor: pointer;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.mensagem {
  margin-top: 16px;
  overflow-wrap: anywhere;
}

.sucesso {
  color: #18733b;
}

.erro {
  color: #b42318;
}

.lista-projetos {
  padding: 0;
  list-style: none;
}

.lista-projetos li {
  padding: 16px 0;
  border-bottom: 1px solid #eee;
}

.lista-projetos h3 {
  margin: 0 0 8px;
}

.lista-projetos p {
  margin: 0 0 8px;
  white-space: pre-wrap;
}

.lista-projetos small {
  color: #666;
}
</style>
