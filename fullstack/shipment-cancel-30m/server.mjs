/** Onsite starter. Node.js 18+, standard library only. */
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';

// In-memory fixtures. Restart the process to reset; no database is needed.
const shipments = [
  { id: 'S1001', recipient: 'Alex Chen', status: 'ready' },
  { id: 'S1002', recipient: 'Sam Lee', status: 'shipped' },
  { id: 'S1003', recipient: 'Robin Lin', status: 'cancelled' },
];

// TODO 1: Implement the business rules in TASK.md. Return { status, body }.
// The HTTP adapter below already handles routing and JSON serialization.
export function cancelShipment(id) {
  return {
    status: 501,
    body: { code: 'NOT_IMPLEMENTED', message: '取消接口尚未实现' },
  };
}

const assets = new Map([
  ['/', ['index.html', 'text/html; charset=utf-8']],
  ['/app.js', ['app.js', 'text/javascript; charset=utf-8']],
]);

function sendJson(response, status, body) {
  const raw = JSON.stringify(body);
  response.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(raw),
    'Cache-Control': 'no-store',
  });
  response.end(raw);
}

const server = createServer(async (request, response) => {
  try {
    const pathname = new URL(request.url, 'http://localhost').pathname;
    if (request.method === 'GET' && pathname === '/health') {
      sendJson(response, 200, { status: 'ok', version: 'F-ON-30-v1.0' });
      return;
    }
    if (request.method === 'GET' && pathname === '/api/shipments') {
      sendJson(response, 200, { shipments });
      return;
    }
    const match = pathname.match(/^\/api\/shipments\/([A-Za-z0-9_-]+)\/cancel$/);
    if (request.method === 'POST' && match) {
      const result = cancelShipment(match[1]);
      sendJson(response, result.status, result.body);
      return;
    }
    if (request.method === 'GET' && assets.has(pathname)) {
      const [file, contentType] = assets.get(pathname);
      const raw = await readFile(new URL(`./public/${file}`, import.meta.url));
      response.writeHead(200, {
        'Content-Type': contentType,
        'Cache-Control': 'no-store',
      });
      response.end(raw);
      return;
    }
    sendJson(response, 404, { code: 'NOT_FOUND', message: '路径不存在' });
  } catch (error) {
    console.error(error);
    sendJson(response, 500, { code: 'INTERNAL_ERROR', message: '服务异常' });
  }
});

const port = Number(process.env.PORT || 8766);
server.listen(port, '127.0.0.1', () => {
  console.log(`Open http://127.0.0.1:${server.address().port}`);
});
