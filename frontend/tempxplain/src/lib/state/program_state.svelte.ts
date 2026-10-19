import { backend } from "$lib/backend.svelte";
import type { ModelFoil, ModelReference, ProgramData } from "$lib/bindings";

class ModelState {
  program_data: ProgramData | undefined = $state();
  reference: ModelReference | undefined = $state();
  explanation: ModelFoil | undefined = $state();
  is_loading: boolean = $state(false);

  constructor() {
    this.#update();
  }

  async #update() {
    this.is_loading = true;
    const response_program_data = await backend.call("get_program_data");
    this.program_data = response_program_data;
    this.reference = (await backend.call("get_reference")) ?? undefined;
    this.explanation = (await backend.call("get_foil")) ?? undefined;
    this.is_loading = false;
  }
}

export const model_state = new ModelState();
