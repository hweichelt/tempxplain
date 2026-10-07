import { backend } from "$lib/backend.svelte";
import type { Explanation, ProgramData } from "$lib/bindings";

class ProgramState {
  program: string | undefined = $state();
  program_data: ProgramData | undefined = $state();
  explanation: Explanation | undefined = $state();
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
    const response_program = await backend.call("get_program");
    this.program = response_program;
    const response_program_data = await backend.call("get_program_data");
    this.program_data = response_program_data;
    const response_explanation = await backend.call("get_explanation");
    this.explanation = response_explanation;
    this.is_loading = false;
  }
}

export const program_state = new ProgramState();
