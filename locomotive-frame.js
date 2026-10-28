import { mountFrameJViewer } from './framej3d.js';
import { loadCompressedModel } from './lt3-model.js';
const host = document.querySelector('#lt2-viewer');
mountFrameJViewer(host, {
  modelData: await loadCompressedModel(new URL('./assets/locomotive-lt2/integration-model.json.gz', import.meta.url)),
  title: 'LT2 · locomotive main frame and removable skid',
  badge: 'PRELIMINARY PHYSICAL PARTS',
  groupControls: true,
  note: '54 LT2 steel solids plus32 unchanged DT2 reference parts. Main-frame and engine-skid proposals; no fabrication release. Viewer dimensions are inches; CAD source and drawings are millimetres.'
});
host.querySelector('[data-action=reset]').textContent = 'Whole frame';
const fallback = host.querySelector('.coach3d-error a');
fallback.href = '#drawings';
fallback.textContent = 'Open frame drawings';
host.querySelector('.coach3d-options').hidden = true;
