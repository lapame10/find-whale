#!/usr/bin/env python3
"""Actualiza los sitios que todavia usaban el 'modo' viejo (volar/seguir)
al sistema nuevo de roles (piloto/retrieval/watcher), y hace que la app
pinte a cada uno segun su rol.

Pam: 'lo que me hace falta es que pueda haber varios pilotos o no pilotos a
la vez'.
"""

RUTA = '/Users/lapame10/.hermes/workspace/find-whale/index.html'
s = open(RUTA, encoding='utf-8').read()
antes = s

cambios = [
    # 1) el latido del GPS: mando el rol, no el modo
    ("      nombre: yo.nombre, color: yo.color, modo: yo.modo,",
     "      nombre: yo.nombre, color: yo.color, rol: yo.rol,"),

    # 2) al cambiar de estado
    ("  late({ nombre:yo.nombre, color:yo.color, modo:yo.modo, estado:nuevo,",
     "  late({ nombre:yo.nombre, color:yo.color, rol:yo.rol, estado:nuevo,"),

    # 3) el wake lock solo para el que vuela
    ("    if (yo && yo.modo === 'volar'){",
     "    if (yo && yo.rol === 'piloto'){"),
    ("  if (document.visibilityState === 'visible' && yo && yo.modo === 'volar'){",
     "  if (document.visibilityState === 'visible' && yo && yo.rol === 'piloto'){"),
    ("  if (yo && yo.modo === 'volar' && document.visibilityState === 'visible'",
     "  if (yo && yo.rol === 'piloto' && document.visibilityState === 'visible'"),

    # 4) los botones de la portada
    ("$('bVolar').onclick = () => entra('volar');",
     "$('bVolar').onclick = () => entra(rolElegido(), '');        /* sala nueva */"),
    ("""$('bSeguir').onclick = () => {
  const cod = ($('miCodigo').value || '').toUpperCase().trim();
  entra('seguir', cod);
};""",
     ""),
    ("""$('bUnir').onclick = () => {
  const cod = ($('miCodigo').value || '').toUpperCase().trim();
  if (cod.length !== 4){ $('e1').textContent = 'Escribe las 4 letras del código.'; return; }
  entra('seguir', cod);
};""",
     """$('bUnir').onclick = () => {
  const cod = ($('miCodigo').value || '').toUpperCase().trim();
  if (cod.length !== 4){ $('e1').textContent = 'Escribe las 4 letras del código.'; return; }
  entra(rolElegido(), cod);
};
/* los tres botones de rol */
document.querySelectorAll('#misRoles .rol').forEach(b => {
  b.onclick = () => {
    document.querySelectorAll('#misRoles .rol').forEach(x => x.classList.remove('on'));
    b.classList.add('on');
  };
});"""),

    # 5) el auto-arranque al recargar
    ("""    yo = prev; miEstado = 'vuelo';
    arranca(prev.modo === 'volar');""",
     """    yo = prev;
    if (!yo.rol) yo.rol = (yo.modo === 'seguir') ? 'watcher' : 'piloto';   /* compatibilidad */
    miEstado = (yo.rol === 'retrieval') ? 'retrieval' : 'vuelo';
    arranca();"""),
]

for viejo, nuevo in cambios:
    if viejo not in s:
        print('  NO ENCUENTRO:', viejo[:70].replace('\n', ' | '))
    else:
        s = s.replace(viejo, nuevo)
        print('  OK:', viejo[:60].replace('\n', ' | '))

open(RUTA, 'w', encoding='utf-8').write(s)
print()
print('  antes:', len(antes), ' -> ahora:', len(s))
