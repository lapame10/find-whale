#!/usr/bin/env python3
"""Pinta a cada uno segun su ROL, no solo segun su estado.

  piloto + volando  -> parapente (gota, apunta donde esta)
  piloto + tierra   -> persona
  retrieval         -> coche
  watcher/miron     -> ojo
  cualquiera + SOS  -> triangulo de socorro en rojo
"""

RUTA = '/Users/lapame10/.hermes/workspace/find-whale/index.html'
s = open(RUTA, encoding='utf-8').read()

ojo = open('/tmp/path_visibility.txt').read().strip()

# 1) añado el icono del ojo
marca = "const ICONO_SOCORRO = '"
i = s.find(marca)
if i < 0:
    raise SystemExit('no encuentro ICONO_SOCORRO')
fin = s.find("';\n", i) + 3
s = s[:fin] + "const ICONO_OJO = '%s';\n" % ojo + s[fin:]

# 2) reemplazo el cuerpo de iconoPiloto
ini = s.find('function iconoPiloto(p){')
fin = s.find('  return L.divIcon({', ini)
if ini < 0 or fin < 0:
    raise SystemExit('no encuentro iconoPiloto')

nuevo = """function iconoPiloto(p){
  const col = (COLORES.find(c => c.id === p.color) || {}).c || '#888';
  const socorro  = (p.estado === 'sos');
  const esCoche  = (p.rol === 'retrieval');
  const esMiron  = (p.rol === 'watcher');
  const enTierra = (p.estado === 'tierra') || esCoche || esMiron;

  /* que dibujo lleva dentro, por orden de importancia */
  let icono = ICONO_PARA;                          /* piloto en el aire */
  if (socorro)         icono = ICONO_SOCORRO;      /* emergencia */
  else if (esCoche)    icono = ICONO_COCHE;        /* coche de recogida */
  else if (esMiron)    icono = ICONO_OJO;          /* solo mira */
  else if (enTierra)   icono = ICONO_PERSONA;      /* aterrizo y esta bien */

  const colorPin = socorro ? '#c62828' : esCoche ? '#e07b00' : esMiron ? '#6b7f88' : col;

  /* forma: gota si esta en el aire (apunta al sitio exacto), circulo si esta
     en el suelo, en el coche o mirando */
  let cuerpo, ix, iy, ancla;
  if (enTierra){
    cuerpo = '<ellipse cx="19" cy="50" rx="13" ry="4" fill="rgba(0,0,0,.16)"/>'
           + '<circle cx="19" cy="22" r="19" fill="' + colorPin + '" stroke="#fff" stroke-width="2.6"/>';
    ix = 7; iy = 10; ancla = [19, 22];
  } else {
    cuerpo = '<path d="M19 2C10 2 3 9 3 18c0 12.5 16 28 16 28s16-15.5 16-28C35 9 28 2 19 2z"'
           + ' fill="' + colorPin + '" stroke="#fff" stroke-width="2.6"/>';
    ix = 7; iy = 6; ancla = [19, 46];
  }

"""
s = s[:ini] + nuevo + s[fin:]
open(RUTA, 'w', encoding='utf-8').write(s)
print('  ojo: %d chars' % len(ojo))
print('  archivo:', len(s), 'bytes')
