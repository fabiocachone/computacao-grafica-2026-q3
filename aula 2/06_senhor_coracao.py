"""
Senhor Coração: uma geometria desenhada várias vezes.

Duas curvas na VRAM (o coração e um círculo) e cinco desenhos por quadro.
O que muda de um desenho para o outro não está em nenhum VBO: está em
variáveis uniformes. As teclas não animam nada — elas trocam o valor de
uma uniforme e o desenho seguinte já sai diferente.

Computação Gráfica - UFABC
"""

import sys
from pathlib import Path

import glfw
import moderngl
import numpy as np

SHADERS = Path(__file__).parent / "shaders"

# Ajuste estas constantes para modificar as cores do coração, olhos e fundo.
MAGENTA = (0.85, 0.10, 0.45, 1.0)
BRANCO_OLHO = (1.0, 1.0, 1.0, 1.0)
PRETO = (0.05, 0.05, 0.05, 1.0)
FUNDO_DIA = (0.96, 0.96, 0.94, 1.0)
FUNDO_NOITE = (0.05, 0.05, 0.12, 1.0)

# Ajuste a escala e a posição dos elementos para deformar o desenho.
ESCALA_CORPO = 0.62
ESCALA_OLHO, ESCALA_PUPILA = 0.085, 0.040
CENTRO_OLHO = (0.17, 0.20)  # afastamento do eixo e altura de cada olho

# Até onde a pupila pode sair do centro do olho, sem escapar do branco.
LIMITE_OLHAR = ESCALA_OLHO - ESCALA_PUPILA
PASSO_OLHAR = LIMITE_OLHAR / 2.0


def leque(x, y):
    """Empacota uma curva fechada como TRIANGLE_FAN."""
    x = np.concatenate(([0.0], x, [x[0]]))
    y = np.concatenate(([0.0], y, [y[0]]))
    return np.column_stack((x, y, np.zeros_like(x), np.ones_like(x))).astype("f4")


def curva_coracao(n=180):
    # Aumente ou diminua n para refinar o contorno do coração.
    t = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)
    x = 16.0 * np.sin(t) ** 3
    y = 13.0 * np.cos(t) - 5.0 * np.cos(2 * t) - 2.0 * np.cos(3 * t) - np.cos(4 * t)
    y = y - 0.5 * (y.max() + y.min())  # centra a curva na origem
    return leque(x / 17.0, y / 17.0)  # normaliza para caber em [-1, 1]


def curva_circulo(n=48):
    # Ajuste o número de lados do círculo para aumentar ou reduzir a suavidade.
    t = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)
    return leque(np.cos(t), np.sin(t))


def erro_glfw(codigo, descricao):
    """Substitui o aviso padrão do pyGLFW: imprime código e descrição em stderr."""
    print(f"GLFW [{codigo}]: {descricao}", file=sys.stderr)


glfw.set_error_callback(erro_glfw)

if not glfw.init():
    sys.exit("FALHA: glfw não inicializou")

glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 0)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)
glfw.window_hint(glfw.SAMPLES, 4)
glfw.window_hint(glfw.RESIZABLE, False)

# Ajuste a resolução e o nome da janela para personalizar a apresentação.
janela = glfw.create_window(640, 640, "Senhor Coração", None, None)
if not janela:
    glfw.terminate()
    sys.exit("FALHA: não foi possível criar a janela")

glfw.make_context_current(janela)
ctx = moderngl.create_context()

print(f"amostras por pixel obtidas: {ctx.screen.samples}")

prog = ctx.program(
    vertex_shader=(SHADERS / "senhor_coracao.vert").read_text(encoding="utf-8"),
    fragment_shader=(SHADERS / "senhor_coracao.frag").read_text(encoding="utf-8"),
)


def montar(vertices):
    vbo = ctx.buffer(vertices.tobytes())
    return vbo, ctx.vertex_array(prog, [(vbo, "4f", "vPosition")])


vbo_coracao, vao_coracao = montar(curva_coracao())
vbo_circulo, vao_circulo = montar(curva_circulo())

# Todo o estado do programa cabe em dois números e um booleano.
olhar_x, olhar_y = 0.0, 0.0
noite = False


def tecla(window, key, scancode, action, mods):
    global olhar_x, olhar_y, noite
    if action != glfw.PRESS and action != glfw.REPEAT:
        return
    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
    elif key == glfw.KEY_D:
        # Tecla D: troca entre tema dia/noite.
        noite = not noite
    elif key in (glfw.KEY_LEFT, glfw.KEY_RIGHT, glfw.KEY_UP, glfw.KEY_DOWN):
        # Ajuste os valores do passo para mover a pupila com mais/menos velocidade.
        dx = {glfw.KEY_LEFT: -1.0, glfw.KEY_RIGHT: 1.0}.get(key, 0.0)
        dy = {glfw.KEY_DOWN: -1.0, glfw.KEY_UP: 1.0}.get(key, 0.0)
        olhar_x += dx * PASSO_OLHAR
        olhar_y += dy * PASSO_OLHAR

        distancia = (olhar_x ** 2 + olhar_y ** 2) ** 0.5
        if distancia > LIMITE_OLHAR:
            # Limita o movimento da pupila para não sair do círculo do olho.
            olhar_x *= LIMITE_OLHAR / distancia
            olhar_y *= LIMITE_OLHAR / distancia


glfw.set_key_callback(janela, tecla)


def ajustar(nome, valor):
    """Escreve num uniforme, se ele existir."""
    uniforme = prog.get(nome, None)
    if uniforme is not None:
        uniforme.value = valor


def desenhar(vao, escala, deslocamento, cor):
    """Carrega os três uniformes daquele desenho e dispara a chamada."""
    # Aqui você pode trocar o valor de escala, deslocamento e cor para criar variações.
    ajustar("u_escala", escala)
    ajustar("u_deslocamento", deslocamento)
    ajustar("u_cor", cor)
    vao.render(moderngl.TRIANGLE_FAN)


while not glfw.window_should_close(janela):
    # Ajuste a intensidade de 'u_atenuacao' para deixar o tema mais escuro ou claro.
    ajustar("u_atenuacao", 0.35 if noite else 1.0)
    # Troque o fundo aqui para alterar o visual geral do cenário.
    ctx.clear(*(FUNDO_NOITE if noite else FUNDO_DIA))

    desenhar(vao_coracao, ESCALA_CORPO, (0.0, 0.0), MAGENTA)

    for lado in (-1.0, 1.0):
        centro = (lado * CENTRO_OLHO[0], CENTRO_OLHO[1])
        # Ajuste a posição central dos olhos e o tamanho de cada círculo.
        desenhar(vao_circulo, ESCALA_OLHO, centro, BRANCO_OLHO)
        desenhar(vao_circulo, ESCALA_PUPILA, (centro[0] + olhar_x, centro[1] + olhar_y), PRETO)

    glfw.swap_buffers(janela)
    glfw.poll_events()

for recurso in (vao_coracao, vao_circulo, vbo_coracao, vbo_circulo, prog):
    recurso.release()

glfw.terminate()
print("Execução finalizada.")
