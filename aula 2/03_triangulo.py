"""
Triângulo com dados NÃO intercalados.
Um VBO por atributo.
Primeiro programa com shaders em arquivos separados (shaders/basico.*).

MCCC007-23 - Computação Gráfica - UFABC
Prof. João Paulo Gois

Executar: python 03_triangulo.py
Sair: ESC ou fechar a janela
"""
import sys
from pathlib import Path

import glfw
import moderngl
import numpy as np

# Caminho relativo ao arquivo.
# Não ao diretório a partir do qual o Python foi chamado.
SHADERS = Path(__file__).parent / "shaders"


def erro_glfw(codigo, descricao):
    """Substitui o aviso padrão do pyGLFW: imprime código
    e descrição de qualquer erro do GLFW em stderr"""
    print(f"GLFW [{codigo}]: {descricao}", file=sys.stderr)


glfw.set_error_callback(erro_glfw)

if not glfw.init():
    sys.exit("FALHA: glfw nao inicializou")

# Ajuste aqui a versão OpenGL e o perfil do contexto.
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 0)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)

# Mude a resolução e o nome da janela para customizar a apresentação.
janela = glfw.create_window(800, 600, "Olá triângulo (dois VBOs)", None, None)
if not janela:
    glfw.terminate()
    sys.exit("FALHA: não foi possível criar a janela")

glfw.make_context_current(janela)
ctx = moderngl.create_context()

# Para o driver, o shader continua sendo uma string.
# Ela só passou a ser lida a partir de arquivos.
prog = ctx.program(
    vertex_shader=(SHADERS / "basico.vert").read_text(encoding="utf-8"),
    fragment_shader=(SHADERS / "basico.frag").read_text(encoding="utf-8"),
)

# Arranjos independentes na CPU.
# v0 topo
# v1 esquerda
# v2 direita
# Altere estes valores para mover os vértices ou mudar as cores do triângulo.
posicoes = np.array([
    0.0,  0.5, 0.0, 1.0,
   -0.5, -0.5, 0.0, 1.0,
    0.5, -0.5, 0.0, 1.0,
], dtype='f4')

cores = np.array([
    1.0, 0.0, 0.0, 1.0,  # v0 vermelho
    0.0, 1.0, 0.0, 1.0,  # v1 verde
    0.0, 0.0, 1.0, 1.0,  # v2 azul
], dtype='f4')

vbo_pos = ctx.buffer(posicoes.tobytes())
vbo_cor = ctx.buffer(cores.tobytes())

# Um VAO pode reunir vários VBOs.
vao = ctx.vertex_array(prog, [
    (vbo_pos, '4f', 'vPosition'),
    (vbo_cor, '4f', 'vColors'),
])

while not glfw.window_should_close(janela):
    if glfw.get_key(janela, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(janela, True)

    # Ajuste o fundo para uma cor diferente (RGBA).
    ctx.clear(1.0, 1.0, 1.0, 1.0)
    vao.render(moderngl.TRIANGLES)
    glfw.swap_buffers(janela)
    glfw.poll_events()

vao.release()
vbo_pos.release()
vbo_cor.release()
prog.release()
glfw.terminate()
print("Execucao finalizada.")
