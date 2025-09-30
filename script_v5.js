const periodicTable = document.getElementById('periodic-table');
const lanthanideActinideBlock = document.getElementById('lanthanides-actinides-block');
const searchBar = document.getElementById('search-bar');

const positions = {
    1: { row: 1, col: 1 }, 2: { row: 1, col: 18 },
    3: { row: 2, col: 1 }, 4: { row: 2, col: 2 }, 5: { row: 2, col: 13 }, 6: { row: 2, col: 14 }, 7: { row: 2, col: 15 }, 8: { row: 2, col: 16 }, 9: { row: 2, col: 17 }, 10: { row: 2, col: 18 },
    11: { row: 3, col: 1 }, 12: { row: 3, col: 2 }, 13: { row: 3, col: 13 }, 14: { row: 3, col: 14 }, 15: { row: 3, col: 15 }, 16: { row: 3, col: 16 }, 17: { row: 3, col: 17 }, 18: { row: 3, col: 18 },
    19: { row: 4, col: 1 }, 20: { row: 4, col: 2 }, 21: { row: 4, col: 3 }, 22: { row: 4, col: 4 }, 23: { row: 4, col: 5 }, 24: { row: 4, col: 6 }, 25: { row: 4, col: 7 }, 26: { row: 4, col: 8 }, 27: { row: 4, col: 9 }, 28: { row: 4, col: 10 }, 29: { row: 4, col: 11 }, 30: { row: 4, col: 12 }, 31: { row: 4, col: 13 }, 32: { row: 4, col: 14 }, 33: { row: 4, col: 15 }, 34: { row: 4, col: 16 }, 35: { row: 4, col: 17 }, 36: { row: 4, col: 18 },
    37: { row: 5, col: 1 }, 38: { row: 5, col: 2 }, 39: { row: 5, col: 3 }, 40: { row: 5, col: 4 }, 41: { row: 5, col: 5 }, 42: { row: 5, col: 6 }, 43: { row: 5, col: 7 }, 44: { row: 5, col: 8 }, 45: { row: 5, col: 9 }, 46: { row: 5, col: 10 }, 47: { row: 5, col: 11 }, 48: { row: 5, col: 12 }, 49: { row: 5, col: 13 }, 50: { row: 5, col: 14 }, 51: { row: 5, col: 15 }, 52: { row: 5, col: 16 }, 53: { row: 5, col: 17 }, 54: { row: 5, col: 18 },
    55: { row: 6, col: 1 }, 56: { row: 6, col: 2 }, 57: { row: 6, col: 3 }, 72: { row: 6, col: 4 }, 73: { row: 6, col: 5 }, 74: { row: 6, col: 6 }, 75: { row: 6, col: 7 }, 76: { row: 6, col: 8 }, 77: { row: 6, col: 9 }, 78: { row: 6, col: 10 }, 79: { row: 6, col: 11 }, 80: { row: 6, col: 12 }, 81: { row: 6, col: 13 }, 82: { row: 6, col: 14 }, 83: { row: 6, col: 15 }, 84: { row: 6, col: 16 }, 85: { row: 6, col: 17 }, 86: { row: 6, col: 18 },
    87: { row: 7, col: 1 }, 88: { row: 7, col: 2 }, 89: { row: 7, col: 3 }, 104: { row: 7, col: 4 }, 105: { row: 7, col: 5 }, 106: { row: 7, col: 6 }, 107: { row: 7, col: 7 }, 108: { row: 7, col: 8 }, 109: { row: 7, col: 9 }, 110: { row: 7, col: 10 }, 111: { row: 7, col: 11 }, 112: { row: 7, col: 12 }, 113: { row: 7, col: 13 }, 114: { row: 7, col: 14 }, 115: { row: 7, col: 15 }, 116: { row: 7, col: 16 }, 117: { row: 7, col: 17 }, 118: { row: 7, col: 18 }
};

const lanthanideActinidePositions = {
    57: { row: 1, col: 3 }, 
    58: { row: 1, col: 4 }, 
    59: { row: 1, col: 5 }, 
    60: { row: 1, col: 6 }, 
    61: { row: 1, col: 7 }, 
    62: { row: 1, col: 8 }, 
    63: { row: 1, col: 9 }, 
    64: { row: 1, col: 10 }, 
    65: { row: 1, col: 11 }, 
    66: { row: 1, col: 12 }, 
    67: { row: 1, col: 13 }, 
    68: { row: 1, col: 14 }, 
    69: { row: 1, col: 15 }, 
    70: { row: 1, col: 16 }, 
    71: { row: 1, col: 17 },
    89: { row: 2, col: 3 }, 90: { row: 2, col: 4 }, 91: { row: 2, col: 5 }, 92: { row: 2, col: 6 }, 93: { row: 2, col: 7 }, 94: { row: 2, col: 8 }, 95: { row: 2, col: 9 }, 96: { row: 2, col: 10 }, 97: { row: 2, col: 11 }, 98: { row: 2, col: 12 }, 99: { row: 2, col: 13 }, 100: { row: 2, col: 14 }, 101: { row: 2, col: 15 }, 102: { row: 2, col: 16 }, 103: { row: 2, col: 17 }
};

// ===== VARIABLES DEL POPUP REFACTORIZADAS =====
const popup = document.getElementById('element-popup');
const popupElementSymbol = document.getElementById('popup-element-symbol');
const popupElementName = document.getElementById('popup-element-name');
const popupElementNumber = document.getElementById('popup-element-number');
const popupElementGroup = document.getElementById('popup-element-group');
const popupAtomModelViewer = document.getElementById('popup-atom-model');

// Elementos de estadísticas
const popupStatProtons = document.getElementById('popup-stat-protons');
const popupStatNeutrons = document.getElementById('popup-stat-neutrons');
const popupStatElectrons = document.getElementById('popup-stat-electrons');
const popupStatShells = document.getElementById('popup-stat-shells');

// Elementos de propiedades
const popupPropertyMass = document.getElementById('popup-property-mass');
const popupPropertyMelting = document.getElementById('popup-property-melting');
const popupPropertyBoiling = document.getElementById('popup-property-boiling');
const popupPropertyDensity = document.getElementById('popup-property-density');
const popupPropertyState = document.getElementById('popup-property-state');
const popupPropertyElectronegativity = document.getElementById('popup-property-electronegativity');
const popupPropertyElectronConfig = document.getElementById('popup-property-electron-config');
const popupDiscoveryInfoText = document.getElementById('popup-discovery-info-text');

const popupCloseBtn = document.querySelector('.popup-close-btn');

// ===== FUNCIONES PRINCIPALES =====
function renderElements() {
    elements.forEach(elementData => {
        const elementDiv = document.createElement('div');
        elementDiv.classList.add('element', `group-${elementData.group}`);
        elementDiv.setAttribute('data-name', elementData.name.toLowerCase());
        elementDiv.setAttribute('data-symbol', elementData.symbol.toLowerCase());
        
        // Determinar el contenedor y posición
        let container = periodicTable;
        let pos = positions[elementData.number];

        if (elementData.group === 'lantanido' || elementData.group === 'actinido') {
            container = lanthanideActinideBlock;
            pos = lanthanideActinidePositions[elementData.number];
        }

        if (pos) {
            elementDiv.style.gridRow = pos.row;
            elementDiv.style.gridColumn = pos.col;
        }

        elementDiv.innerHTML = `
            <div class="element-number">${elementData.number}</div>
            <div class="element-symbol">${elementData.symbol}</div>
            <div class="element-name">${elementData.name}</div>
        `;

        elementDiv.addEventListener('click', () => {
            showElementInfo(elementData);
        });

        container.appendChild(elementDiv);
    });
}

function showElementInfo(elementData) {
    // Actualizar información básica
    popupElementSymbol.textContent = elementData.symbol;
    popupElementName.textContent = elementData.name;
    popupElementNumber.textContent = `Número Atómico: ${elementData.number}`;
    popupElementGroup.textContent = elementData.group.replace(/-/g, ' ');
    
    // Actualizar estadísticas del átomo
    popupStatProtons.textContent = elementData.number;
    popupStatNeutrons.textContent = Math.round(elementData.mass - elementData.number);
    popupStatElectrons.textContent = elementData.number;
    
    // Calcular capas electrónicas
    const shellConfig = calculateElectronShells(elementData.electronConfig);
    popupStatShells.textContent = shellConfig;
    
    // Actualizar propiedades
    popupPropertyMass.textContent = `${elementData.mass} u`;
    popupPropertyMelting.textContent = elementData.meltingPoint ? `${elementData.meltingPoint} K` : 'Desconocido';
    popupPropertyBoiling.textContent = elementData.boilingPoint ? `${elementData.boilingPoint} K` : 'Desconocido';
    popupPropertyDensity.textContent = elementData.density ? `${elementData.density} g/cm³` : 'Desconocida';
    popupPropertyElectronConfig.textContent = elementData.electronConfig;
    
    // Determinar estado a 25°C
    const state = determineState(elementData);
    popupPropertyState.textContent = state;
    
    // Electronegatividad
    const electronegativity = getElectronegativity(elementData.number);
    popupPropertyElectronegativity.textContent = electronegativity;
    
    // Información de descubrimiento
    const discoveryInfo = getDiscoveryInfo(elementData.number);
    popupDiscoveryInfoText.innerHTML = discoveryInfo;
    
    // Cargar modelo 3D
    if (elementData.model3d && elementData.model3d.trim() !== '') {
        popupAtomModelViewer.src = elementData.model3d;
    } else {
        popupAtomModelViewer.src = '';
        // Opcional: mostrar un placeholder si no hay modelo
        console.log(`No hay modelo 3D disponible para ${elementData.name}`);
    }
    
    // Mostrar el popup
    popup.classList.add('active');
}

// ===== FUNCIONES AUXILIARES =====
function calculateElectronShells(electronConfig) {
    // Simplificación para mostrar capas electrónicas
    const config = electronConfig.replace(/\[.*?\]/g, '');
    const shells = config.match(/\d[sdpf]/g);
    if (shells) {
        return shells.map(shell => shell[0]).join('-');
    }
    return 'N/A';
}

function determineState(elementData) {
    // Simplificación para determinar estado a temperatura ambiente (298K)
    if (elementData.meltingPoint === null || elementData.boilingPoint === null) {
        return 'Desconocido';
    }
    
    if (elementData.meltingPoint < 298 && elementData.boilingPoint < 298) {
        return 'Gas';
    } else if (elementData.meltingPoint < 298) {
        return 'Líquido';
    } else {
        return 'Sólido';
    }
}

function getElectronegativity(atomicNumber) {
    // Valores de electronegatividad aproximados (Pauling)
    const electronegativities = {
        1: 2.20, 2: null, 3: 0.98, 4: 1.57, 5: 2.04, 6: 2.55, 7: 3.04, 8: 3.44, 9: 3.98, 10: null,
        11: 0.93, 12: 1.31, 13: 1.61, 14: 1.90, 15: 2.19, 16: 2.58, 17: 3.16, 18: null,
        19: 0.82, 20: 1.00, 21: 1.36, 22: 1.54, 23: 1.63, 24: 1.66, 25: 1.55, 26: 1.83, 27: 1.88, 28: 1.91,
        29: 1.90, 30: 1.65, 31: 1.81, 32: 2.01, 33: 2.18, 34: 2.55, 35: 2.96, 36: 3.00,
        // Puedes agregar más valores según necesites
    };
    const value = electronegativities[atomicNumber];
    return value ? `${value} (Pauling)` : 'Desconocida';
}

function getDiscoveryInfo(atomicNumber) {
    // Información de descubrimiento de ejemplo
    const discoveries = {
        1: 'Descubierto por: Henry Cavendish (1766)<br>Origen del nombre: Del griego "hydro" (agua) y "genes" (formador)',
        2: 'Descubierto por: Pierre Janssen (1868)<br>Origen del nombre: Del griego "helios" (sol)',
        3: 'Descubierto por: Johan August Arfwedson (1817)<br>Origen del nombre: Del griego "lithos" (piedra)',
        4: 'Descubierto por: Louis Nicolas Vauquelin (1798)<br>Origen del nombre: Del griego "beryllos" (berilo)',
        5: 'Descubierto por: Joseph Louis Gay-Lussac (1808)<br>Origen del nombre: Del árabe "buraq" (borax)',
        6: 'Conocido desde la antigüedad<br>Origen del nombre: Del latín "carbo" (carbón)',
        7: 'Descubierto por: Daniel Rutherford (1772)<br>Origen del nombre: Del griego "nitron" y "genes" (formador de nitro)',
        8: 'Descubierto por: Joseph Priestley (1774)<br>Origen del nombre: Del griego "oxy" (ácido) y "genes" (formador)',
        9: 'Descubierto por: Henri Moissan (1886)<br>Origen del nombre: Del latín "fluere" (fluir)',
        10: 'Descubierto por: William Ramsay (1898)<br>Origen del nombre: Del griego "neos" (nuevo)',
        // Puedes agregar más información según necesites
    };
    return discoveries[atomicNumber] || 'Información de descubrimiento no disponible';
}

// ===== EVENT LISTENERS =====
// Cerrar el popup al hacer clic en la X
popupCloseBtn.addEventListener('click', () => {
    popup.classList.remove('active');
});

// Cerrar el popup al hacer clic fuera del contenido
popup.addEventListener('click', (e) => {
    if (e.target === popup) {
        popup.classList.remove('active');
    }
});

// Cerrar el popup con la tecla Escape
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && popup.classList.contains('active')) {
        popup.classList.remove('active');
    }
});

// Búsqueda de elementos
searchBar.addEventListener('keyup', (e) => {
    const searchText = e.target.value.toLowerCase();
    const allElements = document.querySelectorAll('.element');

    allElements.forEach(element => {
        const elementName = element.getAttribute('data-name');
        const elementSymbol = element.getAttribute('data-symbol');
        if (elementName.includes(searchText) || elementSymbol.includes(searchText)) {
            element.classList.remove('hidden');
        } else {
            element.classList.add('hidden');
        }
    });
});

// Inicializar la tabla periódica
renderElements();