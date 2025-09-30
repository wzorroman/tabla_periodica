import unicodedata
import requests
import os
import json
from urllib.parse import urlparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Datos de los elementos (copiados de tu JavaScript)
elements = [
    { "number": 1, "symbol": "H", "name": "Hidrógeno", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_001_hydrogen/element_001_hydrogen.glb" },
    { "number": 2, "symbol": "He", "name": "Helio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_002_helium/element_002_helium.glb"},
    { "number": 3, "symbol": "Li", "name": "Litio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_003_lithium/element_003_lithium.glb" },
    { "number": 4, "symbol": "Be", "name": "Berilio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_004_beryllium/element_004_beryllium.glb" },
    { "number": 5, "symbol": "B", "name": "Boro", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_005_boron/element_005_boron.glb" },
    { "number": 6, "symbol": "C", "name": "Carbono", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_006_carbon/element_006_carbon.glb"  },
    { "number": 7, "symbol": "N", "name": "Nitrógeno", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_007_nitrogen/element_007_nitrogen.glb"  },
    { "number": 8, "symbol": "O", "name": "Oxígeno", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_008_oxygen/element_008_oxygen.glb" },
    { "number": 9, "symbol": "F", "name": "Flúor", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_009_fluorine/element_009_fluorine.glb" },
    { "number": 10, "symbol": "Ne", "name": "Neón", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_010_neon/element_010_neon.glb" },
    { "number": 11, "symbol": "Na", "name": "Sodio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_011_sodium/element_011_sodium.glb" },
    { "number": 12, "symbol": "Mg", "name": "Magnesio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_012_magnesium/element_012_magnesium.glb" },
    { "number": 13, "symbol": "Al", "name": "Aluminio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_013_aluminum/element_013_aluminum.glb" },
    { "number": 14, "symbol": "Si", "name": "Silicio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_014_silicon/element_014_silicon.glb" },
    { "number": 15, "symbol": "P", "name": "Fósforo", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_015_phosphorus/element_015_phosphorus.glb" },
    { "number": 16, "symbol": "S", "name": "Azufre", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_016_sulfur/element_016_sulfur.glb" },
    { "number": 17, "symbol": "Cl", "name": "Cloro", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_017_chlorine/element_017_chlorine.glb" },
    { "number": 18, "symbol": "Ar", "name": "Argón", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_018_argon/element_018_argon.glb" },
    { "number": 19, "symbol": "K", "name": "Potasio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_019_potassium/element_019_potassium.glb" },
    { "number": 20, "symbol": "Ca", "name": "Calcio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_020_calcium/element_020_calcium.glb" },
    { "number": 21, "symbol": "Sc", "name": "Escandio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_021_scandium/element_021_scandium.glb" },
    { "number": 22, "symbol": "Ti", "name": "Titanio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_022_titanium/element_022_titanium.glb"  },
    { "number": 23, "symbol": "V", "name": "Vanadio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_023_vanadium/element_023_vanadium.glb"  },
    { "number": 24, "symbol": "Cr", "name": "Cromo", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_024_chromium/element_024_chromium.glb"  },
    { "number": 25, "symbol": "Mn", "name": "Manganeso", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_025_manganese/element_025_manganese.glb"  },
    { "number": 26, "symbol": "Fe", "name": "Hierro", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_026_iron/element_026_iron.glb"  },
    { "number": 27, "symbol": "Co", "name": "Cobalto", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_027_cobalt/element_027_cobalt.glb"  },
    { "number": 28, "symbol": "Ni", "name": "Níquel", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_028_nickel/element_028_nickel.glb"  },
    { "number": 29, "symbol": "Cu", "name": "Cobre", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_029_copper/element_029_copper.glb"  },
    { "number": 30, "symbol": "Zn", "name": "Zinc", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_030_zinc/element_030_zinc.glb"  },
    { "number": 31, "symbol": "Ga", "name": "Galio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_031_gallium/element_031_gallium.glb" },
    { "number": 32, "symbol": "Ge", "name": "Germanio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_032_germanium/element_032_germanium.glb" },
    { "number": 33, "symbol": "As", "name": "Arsénico", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_033_arsenic/element_033_arsenic.glb" },
    { "number": 34, "symbol": "Se", "name": "Selenio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_034_selenium/element_034_selenium.glb" },
    { "number": 35, "symbol": "Br", "name": "Bromo", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_035_bromine/element_035_bromine.glb" },
    { "number": 36, "symbol": "Kr", "name": "Kriptón", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_036_krypton/element_036_krypton.glb" },
    { "number": 37, "symbol": "Rb", "name": "Rubidio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_037_rubidium/element_037_rubidium.glb" },
    { "number": 38, "symbol": "Sr", "name": "Estroncio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_038_strontium/element_038_strontium.glb" },
    { "number": 39, "symbol": "Y", "name": "Itrio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_039_yttrium/element_039_yttrium.glb" },
    { "number": 40, "symbol": "Zr", "name": "Circonio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_040_zirconium/element_040_zirconium.glb" },
    { "number": 41, "symbol": "Nb", "name": "Niobio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_041_niobium/element_041_niobium.glb" },
    { "number": 42, "symbol": "Mo", "name": "Molibdeno", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_042_molybdenum/element_042_molybdenum.glb" },
    { "number": 43, "symbol": "Tc", "name": "Tecnecio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_043_technetium/element_043_technetium.glb" },
    { "number": 44, "symbol": "Ru", "name": "Rutenio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_044_ruthenium/element_044_ruthenium.glb" },
    { "number": 45, "symbol": "Rh", "name": "Rodio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_045_rhodium/element_045_rhodium.glb" },
    { "number": 46, "symbol": "Pd", "name": "Paladio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_046_palladium/element_046_palladium.glb" },
    { "number": 47, "symbol": "Ag", "name": "Plata", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_047_silver/element_047_silver.glb" },
    { "number": 48, "symbol": "Cd", "name": "Cadmio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_048_cadmium/element_048_cadmium.glb" },
    { "number": 49, "symbol": "In", "name": "Indio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_049_indium/element_049_indium.glb" },
    { "number": 50, "symbol": "Sn", "name": "Estaño", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_050_tin/element_050_tin.glb" },
    { "number": 51, "symbol": "Sb", "name": "Antimonio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_051_antimony/element_051_antimony.glb" },
    { "number": 52, "symbol": "Te", "name": "Telurio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_052_tellurium/element_052_tellurium.glb" },
    { "number": 53, "symbol": "I", "name": "Yodo", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_053_iodine/element_053_iodine.glb" },
    { "number": 54, "symbol": "Xe", "name": "Xenón", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_054_xenon/element_054_xenon.glb" },
    { "number": 55, "symbol": "Cs", "name": "Cesio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_055_cesium/element_055_cesium.glb"  },
    { "number": 56, "symbol": "Ba", "name": "Bario", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_056_barium/element_056_barium.glb" },
    { "number": 57, "symbol": "La", "name": "Lantano", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_057_lanthanum/element_057_lanthanum.glb" },
    { "number": 58, "symbol": "Ce", "name": "Cerio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_058_cerium/element_058_cerium.glb" },
    { "number": 59, "symbol": "Pr", "name": "Praseodimio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_059_praseodymium/element_059_praseodymium.glb" },
    { "number": 60, "symbol": "Nd", "name": "Neodimio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_060_neodymium/element_060_neodymium.glb"  },
    { "number": 61, "symbol": "Pm", "name": "Prometio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_061_promethium/element_061_promethium.glb"  },
    { "number": 62, "symbol": "Sm", "name": "Samario", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_062_samarium/element_062_samarium.glb"  },
    { "number": 63, "symbol": "Eu", "name": "Europio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_063_europium/element_063_europium.glb"  },
    { "number": 64, "symbol": "Gd", "name": "Gadolinio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_064_gadolinium/element_064_gadolinium.glb"  },
    { "number": 65, "symbol": "Tb", "name": "Terbio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_065_terbium/element_065_terbium.glb"  },
    { "number": 66, "symbol": "Dy", "name": "Disprosio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_066_dysprosium/element_066_dysprosium.glb"  },
    { "number": 67, "symbol": "Ho", "name": "Holmio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_067_holmium/element_067_holmium.glb"  },
    { "number": 68, "symbol": "Er", "name": "Erbio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_068_erbium/element_068_erbium.glb"  },
    { "number": 69, "symbol": "Tm", "name": "Tulio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_069_thulium/element_069_thulium.glb"  },
    { "number": 70, "symbol": "Yb", "name": "Iterbio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_070_ytterbium/element_070_ytterbium.glb"  },
    { "number": 71, "symbol": "Lu", "name": "Lutecio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_071_lutetium/element_071_lutetium.glb"  },
    { "number": 72, "symbol": "Hf", "name": "Hafnio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_072_hafnium/element_072_hafnium.glb"  },
    { "number": 73, "symbol": "Ta", "name": "Tantalio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_073_tantalum/element_073_tantalum.glb"  },
    { "number": 74, "symbol": "W", "name": "Wolframio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_074_tungsten/element_074_tungsten.glb"  },
    { "number": 75, "symbol": "Re", "name": "Renio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_075_rhenium/element_075_rhenium.glb"  },
    { "number": 76, "symbol": "Os", "name": "Osmio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_076_osmium/element_076_osmium.glb"  },
    { "number": 77, "symbol": "Ir", "name": "Iridio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_077_iridium/element_077_iridium.glb"  },
    { "number": 78, "symbol": "Pt", "name": "Platino", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_078_platinum/element_078_platinum.glb"  },
    { "number": 79, "symbol": "Au", "name": "Oro", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_079_gold/element_079_gold.glb"  },
    { "number": 80, "symbol": "Hg", "name": "Mercurio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_080_mercury/element_080_mercury.glb"  },
    { "number": 81, "symbol": "Tl", "name": "Talio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_081_thallium/element_081_thallium.glb"  },
    { "number": 82, "symbol": "Pb", "name": "Plomo", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_082_lead/element_082_lead.glb"  },
    { "number": 83, "symbol": "Bi", "name": "Bismuto", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_083_bismuth/element_083_bismuth.glb"  },
    { "number": 84, "symbol": "Po", "name": "Polonio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_084_polonium/element_084_polonium.glb"  },
    { "number": 85, "symbol": "At", "name": "Astato", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_085_astatine/element_085_astatine.glb"  },
    { "number": 86, "symbol": "Rn", "name": "Radón", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_086_radon/element_086_radon.glb"  },
    { "number": 87, "symbol": "Fr", "name": "Francio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_087_francium/element_087_francium.glb"  },
    { "number": 88, "symbol": "Ra", "name": "Radio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_088_radium/element_088_radium.glb"  },
    { "number": 89, "symbol": "Ac", "name": "Actinio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_089_actinium/element_089_actinium.glb"  },
    { "number": 90, "symbol": "Th", "name": "Torio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_090_thorium/element_090_thorium.glb"  },
    { "number": 91, "symbol": "Pa", "name": "Protactinio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_091_protactinium/element_091_protactinium.glb"  },
    { "number": 92, "symbol": "U", "name": "Uranio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_092_uranium/element_092_uranium.glb"  },
    { "number": 93, "symbol": "Np", "name": "Neptunio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_093_neptunium/element_093_neptunium.glb"  },
    { "number": 94, "symbol": "Pu", "name": "Plutonio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_094_plutonium/element_094_plutonium.glb"  },
    { "number": 95, "symbol": "Am", "name": "Americio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_095_americium/element_095_americium.glb"  },
    { "number": 96, "symbol": "Cm", "name": "Curio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_096_curium/element_096_curium.glb"  },
    { "number": 97, "symbol": "Bk", "name": "Berkelio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_097_berkelium/element_097_berkelium.glb"  },
    { "number": 98, "symbol": "Cf", "name": "Californio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_098_californium/element_098_californium.glb"  },
    { "number": 99, "symbol": "Es", "name": "Einstenio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_099_einsteinium/element_099_einsteinium.glb"  },
    { "number": 100, "symbol": "Fm", "name": "Fermio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_100_fermium/element_100_fermium.glb"  },
    { "number": 101, "symbol": "Md", "name": "Mendelevio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_101_mendelevium/element_101_mendelevium.glb"  },
    { "number": 102, "symbol": "No", "name": "Nobelio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_102_nobelium/element_102_nobelium.glb"  },
    { "number": 103, "symbol": "Lr", "name": "Lawrencio", "model3d": "https://storage.googleapis.com/search-ar-edu/periodic-table/element_103_lawrencium/element_103_lawrencium.glb"  }
]

def crear_directorio_modelos():
    """Crea el directorio para almacenar los modelos 3D"""
    directorio = "modelos_3d"
    if not os.path.exists(directorio):
        os.makedirs(directorio)
        print(f"📁 Directorio '{directorio}' creado")
    return directorio

def descargar_modelo(elemento, directorio, session):
    """Descarga un modelo 3D individual"""
    if not elemento["model3d"] or elemento["model3d"].strip() == "":
        return f"❌ {elemento['symbol']}: No tiene URL de modelo 3D", False
    
    url = elemento["model3d"]
    
    # Generar nombre de archivo
    nombre_ele = eliminar_tildes(elemento['name'].lower())
    nombre_archivo = f"element_{elemento['number']:03d}_{nombre_ele}.glb"
    ruta_archivo = os.path.join(directorio, nombre_archivo)
    
    # Verificar si el archivo ya existe
    if os.path.exists(ruta_archivo):
        tamaño = os.path.getsize(ruta_archivo)
        return f"✅ {elemento['symbol']}: Ya existe ({tamaño/1024:.1f} KB)", True
    
    try:
        # Descargar el archivo
        respuesta = session.get(url, stream=True, timeout=30)
        respuesta.raise_for_status()
        
        # Guardar el archivo
        with open(ruta_archivo, 'wb') as archivo:
            for chunk in respuesta.iter_content(chunk_size=8192):
                if chunk:
                    archivo.write(chunk)
        
        tamaño = os.path.getsize(ruta_archivo)
        return f"✅ {elemento['symbol']}: Descargado ({tamaño/1024:.1f} KB)", True
    
    except requests.exceptions.RequestException as e:
        return f"❌ {elemento['symbol']}: Error - {str(e)}", False
    except Exception as e:
        return f"❌ {elemento['symbol']}: Error inesperado - {str(e)}", False

def descargar_modelos_paralelo(max_workers=5):
    """Descarga todos los modelos en paralelo"""
    directorio = crear_directorio_modelos()
    
    print("🚀 Iniciando descarga de modelos 3D...")
    print(f"📊 Total de elementos: {len(elements)}")
    print(f"🔗 Descargando en paralelo con {max_workers} hilos")
    print("-" * 50)
    
    elementos_con_modelo = [e for e in elements if e["model3d"] and e["model3d"].strip() != ""]
    elementos_sin_modelo = [e for e in elements if not e["model3d"] or e["model3d"].strip() == ""]
    
    print(f"📥 Elementos con modelo: {len(elementos_con_modelo)}")
    print(f"🚫 Elementos sin modelo: {len(elementos_sin_modelo)}")
    
    # Crear sesión para reutilizar conexiones
    with requests.Session() as session:
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Descargar en paralelo
        exitosos = 0
        fallidos = 0
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Enviar todas las tareas
            futuros = {
                executor.submit(descargar_modelo, elemento, directorio, session): elemento 
                for elemento in elementos_con_modelo
            }
            
            # Procesar resultados conforme se completan
            for futuro in as_completed(futuros):
                elemento = futuros[futuro]
                try:
                    mensaje, exito = futuro.result()
                    print(mensaje)
                    if exito:
                        exitosos += 1
                    else:
                        fallidos += 1
                except Exception as e:
                    print(f"❌ {elemento['symbol']}: Error en el futuro - {str(e)}")
                    fallidos += 1
        
        # Mostrar resumen
        print("-" * 50)
        print("📊 RESUMEN DE DESCARGA:")
        print(f"✅ Descargas exitosas: {exitosos}")
        print(f"❌ Descargas fallidas: {fallidos}")
        print(f"🚫 Sin modelo disponible: {len(elementos_sin_modelo)}")
        print(f"💾 Directorio: {os.path.abspath(directorio)}")
        
        # Guardar lista de elementos sin modelo
        if elementos_sin_modelo:
            with open(os.path.join(directorio, "elementos_sin_modelo.txt"), "w", encoding="utf-8") as f:
                f.write("Elementos sin modelo 3D disponible:\n")
                for elemento in elementos_sin_modelo:
                    f.write(f"{elemento['number']:3d}. {elemento['symbol']} - {elemento['name']}\n")

def descargar_modelos_secuencial():
    """Descarga todos los modelos de forma secuencial (más lento pero más estable)"""
    directorio = crear_directorio_modelos()
    
    print("🚀 Iniciando descarga secuencial de modelos 3D...")
    print(f"📊 Total de elementos: {len(elements)}")
    print("-" * 50)
    
    exitosos = 0
    fallidos = 0
    
    with requests.Session() as session:
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        for elemento in elements:
            if not elemento["model3d"] or elemento["model3d"].strip() == "":
                print(f"🚫 {elemento['symbol']}: No tiene modelo disponible")
                continue
            
            mensaje, exito = descargar_modelo(elemento, directorio, session)
            print(mensaje)
            
            if exito:
                exitosos += 1
            else:
                fallidos += 1
            
            # Pequeña pausa entre descargas para no sobrecargar el servidor
            time.sleep(0.5)
    
    print("-" * 50)
    print(f"📊 RESUMEN: {exitosos} exitosos, {fallidos} fallidos")

def eliminar_tildes(texto):
    """Elimina tildes y caracteres especiales del texto"""
    texto = texto.replace('ñ', 'n').replace('Ñ', 'N')
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    return texto

def generar_archivo_json():
    """Genera un archivo JSON con la información actualizada de los modelos locales"""
    directorio = "modelos_3d"
    datos_actualizados = []
    
    for elemento in elements:
        elemento_actualizado = elemento.copy()
        
        # Verificar si existe el modelo local
        nombre_ele = eliminar_tildes(elemento['name'].lower())
        nombre_archivo = f"element_{elemento['number']:03d}_{nombre_ele}.glb"
        ruta_local = os.path.join(directorio, nombre_archivo)
        
        if os.path.exists(ruta_local):
            # Usar ruta local relativa
            elemento_actualizado["model3d_local"] = f"modelos_3d/{nombre_archivo}"
        else:
            elemento_actualizado["model3d_local"] = None
        
        datos_actualizados.append(elemento_actualizado)
    
    with open("elementos_con_modelos_locales.json", "w", encoding="utf-8") as f:
        json.dump(datos_actualizados, f, indent=2, ensure_ascii=False)
    
    print("📄 Archivo JSON generado: 'elementos_con_modelos_locales.json'")

if __name__ == "__main__":
    print("🔬 DESCARGADOR DE MODELOS 3D DE LA TABLA PERIÓDICA")
    print("=" * 60)
    
    while True:
        print("\nSelecciona el modo de descarga:")
        print("1. Descarga paralela (rápida)")
        print("2. Descarga secuencial (estable)")
        print("3. Solo generar archivo JSON")
        print("4. Salir")
        
        opcion = input("\nIngresa tu opción (1-4): ").strip()
        
        if opcion == "1":
            try:
                workers = int(input("Número de hilos paralelos (recomendado: 3-10): ") or "5")
                descargar_modelos_paralelo(workers)
                generar_archivo_json()
            except ValueError:
                print("❌ Número inválido, usando valor por defecto (5)")
                descargar_modelos_paralelo(5)
                generar_archivo_json()
        
        elif opcion == "2":
            descargar_modelos_secuencial()
            generar_archivo_json()
        
        elif opcion == "3":
            generar_archivo_json()
        
        elif opcion == "4":
            print("👋 ¡Hasta luego!")
            break
        
        else:
            print("❌ Opción inválida. Por favor, selecciona 1-4.")
        
        input("\nPresiona Enter para continuar...")