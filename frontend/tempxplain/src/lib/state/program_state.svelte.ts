import { backend, type BackendError } from "$lib/backend.svelte";

class ProgramState {
  program: string | undefined = $state();
  is_loading: boolean = $state(false);

  constructor() {
    this.#update();
  }

  async set_program(program: string) {
    await backend.call("set_program", { program: program });
    this.#update();
  }

  async #update() {
    this.is_loading = true;
    const response = await backend.call("get_program");
    this.program = response;
    this.is_loading = false;
  }
}

export const program_state = new ProgramState();
