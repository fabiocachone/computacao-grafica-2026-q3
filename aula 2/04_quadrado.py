"""
Quadrado com EBO: quatro vértices, dois triângulos, seis índices.
MCCC007-23 - Computação Gráfica - UFABC

Executar: python 04_quadrado.py
Sair: ESC ou fechar a janela
"""

import sys
from pathlib import Path

import glfw
import moderngl
import numpy as np

SHADERS = Path(__file__).parent / "shaders"


def erro_glfw(codigo, descricao):
    """Substitui o aviso padrão do pyGLFW: imprime código e descrição em stderr."""
    print(f"GLFW [{codigo}]: {descricao}", file=sys.stderr)


glfw.set_error_callback(erro_glfw)

if not glfw.init():
    sys.exit("FALHA: glfw não inicializou")

# Ajuste aqui a versão e o perfil OpenGL do contexto.
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 0)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)

# Mude o tamanho e o título para personalizar a janela.
janela = glfw.create_window(600, 600, "Quadrado com EBO", None, None)
if not janela:
    glfw.terminate()
    sys.exit("FALHA: não foi possível criar a janela")

glfw.make_context_current(janela)
ctx = moderngl.create_context()

prog = ctx.program(
    vertex_shader=(SHADERS / "basico.vert").read_text(encoding="utf-8"),
    fragment_shader=(SHADERS / "basico.frag").read_text(encoding="utf-8"),
)

# Posição (x, y, z, w) e cor (r, g, b, a) de cada vértice.
# Ajuste estes valores para mudar o formato do quadrado e as cores dos vértices.
vertices = np.array([
    -0.5, -0.5, 0.0, 1.0,   1.0, 0.0, 0.0, 1.0,  # v0: vermelho
     0.5, -0.5, 0.0, 1.0,   0.0, 1.0, 0.0, 1.0,  # v1: verde
     0.5,  0.5, 0.0, 1.0,   0.0, 0.0, 1.0, 1.0,  # v2: azul
    -0.5,  0.5, 0.0, 1.0,   1.0, 1.0, 0.0, 1.0,  # v3: amarelo
], dtype="f4")

# Dois triângulos usando a diagonal 0 - 2.
# Troque a ordem dos índices para alterar qual diagonal será usada.
indices = np.array([0, 1, 2, 2, 3, 0], dtype="u4")

vbo = ctx.buffer(vertices.tobytes())
ebo = ctx.buffer(indices.tobytes())
vao = ctx.vertex_array(
    prog,
    [(vbo, "4f 4f", "vPosition", "vColors")],
    index_buffer=ebo,
)

while not glfw.window_should_close(janela):
    if glfw.get_key(janela, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(janela, True)

    # Ajuste a cor do fundo (RGBA) para mudar o visual do cenário.
    ctx.clear(1.0, 1.0, 1.0, 1.0)
    vao.render(moderngl.TRIANGLES)
    glfw.swap_buffers(janela)
    glfw.poll_events()

vao.release()
ebo.release()
vbo.release()
prog.release()
glfw.terminate()
print("Execução finalizada.")
