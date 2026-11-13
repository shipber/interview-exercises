const list = document.querySelector('#shipments');
const message = document.querySelector('#message');
const reload = document.querySelector('#reload');
const labels = { ready: '待发货', shipped: '已发货', cancelled: '已取消' };
let shipments = [];

function showMessage(text, kind = 'info') {
  message.textContent = text;
  message.dataset.kind = kind;
}

function render() {
  list.replaceChildren();
  for (const shipment of shipments) {
    const row = document.createElement('tr');
    for (const value of [shipment.id, shipment.recipient, labels[shipment.status]]) {
      const cell = document.createElement('td');
      cell.textContent = value;
      row.append(cell);
    }
    const action = document.createElement('td');
    if (shipment.status === 'ready') {
      const button = document.createElement('button');
      button.type = 'button';
      button.textContent = '取消运单';
      button.addEventListener('click', () => cancelShipment(shipment.id, button));
      action.append(button);
    } else {
      action.textContent = '—';
    }
    row.append(action);
    list.append(row);
  }
}

async function loadShipments() {
  reload.disabled = true;
  showMessage('正在加载…');
  try {
    const response = await fetch('/api/shipments');
    if (!response.ok) throw new Error(`加载失败（HTTP ${response.status}）`);
    const body = await response.json();
    shipments = body.shipments;
    render();
    showMessage(`共 ${shipments.length} 条运单`);
  } catch (error) {
    showMessage(error.message, 'error');
  } finally {
    reload.disabled = false;
  }
}

// TODO 2: Call the cancellation API and handle pending/success/failure states.
// You may add state or adjust render/loadShipments above when needed.
async function cancelShipment(id, button) {
  showMessage(`待实现：取消 ${id}`);
}

reload.addEventListener('click', loadShipments);
loadShipments();
