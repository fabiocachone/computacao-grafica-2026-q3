"""
Janela, contexto OpenGL e limpeza do buffer de cor.
MCCC007-23 - Computação Gráfica - UFABC
Prof. João Paulo Gois

Executar: python 01_janela.py      Sair: ESC ou fechar a janela
"""
import sys

import glfw
import moderngl


def erro_glfw(codigo, descricao):
    """Substitui o aviso padrão do pyGLFW: imprime código
    e descrição de qualquer erro do GLFW em stderr"""
    print(f"GLFW [{codigo}]: {descricao}", file=sys.stderr)


glfw.set_error_callback(erro_glfw)

if not glfw.init():
    sys.exit("FALHA: glfw nao inicializou")

# As dicas precisam vir ANTES de create_window
# que será criado junto com a janela. Depois, não há mais o que configurar.
# Ajuste estes valores para mudar a resolução e o perfil gráfico: 4.0/CORE.
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 0)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
# Para funcionar em MacOS, é necessário habilitar o forward compatibility
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)

# Estilo personalizado para diferenciar do padrão.
janela = glfw.create_window(900, 540, "Janela de Estudo - Eu", None, None)
if not janela:
    glfw.terminate()
    sys.exit("FALHA: não foi possível criar a janela")

# moderngl não cria contexto. Ele adota o que estiver ativo na thread.
# Inverter estas duas linhas quebra o programa.
glfw.make_context_current(janela)
ctx = moderngl.create_context()

print(f"GL_VERSION  : {ctx.info['GL_VERSION']}")
print(f"GL_RENDERER : {ctx.info['GL_RENDERER']}")
print(f"GL_VENDOR   : {ctx.info['GL_VENDOR']}")
print(f"GL (codigo) : {ctx.version_code}")
print("\nESC ou feche a janela para sair.")

while not glfw.window_should_close(janela):
    if glfw.get_key(janela, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(janela, True)

    # Estilo próprio: fundo azul-violeta para marcar o projeto.
    ctx.clear(0.22, 0.62, 0.88, 1.0)
    glfw.swap_buffers(janela)
    glfw.poll_events()

glfw.terminate()
print("Execucao finalizada.")
