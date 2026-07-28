// ============================================================
// 1. DEFINIÇÃO DOS BLOCOS
// ============================================================
const BLOCK_DEFS = [{
  action: 'navigate',
  label: 'Navegar',
  icon: '🌐',
  category: 'Navegação',
  color: '#3b82f6',
  tooltip: 'Abre uma página web. Defina a URL e aguarde o carregamento.',
  params: [
    { name: 'url', label: 'URL', type: 'text', placeholder: 'https://...', required: true },
    { name: 'wait_until', label: 'Aguardar até', type: 'select', options: ['load', 'domcontentloaded',
        'networkidle'
      ] }
  ],
  children: false
}, 

{
  action: 'monitor',
  label: 'Monitor',
  icon: '👁️',
  category: 'Monitoramento',
  color: '#0ea5e9',
  tooltip: 'Inicia um monitor em background para observar alterações em um elemento da página e executar ações quando eventos ocorrerem.',
  params: [
    {
      name: 'name',
      label: 'Nome',
      type: 'text',
      placeholder: 'Monitor Login'
    },
    {
      name: 'selector',
      label: 'Seletor CSS',
      type: 'text',
      placeholder: '#login',
      required: true,
      isSelector: true
    },
    
    {
      name: 'interval',
      label: 'Intervalo (s)',
      type: 'number',
      placeholder: '10'
    },
    {
      name: 'timeout',
      label: 'Timeout (s)',
      type: 'number',
      placeholder: '30'
    },
    {
      name: 'save_snapshots',
      label: 'Salvar histórico',
      type: 'text',
      placeholder: 'true'
    },
    {
      name: 'max_history',
      label: 'Máx. histórico',
      type: 'number',
      placeholder: '100'
    }
  ],

  children: true,

  childrenSlots: [
    //'on_start',
    //'on_found',
    'on_change',
    'on_not_found',
    //'on_error',
    //'on_stop',
    //'on_timeout'
  ]
}
,{
  action: 'fill',
  label: 'Preencher',
  icon: '✏️',
  category: 'Formulários',
  color: '#10b981',
  tooltip: 'Preenche um campo input ou textarea com o valor especificado.',
  params: [
    { name: 'selector', label: 'Seletor CSS', type: 'text', placeholder: 'input[name="email"]',
      required: true, isSelector: true },
    { name: 'value', label: 'Valor', type: 'text', placeholder: 'usuario@email.com', required: true }
  ],
  children: false
}, {
  action: 'click',
  label: 'Clicar',
  icon: '🖱️',
  category: 'Interação',
  color: '#f59e0b',
  tooltip: 'Clica em um elemento da página (botão, link, etc).',
  params: [
    { name: 'selector', label: 'Seletor CSS', type: 'text', placeholder: 'button[type="submit"]',
      required: true, isSelector: true }
  ],
  children: false
}, {
  action: 'press',
  label: 'Pressionar tecla',
  icon: '⌨️',
  category: 'Interação',
  color: '#8b5cf6',
  tooltip: 'Pressiona uma tecla em um elemento (ex: Enter em um campo de busca).',
  params: [
    { name: 'selector', label: 'Seletor CSS', type: 'text', placeholder: 'input[name="search"]',
      required: true, isSelector: true },
    { name: 'key', label: 'Tecla', type: 'select', options: ['Enter', 'Escape', 'Tab', 'Backspace',
        'Delete', 'ArrowUp', 'ArrowDown'
      ] }
  ],
  children: false
}, {
  action: 'hover',
  label: 'Pairar (hover)',
  icon: '👆',
  category: 'Interação',
  color: '#ec4899',
  tooltip: 'Move o mouse sobre um elemento (útil para menus suspensos).',
  params: [
    { name: 'selector', label: 'Seletor CSS', type: 'text', placeholder: '.menu-item', required: true,
      isSelector: true }
  ],
  children: false
}, {
  action: 'select',
  label: 'Selecionar opção',
  icon: '📋',
  category: 'Formulários',
  color: '#14b8a6',
  tooltip: 'Seleciona uma opção em um elemento &lt;select&gt;.',
  params: [
    { name: 'selector', label: 'Seletor CSS', type: 'text', placeholder: '#pais', required: true,
      isSelector: true },
    { name: 'value', label: 'Valor', type: 'text', placeholder: 'BR', required: true }
  ],
  children: false
}, {
  action: 'extract',
  label: 'Extrair dados',
  icon: '📊',
  category: 'Extrações',
  color: '#f97316',
  tooltip: 'Extrai informações da página (texto, atributo) e guarda numa variável.',
  params: [
    { name: 'selector', label: 'Seletor CSS', type: 'text', placeholder: 'h1', required: true,
      isSelector: true },
    { name: 'attribute', label: 'Atributo', type: 'select', options: ['textContent', 'href', 'src',
        'value', 'innerHTML'
      ] },
    { name: 'variable', label: 'Nome da variável', type: 'text', placeholder: 'titulo', required: true }
  ],
  children: false
}, {
  action: 'screenshot',
  label: 'Capturar tela',
  icon: '📸',
  category: 'Utilitários',
  color: '#6366f1',
  tooltip: 'Tira um screenshot da página atual e salva como arquivo.',
  params: [
    { name: 'filename', label: 'Nome do arquivo', type: 'text', placeholder: 'pagina.png' }
  ],
  children: false
}, {
  action: 'wait',
  label: 'Esperar (tempo)',
  icon: '⏳',
  category: 'Controle',
  color: '#64748b',
  tooltip: 'Aguarda um número fixo de segundos.',
  params: [
    { name: 'seconds', label: 'Segundos', type: 'number', placeholder: '3', required: true }
  ],
  children: false
}, {
  action: 'wait_for_selector',
  label: 'Esperar elemento',
  icon: '🔍',
  category: 'Controle',
  color: '#06b6d4',
  tooltip: 'Aguarda até que um elemento apareça na página.',
  params: [
    { name: 'selector', label: 'Seletor CSS', type: 'text', placeholder: '.resultado', required: true,
      isSelector: true },
    { name: 'timeout', label: 'Timeout (ms)', type: 'number', placeholder: '10000' },
    { name: 'var', label: 'Nome', type: 'text', placeholder: 'produto', required: false }
  ],
  children: false
}, {
  action: 'set',
  label: 'Definir variável',
  icon: '📦',
  category: 'Variáveis',
  color: '#84cc16',
  tooltip: 'Cria ou altera o valor de uma variável.',
  params: [
    { name: 'var', label: 'Nome', type: 'text', placeholder: 'produto', required: true },
    { name: 'value', label: 'Valor', type: 'text', placeholder: 'Notebook', required: true }
  ],
  children: false
}, {
  action: 'log',
  label: 'Registrar mensagem',
  icon: '📝',
  category: 'Utilitários',
  color: '#a3a3a3',
  tooltip: 'Exibe uma mensagem no console (útil para depuração).',
  params: [
    { name: 'message', label: 'Mensagem', type: 'text', placeholder: 'Processo iniciado', required: true }
  ],
  children: false
},{
  action: 'flow',
  label: 'Abrir fluxo',
  icon: '{ }',
  category: 'Utilitários',
  color: '#6504ed',
  tooltip: 'Abre um fluxo existente.',
  params: [
    
    { name: 'flow', label: 'Nome do fluxo', type: 'text', placeholder: 'fluxo1', required: true }
  
  ],
  children: false
}, {
  action: 'loop',
  label: 'Repetir (loop)',
  icon: '🔄',
  category: 'Estruturas',
  color: '#d946ef',
  tooltip: 'Repete um conjunto de ações várias vezes. Arraste blocos para dentro.',
  params: [
    { name: 'times', label: 'Vezes', type: 'number', placeholder: '5', required: true },
    { name: 'interval', label: 'Intervalo (s)', type: 'number', placeholder: '2' }
  ],
  
  children: true,
  childrenSlots: ['steps']
}, {
  action: 'compare',
  label: 'Condição (compare)',
  icon: '⚖️',
  category: 'Estruturas',
  color: '#ef4444',
  tooltip: 'Compara uma variável com um valor. Executa ações diferentes conforme o resultado.',
  params: [
    { name: 'var', label: 'Variável', type: 'text', placeholder: 'preco', required: true },
    { name: 'operator', label: 'Operador', type: 'select', options: ['==', '===', '!=', '>', '<',
        'contains'
      ] },
    { name: 'value', label: 'Valor', type: 'text', placeholder: '100', required: true }
  ],
  children: true,
  childrenSlots: ['on_true', 'on_false']
}, {
  action: 'notify',
  label: 'Notificar (webhook)',
  icon: '🔔',
  category: 'Integrações',
  color: '#fb923c',
  tooltip: 'Envia uma notificação via webhook (ex: Discord, Slack).',
  params: [
    { name: 'webhook', label: 'URL do webhook', type: 'text', placeholder: 'https://...', required: true },
    { name: 'payload', label: 'Payload (JSON)', type: 'text', placeholder: '{"mensagem":"OK"}' }
  ],
  children: false
}];

// ============================================================
// 2. ESTADO
// ============================================================
let blocks = [];
let nextId = 1;
let activeSelectorField = null;

const workspace = document.getElementById('workspace');
const blocksContainer = document.getElementById('blocksContainer');
const placeholder = document.getElementById('placeholder');
const paletteContainer = document.getElementById('paletteContainer');
const jsonOutput = document.getElementById('jsonOutput');

const btnSaveFlow = document.getElementById('btnSaveFlow');
const btnLoadFlow = document.getElementById('btnLoadFlow');

// Elementos do modal
const modal = document.getElementById('selectorModal');
const modalClose = document.getElementById('modalClose');
const htmlInput = document.getElementById('htmlInput');
const btnAnalyze = document.getElementById('btnAnalyze');
const btnClearInput = document.getElementById('btnClearInput');
const btnExample = document.getElementById('btnExample');
const resultsArea = document.getElementById('resultsArea');
const resultsList = document.getElementById('resultsList');

// ============================================================
// 3. RENDERIZAÇÃO DA PALETA
// ============================================================
function renderPalette() {
  const categories = {};
  BLOCK_DEFS.forEach(def => {
    if (!categories[def.category]) categories[def.category] = [];
    categories[def.category].push(def);
  });

  paletteContainer.innerHTML = '';
  for (const [cat, defs] of Object.entries(categories)) {
    const catDiv = document.createElement('div');
    catDiv.className = 'category';
    const title = document.createElement('div');
    title.className = 'category-title';
    title.textContent = cat;
    catDiv.appendChild(title);

    defs.forEach(def => {
      const el = document.createElement('div');
      el.className = 'block-palette';
      el.draggable = true;
      el.dataset.action = def.action;
      el.innerHTML = `
        <span class="icon">${def.icon}</span>
        <span class="label">${def.label}</span>
        <span class="badge">${def.action}</span>
        <span class="tooltip-text">${def.tooltip}</span>
      `;
      el.title = def.tooltip;
      el.addEventListener('dragstart', (e) => {
        e.dataTransfer.setData('text/plain', def.action);
        e.dataTransfer.effectAllowed = 'copy';
        dragState = { type: 'copy', action: def.action, blockId: null };
      });
      el.addEventListener('dragend', () => {
        cleanupDrag();
      });
      catDiv.appendChild(el);
    });
    paletteContainer.appendChild(catDiv);
  }
}

// ============================================================
// 4..1 ÁRVORE DE BLOCOS — funções auxiliares
// ============================================================
function isChildBlock(id) {
  for (const b of blocks) {
    if (b.children) {
      for (const slot in b.children) {
        if (b.children[slot].includes(id)) return true;
      }
    }
  }
  return false;
}

function findBlockById(id) {
  return blocks.find(b => b.id === id);
}

function getRootBlockIds() {
  return blocks.filter(b => !isChildBlock(b.id)).map(b => b.id);
}

function getParentInfo(blockId) {
  for (const b of blocks) {
    if (b.children) {
      for (const slot in b.children) {
        const index = b.children[slot].indexOf(blockId);
        if (index !== -1) {
          return { parentId: b.id, slotName: slot, index };
        }
      }
    }
  }
  const rootIds = getRootBlockIds();
  const rootIndex = rootIds.indexOf(blockId);
  if (rootIndex !== -1) {
    return { parentId: null, slotName: null, index: rootIndex };
  }
  return null;
}

function isDescendant(blockId, possibleAncestorId) {
  if (possibleAncestorId === null) return false;
  let parentInfo = getParentInfo(blockId);
  while (parentInfo && parentInfo.parentId !== null) {
    if (parentInfo.parentId === possibleAncestorId) return true;
    parentInfo = getParentInfo(parentInfo.parentId);
  }
  return false;
}

function getSiblingList(parentId, slotName) {
  if (parentId === null) {
    return getRootBlockIds();
  }
  return getSlotChildren(parentId, slotName);
}

function getSlotChildren(parentId, slotName) {
  const parent = findBlockById(parentId);
  if (!parent || !parent.children) return [];
  return parent.children[slotName] || [];
}

// ============================================================
// 5. ÁRVORE DE BLOCOS — reordenação centralizada
// ============================================================
function reorderTree(blockId, config) {
  const sourceInfo = getParentInfo(blockId);
  const targetInfo = config.targetBlockId ? getParentInfo(config.targetBlockId) : null;
  const targetParentId = targetInfo?.parentId ?? config.parentId ?? null;
  const targetSlotName = targetInfo?.slotName ?? config.slotName ?? null;

  let targetIndex;
  if (config.position === 'end') {
    targetIndex = getSiblingList(targetParentId, targetSlotName).length;
  } else if (config.position === 'before') {
    targetIndex = targetInfo?.index ?? 0;
  } else {
    targetIndex = (targetInfo?.index ?? -1) + 1;
  }

  if (sourceInfo?.parentId === targetParentId && sourceInfo?.slotName === targetSlotName && targetIndex > sourceInfo.index) {
    targetIndex -= 1;
  }

  if (sourceInfo) {
    removeBlockFromTree(blockId);
  }

  if (targetParentId === null) {
    moveBlockToRoot(blockId, targetIndex);
  } else {
    moveBlockToContainer(blockId, targetParentId, targetSlotName, targetIndex);
  }
}

function removeBlockFromTree(blockId) {
  const parentInfo = getParentInfo(blockId);
  if (!parentInfo) return;
  if (parentInfo.parentId === null) {
    // Blocos raiz não precisam ser removidos do array — a reordenação
    // é feita por moveBlockToRoot/moveBlockToContainer, que extraem pelo ID.
    // Remover o objeto do array aqui causa perda permanente do bloco
    // porque findBlockById não o encontra mais na etapa seguinte.
    return;
  }

  const parent = findBlockById(parentInfo.parentId);
  if (!parent || !parent.children || !parent.children[parentInfo.slotName]) return;
  parent.children[parentInfo.slotName] = parent.children[parentInfo.slotName].filter(id => id !== blockId);
}

function moveBlockToRoot(blockId, index) {
  const rootIds = getRootBlockIds().filter(id => id !== blockId);
  const safeIndex = Math.min(Math.max(index, 0), rootIds.length);
  rootIds.splice(safeIndex, 0, blockId);
  const nestedBlocks = blocks.filter(b => isChildBlock(b.id));
  blocks = rootIds.map(id => findBlockById(id)).filter(Boolean).concat(nestedBlocks);
}

function moveBlockToContainer(blockId, parentId, slotName, index) {
  const parent = findBlockById(parentId);
  if (!parent) return;
  if (!parent.children) parent.children = {};
  if (!parent.children[slotName]) parent.children[slotName] = [];

  const currentIndex = parent.children[slotName].indexOf(blockId);
  if (currentIndex !== -1) {
    parent.children[slotName].splice(currentIndex, 1);
  }

  const safeIndex = Math.min(Math.max(index, 0), parent.children[slotName].length);
  parent.children[slotName].splice(safeIndex, 0, blockId);
}

// ============================================================
// 6. CRIAÇÃO E REMOÇÃO DE BLOCOS
// ============================================================
function createBlockFromAction(action) {
  const def = BLOCK_DEFS.find(d => d.action === action);
  if (!def) return null;
  const block = {
    id: nextId++,
    action: action,
    params: {},
    children: def.children ? {} : undefined
  };
  def.params.forEach(param => {
    block.params[param.name] = '';
  });
  return block;
}

function addBlock(action) {
  const newBlock = createBlockFromAction(action);
  if (newBlock) {
    blocks.push(newBlock);
    renderBlocks();
    blocksContainer.scrollTop = blocksContainer.scrollHeight;
  }
}

function removeBlock(id) {
  blocks = blocks.filter(b => b.id !== id);
  blocks.forEach(b => {
    if (b.children) {
      for (const slot in b.children) {
        b.children[slot] = b.children[slot].filter(cid => cid !== id);
      }
    }
  });
  renderBlocks();
}

// ============================================================
// 7. RENDERIZAÇÃO DOS BLOCOS
// ============================================================
function renderBlocks() {
  blocksContainer.innerHTML = '';
  const rootBlocks = blocks.filter(b => !isChildBlock(b.id));
  if (rootBlocks.length === 0) {
    placeholder.style.display = 'block';
    return;
  }

  placeholder.style.display = 'none';
  rootBlocks.forEach(block => {
    blocksContainer.appendChild(createBlockElement(block, false));
  });
}

function createBlockElement(block, isChild) {
  const def = BLOCK_DEFS.find(d => d.action === block.action);
  if (!def) return document.createElement('div');

  const div = document.createElement('div');
  div.className = `block-instance action-${def.action}`;
  div.dataset.id = block.id;
  div.draggable = true;

  const header = document.createElement('div');
  header.className = 'block-header';
  header.innerHTML = `
    <span class="icon">${def.icon}</span>
    <span>${def.label}</span>
    <span style="font-weight:400;font-size:0.7rem;color:#94a3b8;margin-left:auto;">#${block.id}</span>
  `;
  div.appendChild(header);

  const paramsDiv = document.createElement('div');
  paramsDiv.className = 'block-params';
  def.params.forEach(param => {
    const label = document.createElement('label');
    const value = block.params[param.name] ?? '';
    let input;
    if (param.type === 'select') {
      input = document.createElement('select');
      param.options.forEach(opt => {
        const optEl = document.createElement('option');
        optEl.value = opt;
        optEl.textContent = opt;
        if (value === opt) optEl.selected = true;
        input.appendChild(optEl);
      });
    } else {
      input = document.createElement('input');
      input.type = param.type || 'text';
      input.placeholder = param.placeholder || '';
      input.value = value;
    }
    input.dataset.param = param.name;
    input.addEventListener('change', (e) => {
      block.params[param.name] = e.target.value;
    });
    label.textContent = param.label + ': ';
    label.appendChild(input);

    if (param.isSelector) {
      const helpBtn = document.createElement('button');
      helpBtn.className = 'selector-help';
      helpBtn.textContent = '🔍';
      helpBtn.title = 'Ajuda para achar o seletor';
      helpBtn.type = 'button';
      helpBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        activeSelectorField = {
          input: input,
          blockId: block.id,
          paramName: param.name
        };
        openModal();
      });
      label.appendChild(helpBtn);
    }

    paramsDiv.appendChild(label);
  });
  div.appendChild(paramsDiv);

  const removeBtn = document.createElement('button');
  removeBtn.className = 'block-remove';
  removeBtn.textContent = '✕';
  removeBtn.title = 'Remover bloco';
  removeBtn.addEventListener('click', () => {
    removeBlock(block.id);
  });
  div.appendChild(removeBtn);

  // Slots de filhos (loop, compare, etc.)
  if (def.children) {
    const childrenDiv = document.createElement('div');
    childrenDiv.className = 'block-children';
    const slots = def.childrenSlots || ['steps'];
    slots.forEach(slotName => {
      const slotDiv = document.createElement('div');
      slotDiv.className = 'block-slot';
      slotDiv.dataset.slot = slotName;
      slotDiv.dataset.parentId = block.id;

      const title = document.createElement('div');
      title.className = 'slot-title';
      title.textContent = `📦 ${slotName}`;
      slotDiv.appendChild(title);

      if (!block.children) block.children = {};
      if (!block.children[slotName]) block.children[slotName] = [];

      const childIds = block.children[slotName] || [];
      if (childIds.length === 0) {
        slotDiv.classList.add('empty');
        const hint = document.createElement('div');
        hint.className = 'slot-empty-hint';
        hint.textContent = 'Arraste blocos para dentro';
        slotDiv.appendChild(hint);
      }

      childIds.forEach((childId) => {
        const childBlock = blocks.find(b => b.id === childId);
        if (childBlock) {
          slotDiv.appendChild(createBlockElement(childBlock, true));
        }
      });

      childrenDiv.appendChild(slotDiv);
    });
    div.appendChild(childrenDiv);
  }

  // Dragstart e dragend — único listener por bloco
  div.addEventListener('dragstart', (e) => {
    e.stopPropagation(); // impede que blocos-pai capturem o evento
    e.dataTransfer.setData('text/plain', 'move:' + block.id);
    e.dataTransfer.effectAllowed = 'move';
    dragState = { type: 'move', action: null, blockId: block.id };
    // Atraso para que o browser capture o ghost antes de aplicar opacity
    requestAnimationFrame(() => {
      div.classList.add('dragging');
    });
  });

  div.addEventListener('dragend', () => {
    div.classList.remove('dragging');
    cleanupDrag();
  });

  return div;
}

// ============================================================
// 8. DRAG & DROP — Sistema centralizado
// ============================================================

// Estado do arraste
let dragState = null;     // {type: 'copy'|'move', action: string|null, blockId: number|null}
let currentDropConfig = null; // {parentId, slotName, targetBlockId, position}

// Indicador de drop (position: fixed, nunca entra no DOM flow)
const dropIndicator = document.createElement('div');
dropIndicator.className = 'drop-indicator';
document.body.appendChild(dropIndicator);

function showIndicator(rect, indent) {
  const left = (indent || rect.left) + 4;
  const width = rect.width - 8;
  dropIndicator.style.left = left + 'px';
  dropIndicator.style.width = width + 'px';
  dropIndicator.classList.add('visible');
}

function showIndicatorBefore(el) {
  const rect = el.getBoundingClientRect();
  dropIndicator.style.top = (rect.top - 2) + 'px';
  showIndicator(rect);
}

function showIndicatorAfter(el) {
  const rect = el.getBoundingClientRect();
  dropIndicator.style.top = (rect.bottom + 1) + 'px';
  showIndicator(rect);
}

function showIndicatorInsideSlot(slotEl) {
  const rect = slotEl.getBoundingClientRect();
  dropIndicator.style.top = (rect.top + rect.height / 2) + 'px';
  showIndicator(rect);
}

function hideIndicator() {
  dropIndicator.classList.remove('visible');
}

function clearSlotHighlights() {
  document.querySelectorAll('.block-slot.drag-over').forEach(el => {
    el.classList.remove('drag-over');
  });
}

function cleanupDrag() {
  hideIndicator();
  clearSlotHighlights();
  dragState = null;
  currentDropConfig = null;
}

/**
 * calcDropTarget — calcula onde o bloco será inserido baseado na posição do mouse.
 * Percorre todos os .block-instance e .block-slot visíveis usando getBoundingClientRect.
 * Retorna um config {parentId, slotName, targetBlockId, position} ou null.
 */
function calcDropTarget(mouseX, mouseY) {
  clearSlotHighlights();

  // Verifica se o ponto (mouseX, mouseY) está dentro de um retângulo
  function isInside(rect) {
    return mouseX >= rect.left && mouseX <= rect.right &&
           mouseY >= rect.top && mouseY <= rect.bottom;
  }

  // Verifica se um bloco ou seu ancestral é o bloco sendo arrastado
  function isDraggedOrDescendant(blockId) {
    if (!dragState?.blockId) return false;
    if (blockId === dragState.blockId) return true;
    return isDescendant(blockId, dragState.blockId);
  }

  /**
   * Processa recursivamente um elemento .block-instance para determinar
   * o drop target mais específico. Retorna um config ou null.
   *
   * A prioridade é:
   *   1. Se o mouse está sobre um slot filho → delegar para o slot
   *   2. Se o mouse está na zona do header do bloco → before/after no bloco
   *   3. Se o mouse está na zona dos children mas fora de qualquer slot → after no bloco
   */
  function processBlockElement(blockEl) {
    const blockId = Number(blockEl.dataset.id);

    // Ignorar o bloco sendo arrastado e seus filhos
    if (isDraggedOrDescendant(blockId)) return null;
    // Ignorar se está dentro do .dragging ghost
    if (blockEl.closest('.block-instance.dragging')) return null;

    const rect = blockEl.getBoundingClientRect();
    if (!isInside(rect)) return null;

    // --- Verificar slots de children primeiro (depth-first) ---
    const slotsContainer = blockEl.querySelector(':scope > .block-children');
    if (slotsContainer) {
      const slots = slotsContainer.querySelectorAll(':scope > .block-slot');
      for (const slot of slots) {
        const slotParentId = Number(slot.dataset.parentId);
        if (isDraggedOrDescendant(slotParentId)) continue;

        const slotRect = slot.getBoundingClientRect();
        if (!isInside(slotRect)) continue;

        // Mouse está dentro deste slot — procurar o filho mais específico
        const childBlocks = slot.querySelectorAll(':scope > .block-instance');
        let matchedChild = null;

        for (const child of childBlocks) {
          const childId = Number(child.dataset.id);
          if (isDraggedOrDescendant(childId)) continue;

          // Tentar processar recursivamente (se este filho também tem slots)
          const deepResult = processBlockElement(child);
          if (deepResult) return deepResult;

          // Verificar se o mouse está sobre este filho diretamente
          const childRect = child.getBoundingClientRect();
          if (isInside(childRect)) {
            matchedChild = child;
          }
        }

        if (matchedChild) {
          // Mouse sobre um bloco filho — calcular before/after
          const childId = Number(matchedChild.dataset.id);
          const childRect = matchedChild.getBoundingClientRect();

          // Para blocos com children, usar a zona do header para o midpoint
          const childHeader = matchedChild.querySelector(':scope > .block-header');
          const headerBottom = childHeader
            ? childHeader.getBoundingClientRect().bottom
            : childRect.top + Math.min(childRect.height / 2, 40);

          // Se o mouse está acima do meio do header → before, senão → after
          const headerMid = childRect.top + (headerBottom - childRect.top) / 2;
          const pos = mouseY < headerMid ? 'before' : 'after';

          if (pos === 'before') showIndicatorBefore(matchedChild);
          else showIndicatorAfter(matchedChild);

          return {
            parentId: slotParentId,
            slotName: slot.dataset.slot,
            targetBlockId: childId,
            position: pos
          };
        }

        // Mouse no slot mas não sobre nenhum filho visível — verificar se
        // está entre filhos (gaps) ou no espaço vazio no final do slot
        // Verificar entre filhos: encontrar o par de filhos adjacentes
        // onde o mouse está no gap
        const visibleChildren = Array.from(childBlocks).filter(c => {
          const cId = Number(c.dataset.id);
          return !isDraggedOrDescendant(cId) && !c.closest('.block-instance.dragging');
        });

        if (visibleChildren.length > 0) {
          // Mouse antes do primeiro filho?
          const firstRect = visibleChildren[0].getBoundingClientRect();
          if (mouseY < firstRect.top) {
            showIndicatorBefore(visibleChildren[0]);
            const firstId = Number(visibleChildren[0].dataset.id);
            return {
              parentId: slotParentId,
              slotName: slot.dataset.slot,
              targetBlockId: firstId,
              position: 'before'
            };
          }

          // Mouse depois do último filho?
          const lastChild = visibleChildren[visibleChildren.length - 1];
          const lastRect = lastChild.getBoundingClientRect();
          if (mouseY > lastRect.bottom) {
            slot.classList.add('drag-over');
            showIndicatorAfter(lastChild);
            return {
              parentId: slotParentId,
              slotName: slot.dataset.slot,
              targetBlockId: null,
              position: 'end'
            };
          }

          // Mouse entre dois filhos?
          for (let i = 0; i < visibleChildren.length - 1; i++) {
            const curRect = visibleChildren[i].getBoundingClientRect();
            const nextRect = visibleChildren[i + 1].getBoundingClientRect();
            if (mouseY >= curRect.bottom && mouseY <= nextRect.top) {
              showIndicatorAfter(visibleChildren[i]);
              const curId = Number(visibleChildren[i].dataset.id);
              return {
                parentId: slotParentId,
                slotName: slot.dataset.slot,
                targetBlockId: curId,
                position: 'after'
              };
            }
          }
        }

        // Slot vazio ou mouse no padding do slot
        slot.classList.add('drag-over');
        showIndicatorInsideSlot(slot);
        return {
          parentId: slotParentId,
          slotName: slot.dataset.slot,
          targetBlockId: null,
          position: 'end'
        };
      }
    }

    // --- Mouse está sobre o bloco mas NÃO sobre nenhum slot ---
    // Usar a zona do header para decidir before/after
    const header = blockEl.querySelector(':scope > .block-header');
    const headerBottom = header
      ? header.getBoundingClientRect().bottom
      : rect.top + Math.min(rect.height / 2, 40);

    // Se o mouse está acima da metade do header → before
    // Se está abaixo do header → after (mesmo que esteja na zona dos children sem slots)
    const headerMid = rect.top + (headerBottom - rect.top) / 2;
    const pos = mouseY < headerMid ? 'before' : 'after';

    if (pos === 'before') showIndicatorBefore(blockEl);
    else showIndicatorAfter(blockEl);

    const parentInfo = getParentInfo(blockId);
    return {
      parentId: parentInfo?.parentId ?? null,
      slotName: parentInfo?.slotName ?? null,
      targetBlockId: blockId,
      position: pos
    };
  }

  // --- Processar todos os root block-instances ---
  const rootBlockEls = blocksContainer.querySelectorAll(':scope > .block-instance');
  for (const blockEl of rootBlockEls) {
    const result = processBlockElement(blockEl);
    if (result) return result;
  }

  // --- Mouse não está sobre nenhum bloco root — encontrar o root mais próximo ---
  let closest = null;
  let closestDist = Infinity;
  let closestPos = 'after';

  for (const blockEl of rootBlockEls) {
    const blockId = Number(blockEl.dataset.id);
    if (isDraggedOrDescendant(blockId)) continue;
    if (blockEl.closest('.block-instance.dragging')) continue;

    const rect = blockEl.getBoundingClientRect();
    const blockMidY = rect.top + rect.height / 2;
    const dist = Math.abs(mouseY - blockMidY);
    if (dist < closestDist) {
      closestDist = dist;
      closest = blockEl;
      closestPos = mouseY < blockMidY ? 'before' : 'after';
    }
  }

  if (closest) {
    const blockId = Number(closest.dataset.id);
    if (closestPos === 'before') showIndicatorBefore(closest);
    else showIndicatorAfter(closest);
    return {
      parentId: null,
      slotName: null,
      targetBlockId: blockId,
      position: closestPos
    };
  }

  // Workspace vazio ou mouse muito longe
  hideIndicator();
  return {
    parentId: null,
    slotName: null,
    targetBlockId: null,
    position: 'end'
  };
}

// Handler de drop centralizado
function handleDrop(e) {
  e.preventDefault();
  const config = currentDropConfig;
  cleanupDrag();
  if (!config) return;

  const payload = e.dataTransfer.getData('text/plain');
  if (!payload) return;

  if (payload.startsWith('move:')) {
    const sourceId = Number(payload.replace('move:', ''));
    if (!sourceId) return;
    if (config.targetBlockId === sourceId && config.position !== 'end') return;
    // Impede mover um container para dentro de si mesmo
    if (config.parentId === sourceId) {
      alert('Não é possível mover um bloco para dentro de si mesmo.');
      return;
    }
    // Impede mover um container para dentro de si mesmo ou de seus descendentes
    const targetId = config.parentId ?? config.targetBlockId;
    if (targetId && (targetId === sourceId || isDescendant(targetId, sourceId))) {
      alert('Não é possível mover para dentro de um bloco filho do próprio bloco.');
      return;
    }
    reorderTree(sourceId, config);
  } else {
    const newBlock = createBlockFromAction(payload);
    if (!newBlock) return;
    blocks.push(newBlock);
    reorderTree(newBlock.id, config);
  }

  renderBlocks();
}

// ---- Workspace event listeners (ÚNICOS handlers de dragover/drop) ----

workspace.addEventListener('dragover', (e) => {
  e.preventDefault();
  if (!dragState) return;
  e.dataTransfer.dropEffect = dragState.type === 'move' ? 'move' : 'copy';
  currentDropConfig = calcDropTarget(e.clientX, e.clientY);
});

workspace.addEventListener('drop', handleDrop);

workspace.addEventListener('dragleave', (e) => {
  if (!workspace.contains(e.relatedTarget)) {
    cleanupDrag();
  }
});

// ============================================================
// 9. GERAÇÃO DO JSON
// ============================================================
function generateJSON() {
  const rootBlocks = blocks.filter(b => !isChildBlock(b.id));
  const steps = rootBlocks.map(b => buildStep(b)).filter(s => s !== null);
  const flow = {
    name: "Meu Fluxo",
    steps: steps
  };
  return JSON.stringify(flow, null, 2);
}

function buildFlowFromJSON(flowData) {
  if (!flowData || typeof flowData !== 'object') {
    throw new Error('Formato de fluxo inválido.');
  }

  const steps = Array.isArray(flowData.steps) ? flowData.steps : [];
  blocks = [];
  nextId = 1;

  function createBlockFromStep(step) {
    if (!step || typeof step !== 'object' || !step.action) return null;
    const def = BLOCK_DEFS.find(d => d.action === step.action);
    if (!def) return null;

    const block = createBlockFromAction(step.action);
    if (!block) return null;
    Object.keys(step).forEach(key => {
      if (key === 'action') return;
      if (def.params.some(p => p.name === key)) {
        block.params[key] = step[key];
      }
    });

    if (def.children) {
      const slots = def.childrenSlots || ['steps'];
      slots.forEach(slotName => {
        if (Array.isArray(step[slotName])) {
          block.children[slotName] = [];
          step[slotName].forEach(childStep => {
            const childBlock = createBlockFromStep(childStep);
            if (childBlock) {
              block.children[slotName].push(childBlock.id);
            }
          });
        }
      });
    }
    blocks.push(block);
    return block;
  }

  steps.forEach(step => createBlockFromStep(step));
}

function buildStep(block) {
  const def = BLOCK_DEFS.find(d => d.action === block.action);
  if (!def) return null;

  const step = { action: block.action };
  def.params.forEach(param => {
    const val = block.params[param.name];
    if (val === undefined || val === null) return;

     // Regra específica
    if (param.name === 'save_snapshots') {
      step[param.name] = true;
      return;
    }

    const strVal = String(val).trim();
    if (strVal === '') return;
    if (param.type === 'number') {
      step[param.name] = Number(strVal);
    } else {
      step[param.name] = strVal;
    }
  });

  if (def.children && block.children) {
    const slots = def.childrenSlots || ['steps'];
    slots.forEach(slotName => {
      const childIds = block.children[slotName] || [];
      if (childIds.length > 0) {
        const childSteps = childIds.map(id => {
          const childBlock = blocks.find(b => b.id === id);
          return childBlock ? buildStep(childBlock) : null;
        }).filter(s => s !== null);
        if (childSteps.length > 0) {
          step[slotName] = childSteps;
        }
      }
    });
  }
  return step;
}

// ============================================================
// 10. BOTÕES DO PAINEL
// ============================================================
document.getElementById('btnGenerate').addEventListener('click', () => {
  try {
    const json = generateJSON();
    jsonOutput.value = json;
  } catch (err) {
    jsonOutput.value = '❌ Erro ao gerar JSON: ' + err.message;
  }
});

btnSaveFlow.addEventListener('click', async () => {
  if (!blocks.length) {
    alert('Adicione blocos antes de salvar o fluxo.');
    return;
  }
  const name = prompt('Nome do fluxo (sem extensão):');
  if (!name) return;
  const trimmedName = name.trim();
  if (!trimmedName) return;

  try {
    const listResponse = await fetch('/api/flows');
    if (!listResponse.ok) throw new Error('Falha ao listar fluxos existentes.');
    const existingFlows = await listResponse.json();
    const fileName = existingFlows.includes(`${trimmedName}.json`) ? `${trimmedName}.json` : null;
    if (fileName && !confirm(`O arquivo ${fileName} já existe. Deseja sobrescrever?`)) {
      return;
    }

    const payload = {
      name: trimmedName,
      steps: JSON.parse(generateJSON()).steps,
    };
    const response = await fetch('/api/flows', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || 'Falha ao salvar fluxo.');
    }
    const data = await response.json();
    alert(`Fluxo salvo em ${data.path}`);
  } catch (err) {
    alert(err.message);
  }
});

btnLoadFlow.addEventListener('click', async () => {
  try {
    const response = await fetch('/api/flows');
    if (!response.ok) throw new Error('Falha ao listar fluxos.');
    const flowFiles = await response.json();
    if (!Array.isArray(flowFiles) || flowFiles.length === 0) {
      alert('Nenhum fluxo salvo encontrado na pasta flows.');
      return;
    }

    const selected = prompt(`Escolha um fluxo para carregar:\n${flowFiles.join('\n')}`);
    if (!selected) return;
    const sanitized = selected.trim();
    const fileName = flowFiles.includes(sanitized)
      ? sanitized
      : flowFiles.includes(`${sanitized}.json`)
        ? `${sanitized}.json`
        : null;

    if (!fileName) {
      alert('Arquivo não encontrado em flows. Use um nome válido da lista.');
      return;
    }

    const flowResponse = await fetch(`/api/flows/${encodeURIComponent(fileName)}`);
    if (!flowResponse.ok) {
      const error = await flowResponse.json().catch(() => ({}));
      throw new Error(error.detail || 'Falha ao carregar fluxo.');
    }
    const flowData = await flowResponse.json();
    buildFlowFromJSON(flowData);
    renderBlocks();
    jsonOutput.value = generateJSON();
    alert(`Fluxo carregado: ${fileName}`);
  } catch (err) {
    alert(err.message);
  }
});

document.getElementById('btnCopy').addEventListener('click', () => {
  if (jsonOutput.value) {
    navigator.clipboard.writeText(jsonOutput.value).then(() => {
      alert('JSON copiado!');
    }).catch(() => {
      jsonOutput.select();
      document.execCommand('copy');
    });
  }
});
document.getElementById('btnDownload').addEventListener('click', () => {
  if (!jsonOutput.value) {
    alert('Gere o JSON primeiro!');
    return;
  }
  const blob = new Blob([jsonOutput.value], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'fluxo_navyauto.json';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
document.getElementById('btnClear').addEventListener('click', () => {
  if (confirm('Limpar todos os blocos?')) {
    blocks = [];
    renderBlocks();
    jsonOutput.value = '';
  }
});

// ============================================================
// 11. MODAL - CONVERSOR DE ELEMENTO
// ============================================================
function openModal() {
  modal.classList.add('active');
  htmlInput.value = '';
  resultsArea.classList.remove('visible');
  resultsList.innerHTML = '';
  htmlInput.focus();
}

function closeModal() {
  modal.classList.remove('active');
  activeSelectorField = null;
}

modalClose.addEventListener('click', closeModal);
modal.addEventListener('click', (e) => {
  if (e.target === modal) closeModal();
});
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeModal();
});

// Exemplo rápido
btnExample.addEventListener('click', () => {
  htmlInput.value = `<textarea jsname="yZiJbe" class="gLFyf" aria-controls="Alh6id" aria-owns="Alh6id" aria-label="Pesquisar" placeholder="" aria-autocomplete="both" aria-expanded="false" aria-haspopup="false" autocapitalize="off" autocomplete="off" autocorrect="off" id="APjFqb" maxlength="2048" name="q" role="combobox" rows="1" spellcheck="false" data-ved="0ahUKEwjxvr_kgKWVAxWVA7kGHQxAFRgQ39UDCA4">google</textarea>`;
  analyzeHTML();
});

btnClearInput.addEventListener('click', () => {
  htmlInput.value = '';
  resultsArea.classList.remove('visible');
  resultsList.innerHTML = '';
});

btnAnalyze.addEventListener('click', analyzeHTML);

function analyzeHTML() {
  const raw = htmlInput.value.trim();
  if (!raw) {
    alert('Cole o outerHTML do elemento primeiro.');
    return;
  }

  let doc;
  try {
    doc = new DOMParser().parseFromString(raw, 'text/html');
  } catch (e) {
    alert('Erro ao analisar o HTML. Verifique se o código está correto.');
    return;
  }

  const el = doc.body.firstElementChild;
  if (!el) {
    alert('Nenhum elemento encontrado no HTML fornecido.');
    return;
  }

  const tag = el.tagName.toLowerCase();
  const id = el.id || null;
  const classes = el.className ? el.className.split(' ').filter(c => c.trim()) : [];
  const attributes = {};
  for (let attr of el.attributes) {
    attributes[attr.name] = attr.value;
  }

  const candidates = [];
  const stableAttrs = ['name', 'aria-label', 'role', 'data-*', 'placeholder', 'type', 'value'];

  // 1. Tag
  candidates.push({
    selector: tag,
    label: tag,
    stability: 'avoid',
    reason: 'Muito genérico, pode haver vários elementos iguais.'
  });

  // 2. ID
  if (id) {
    const isDynamic = /^[A-Z]{2,}[a-zA-Z0-9]{4,}$/.test(id);
    const stability = isDynamic ? 'avoid' : 'alternative';
    const reason = isDynamic ? 'ID parece gerado automaticamente (pode mudar).' : 'ID estável, mas verifique se é único.';
    candidates.push({
      selector: `#${id}`,
      label: `#${id}`,
      stability: stability,
      reason: reason
    });
  }

  // 3. Classes
  if (classes.length > 0) {
    classes.forEach(cls => {
      const generic = ['active', 'selected', 'hidden', 'visible', 'container', 'wrapper', 'item'];
      if (generic.includes(cls)) return;
      const stability = cls.length > 3 ? 'alternative' : 'avoid';
      const reason = stability === 'alternative' ? 'Classe específica, boa candidata.' : 'Classe muito curta ou genérica.';
      candidates.push({
        selector: `.${cls}`,
        label: `.${cls}`,
        stability: stability,
        reason: reason
      });
    });
  }

  // 4. Atributos estáveis
  const stableKeys = ['name', 'aria-label', 'role', 'placeholder', 'type', 'value'];
  stableKeys.forEach(key => {
    if (attributes[key]) {
      const val = attributes[key];
      const escaped = val.replace(/'/g, "\\'");
      candidates.push({
        selector: `[${key}='${escaped}']`,
        label: `[${key}='${escaped}']`,
        stability: 'recommended',
        reason: `Atributo ${key} é estável e específico.`
      });
    }
  });

  // 5. Data-*
  for (const [key, val] of Object.entries(attributes)) {
    if (key.startsWith('data-')) {
      const escaped = val.replace(/'/g, "\\'");
      candidates.push({
        selector: `[${key}='${escaped}']`,
        label: `[${key}='${escaped}']`,
        stability: 'alternative',
        reason: `Atributo data-* pode ser estável, mas verifique.`
      });
    }
  }

  // 6. Combinações
  if (id) {
    const isDynamic = /^[A-Z]{2,}[a-zA-Z0-9]{4,}$/.test(id);
    if (!isDynamic) {
      candidates.push({
        selector: `${tag}#${id}`,
        label: `${tag}#${id}`,
        stability: 'recommended',
        reason: 'Combinação de tag com ID estável.'
      });
    }
  }
  if (classes.length > 0) {
    classes.forEach(cls => {
      if (cls.length > 3) {
        candidates.push({
          selector: `${tag}.${cls}`,
          label: `${tag}.${cls}`,
          stability: 'alternative',
          reason: 'Tag + classe, boa especificidade.'
        });
      }
    });
  }
  stableKeys.forEach(key => {
    if (attributes[key]) {
      const val = attributes[key].replace(/'/g, "\\'");
      candidates.push({
        selector: `${tag}[${key}='${val}']`,
        label: `${tag}[${key}='${val}']`,
        stability: 'recommended',
        reason: `Tag + ${key}, muito estável.`
      });
    }
  });

  // Remover duplicatas
  const seen = new Set();
  const unique = candidates.filter(c => {
    const key = c.selector;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });

  const order = { recommended: 0, alternative: 1, avoid: 2 };
  unique.sort((a, b) => order[a.stability] - order[b.stability]);

  if (unique.length === 0) {
    resultsList.innerHTML = `<div class="no-results">Nenhum seletor útil encontrado.</div>`;
  } else {
    resultsList.innerHTML = '';
    unique.forEach(c => {
      const div = document.createElement('div');
      div.className = 'result-item';

      const badgeClass = c.stability === 'recommended' ? 'badge-recommended' :
        c.stability === 'alternative' ? 'badge-alternative' : 'badge-avoid';
      const badgeLabel = c.stability === 'recommended' ? '✅ Recomendado' :
        c.stability === 'alternative' ? '👍 Alternativo' : '⚠️ Evitar';

      div.innerHTML = `
        <span class="selector-code">${c.selector}</span>
        <span class="badge ${badgeClass}">${badgeLabel}</span>
        <span style="font-size:0.75rem; color:#64748b; flex:1;">${c.reason}</span>
        <button class="use-btn" data-selector="${c.selector}">Usar</button>
      `;
      resultsList.appendChild(div);
    });

    resultsList.querySelectorAll('.use-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const selector = btn.dataset.selector;
        if (activeSelectorField) {
          activeSelectorField.input.value = selector;
          activeSelectorField.input.dispatchEvent(new Event('change'));
          closeModal();
        } else {
          alert('Nenhum campo de seletor ativo. Feche e tente novamente.');
        }
      });
    });
  }

  resultsArea.classList.add('visible');
}

// ============================================================
// 12. INICIALIZAÇÃO
// ============================================================
renderPalette();

const demoBlocks = [
  { action: 'navigate', params: { url: 'https://google.com', wait_until: 'networkidle' } },
  { action: 'fill', params: { selector: 'textarea[name="q"]', value: 'Navyauto' } },
  { action: 'press', params: { selector: 'input[type="submit"]', key: 'Enter' } },
  { action: 'wait', params: { seconds: 2 } },
  { action: 'screenshot', params: { filename: 'resultado.png' } },
];
demoBlocks.forEach(d => {
  const block = createBlockFromAction(d.action);
  if (block) {
    Object.assign(block.params, d.params);
    blocks.push(block);
  }
});
renderBlocks();

console.log('🧩 Navyauto Blocks — Drag & Drop v2 (centralizado) carregado!');