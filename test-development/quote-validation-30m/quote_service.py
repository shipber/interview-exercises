"""Local assessment simulator. Python 3.10+, standard library only."""

import argparse
import json
from decimal import Decimal, InvalidOperation
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


class InvalidRequest(ValueError):
    pass


def number(value, name):
    if not isinstance(value, str):
        raise InvalidRequest(f"{name} must be a decimal string")
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise InvalidRequest(f"{name} must be a decimal string") from exc
    if not result.is_finite() or result < 0 or result > Decimal("1000000"):
        raise InvalidRequest(f"{name} is outside the supported range")
    return result


def money(value):
    return value.quantize(Decimal("0.01"))


def quote(payload):
    if not isinstance(payload, dict) or payload.get("currency") != "USD":
        raise InvalidRequest("currency must be USD")
    fees = payload.get("fees")
    if not isinstance(fees, list) or not 1 <= len(fees) <= 20:
        raise InvalidRequest("fees must contain 1 to 20 items")
    rate = number(payload.get("fuel_rate"), "fuel_rate")
    if rate > 1:
        raise InvalidRequest("fuel_rate must be between 0 and 1")
    items = []
    seen = set()
    for fee in fees:
        if not isinstance(fee, dict):
            raise InvalidRequest("each fee must be an object")
        code = fee.get("code")
        if not isinstance(code, str) or not code or code in seen:
            raise InvalidRequest("fee code must be nonempty and unique")
        seen.add(code)
        public = number(fee.get("public_amount"), "public_amount")
        cost = number(fee.get("cost_amount"), "cost_amount")
        discount = number(fee.get("discount_percent"), "discount_percent")
        if discount > 100:
            raise InvalidRequest("discount_percent must be between 0 and 100")
        if public != money(public) or cost != money(cost):
            raise InvalidRequest("input amounts must have at most two decimal places")
        amount = money(public * (1 - discount / 100))
        if amount == 0:
            continue
        items.append({"code": code, "amount": format(amount, ".2f")})
    subtotal = sum((Decimal(item["amount"]) for item in items), Decimal("0"))
    fuel = money(subtotal * rate)
    return {
        "currency": "USD",
        "fees": items,
        "subtotal": format(subtotal, ".2f"),
        "fuel": format(fuel, ".2f"),
        "total": format(subtotal + fuel, ".2f"),
    }


def evaluate(payload):
    try:
        return 200, quote(payload)
    except InvalidRequest as exc:
        return 422, {"code": "INVALID_INPUT", "message": str(exc)}


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, body):
        raw = json.dumps(body, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {"status": "ok", "version": "onsite-30m-v1"})
        else:
            self.send_json(404, {"code": "NOT_FOUND"})

    def do_POST(self):
        if self.path != "/quote":
            self.send_json(404, {"code": "NOT_FOUND"})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 65536:
                raise ValueError("request body must contain 1 to 65536 bytes")
            payload = json.loads(self.rfile.read(size))
        except (ValueError, UnicodeError) as exc:
            self.send_json(400, {"code": "INVALID_JSON", "message": str(exc)})
            return
        self.send_json(*evaluate(payload))

    def log_message(self, fmt, *args):
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--quote-file", type=Path)
    args = parser.parse_args()
    if args.quote_file:
        payload = json.loads(args.quote_file.read_text(encoding="utf-8"))
        status, body = evaluate(payload)
        print(json.dumps({"status": status, "body": body}, ensure_ascii=False))
        return
    server = HTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Listening on http://127.0.0.1:{server.server_port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
