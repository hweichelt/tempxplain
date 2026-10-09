import { backend } from "$lib/backend.svelte";
import type { Model } from "$lib/bindings";

class VisualizationState {
  #cache = new Map<string, Promise<string | undefined>>();

  get_key(model: Model, t: number): string {
    return `${model}:${t}`;
  }

  async #fetch(model: Model, t: number): Promise<string | undefined> {
    const result = await backend.call("get_visualization", { model, t });
    return result ?? undefined;
  }

  #load(model: Model, t: number): Promise<string | undefined> {
    const key = this.get_key(model, t);
    let image = this.#cache.get(key);
    if (image === undefined) {
      image = this.#fetch(model, t);
      this.#cache.set(key, image);
      // Drop failed requests from cache (they will be retired on next load)
      image.catch(() => this.#cache.delete(key));
    }
    return image;
  }

  get(
    model: Model,
    t: number,
    fetch_next: boolean = true,
  ): Promise<string | undefined> {
    const image = this.#load(model, t);
    // Already fetch the next image in the background to avoid stuttering on first load
    if (fetch_next) {
      this.#load(model, t + 1).catch(() => {});
    }
    return image;
  }
}

export const visualization_state = new VisualizationState();
