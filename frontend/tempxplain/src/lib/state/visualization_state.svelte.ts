import { backend } from "$lib/backend.svelte";
import type { Model } from "$lib/bindings";

class VisualizationState {
  #cache = new Map<string, string>();

  get_key(model: Model, t: number): string {
    return `${model}:${t}`;
  }

  async get(model: Model, t: number): Promise<string | undefined> {
    const key = this.get_key(model, t);
    let image = this.#cache.get(key);
    if (image === undefined) {
      const result = await backend.call("get_visualization", { model, t });
      if (result === null) {
        return undefined;
      }
      image = `data:image/svg+xml;base64,${result}`;
      this.#cache.set(key, image);
    }
    return image;
  }
}

export const visualization_state = new VisualizationState();
