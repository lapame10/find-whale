#!/usr/bin/env python3
"""Añade el icono del coche (retrieval) y el de socorro a Find Whale."""

RUTA = '/Users/lapame10/.hermes/workspace/find-whale/index.html'

coche = open('/tmp/path_directions_car.txt').read().strip()
sos   = open('/tmp/path_sos.txt').read().strip()

s = open(RUTA, encoding='utf-8').read()

# 1) añado las dos constantes nuevas tras ICONO_PERSONA
viejo = "const ICONO_PERSONA = '"
i = s.find(viejo)
if i < 0:
    raise SystemExit('no encuentro ICONO_PERSONA')
fin_linea = s.find("';\n", i) + 3
s = s[:fin_linea] + "const ICONO_COCHE = '%s';\nconst ICONO_SOCORRO = '%s';\n" % (coche, sos) + s[fin_linea:]

# 2) reemplazo el cuerpo de iconoPiloto para que entienda recogeme y ayuda
ini = s.find('function iconoPiloto(p){')
fin = s.find('  return L.divIcon({', ini)
if ini < 0 or fin < 0:
    raise SystemExit('no encuentro el cuerpo de iconoPiloto')

nuevo = """function iconoPiloto(p){
  const col = (COLORES.find(c => c.id === p.color) || {}).c || '#888';
  const enTierra = (p.estado === 'tierra');
  const recoge   = (p.estado === 'retrieval');
  const socorro  = (p.estado === 'sos');

  /* que dibujo lleva dentro */
  let icono = ICONO_PARA;                       /* volando */
  if (recoge)        icono = ICONO_COCHE;       /* pide recogida */
  else if (socorro)  icono = ICONO_SOCORRO;     /* emergencia */
  else if (enTierra) icono = ICONO_PERSONA;     /* en el suelo */

  /* el color: el suyo, menos si pide ayuda (rojo) o recogida (naranja) */
  const colorPin = socorro ? '#c62828' : recoge ? '#e07b00' : col;

  /* forma: gota si esta en el aire, circulo si esta en el suelo */
  let cuerpo, ix, iy, ancla;
  if (enTierra && !recoge && !socorro){
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
print('  coche :', len(coche), 'chars')
print('  socorro:', len(sos), 'chars')
print('  archivo:', len(s), 'bytes')
