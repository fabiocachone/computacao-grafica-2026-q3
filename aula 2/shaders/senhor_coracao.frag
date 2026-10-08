#version 330 core
uniform vec4 u_cor;
uniform float u_atenuacao;
out vec4 fColor;

void main() {
    fColor = u_cor * u_atenuacao;
}
