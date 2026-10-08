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

# Personalização do programa para deixar o visual diferente do padrão.
janela = glfw.create_window(640, 640, "Quadrado do Meu Estilo", None, None)
if not janela:
    glfw.terminate()
    sys.exit("FALHA: não foi possível criar a janela")

glfw.make_context_current(janela)
ctx = moderngl.create_context()

prog = ctx.program(
    vertex_shader=(SHADERS / "basico.vert").read_text(encoding="utf-8"),
    fragment_shader=(SHADERS / "basico.frag").read_text(encoding="utf-8"),
)

# Personalização das cores para um visual mais moderno.
vertices = np.array([
    -0.5, -0.5, 0.0, 1.0,   0.95, 0.50, 0.20, 1.0,  # v0: laranja
     0.5, -0.5, 0.0, 1.0,   0.25, 0.75, 0.95, 1.0,  # v1: azul
     0.5,  0.5, 0.0, 1.0,   0.85, 0.25, 0.85, 1.0,  # v2: roxo
    -0.5,  0.5, 0.0, 1.0,   0.30, 0.90, 0.65, 1.0,  # v3: verde
], dtype="f4")

# Diagonal principal com um toque diferente.
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

    # Fundo pastel para diferenciar do padrão clássico.
    ctx.clear(0.96, 0.93, 1.0, 1.0)
    vao.render(moderngl.TRIANGLES)
    glfw.swap_buffers(janela)
    glfw.poll_events()

vao.release()
ebo.release()
vbo.release()
prog.release()
glfw.terminate()
print("Execução finalizada.")
