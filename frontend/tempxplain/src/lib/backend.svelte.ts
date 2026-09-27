/**
 * The functions provided by the Python backend (see `src/tempxplain/api.py`).
 *
 * Add an entry here whenever a function is added to the backend.
 */
export interface Api {
  ping: { params: Record<string, never>; result: "pong" };
  set_program: { params: { program: string }; result: null };
  get_program: { params: Record<string, never>; result: string };
}

type Response = { id: number | null } & (
  | { result: unknown; error?: undefined }
  | { error: { type: string; message: string } }
);

type Pending = {
  resolve: (result: never) => void;
  reject: (error: Error) => void;
};

const RECONNECT_DELAY = 1000;
const BACKEND_HOST = "127.0.0.1";
const BACKEND_PORT = 8765;

export class BackendError extends Error {
  constructor(
    readonly type: string,
    message: string,
  ) {
    super(message);
    this.name = type;
  }
}

export class Backend {
  connected = $state(false);

  #socket: WebSocket | null = null;
  #opening: Promise<WebSocket> | null = null;
  #pending = new Map<number, Pending>();
  #nextId = 1;
  #closed = false;

  constructor(readonly url: string) {}

  connect(): Promise<WebSocket> {
    this.#closed = false;
    if (this.#socket?.readyState === WebSocket.OPEN)
      return Promise.resolve(this.#socket);
    this.#opening ??= new Promise((resolve, reject) => {
      const socket = new WebSocket(this.url);
      socket.onopen = () => {
        this.#socket = socket;
        this.#opening = null;
        this.connected = true;
        resolve(socket);
      };
      socket.onmessage = (event) => this.#receive(event.data);
      socket.onclose = () => {
        this.#socket = null;
        this.#opening = null;
        this.connected = false;
        const error = new Error(`connection to backend at ${this.url} lost`);
        reject(error);
        for (const pending of this.#pending.values()) pending.reject(error);
        this.#pending.clear();
        // Try to reconnect automatically
        if (!this.#closed) {
          setTimeout(
            () => !this.#closed && this.connect().catch(() => {}),
            RECONNECT_DELAY,
          );
        }
      };
    });
    return this.#opening;
  }

  /** Call a function in the backend and wait for its result. */
  async call<M extends keyof Api>(
    method: M,
    ...[params]: Api[M]["params"] extends Record<string, never>
      ? []
      : [Api[M]["params"]]
  ): Promise<Api[M]["result"]> {
    const socket = await this.connect();
    const id = this.#nextId++;
    return new Promise((resolve, reject) => {
      this.#pending.set(id, { resolve, reject });
      socket.send(JSON.stringify({ id, method, params: params ?? {} }));
    });
  }

  close() {
    this.#closed = true;
    this.#socket?.close();
  }

  #receive(data: string) {
    const response: Response = JSON.parse(data);
    const pending =
      response.id === null ? undefined : this.#pending.get(response.id);
    if (!pending) {
      console.error("unexpected message from backend", response);
      return;
    }
    this.#pending.delete(response.id!);
    if (response.error)
      pending.reject(
        new BackendError(response.error.type, response.error.message),
      );
    else pending.resolve(response.result as never);
  }
}

export const backend = new Backend(
  import.meta.env.VITE_BACKEND_URL ?? `ws://${BACKEND_HOST}:${BACKEND_PORT}`,
);
