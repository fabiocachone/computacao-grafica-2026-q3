#version 330 core
in vec4 vPosition;
uniform vec2 u_deslocamento;
uniform float u_escala;

void main() {
    vec2 pos = vPosition.xy * u_escala + u_deslocamento;
    gl_Position = vec4(pos, 0.0, 1.0);
}
