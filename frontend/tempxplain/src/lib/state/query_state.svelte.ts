import { backend } from "$lib/backend.svelte";
import type { Query, QueryError } from "$lib/bindings";

class QueryState {
  raw: string = $state("");
  parsed: Query[] | undefined = $state();
  error: QueryError | undefined = $state();

  constructor() {
    let initial_query = this.get_query();
  }

  async set_raw(raw: string) {
    this.raw = raw;
    this.#parse();
  }

  async get_query() {
    const result = await backend.call("get_query");
    if (result) {
      this.set_raw(result);
    }
    return result;
  }

  async set_query() {
    backend.call("set_query", { query: this.raw });
  }

  async #parse() {
    const result = await backend.call("parse_query", { query_raw: this.raw });
    if (result.error) {
      this.error = result.error;
    } else {
      this.parsed = result.queries !== null ? result.queries : undefined;
      this.error = undefined;
    }
  }
}

export const query_state = new QueryState();
