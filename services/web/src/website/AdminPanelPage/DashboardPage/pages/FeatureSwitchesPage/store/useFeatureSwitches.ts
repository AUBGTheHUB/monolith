// services/web/src/website/AdminPanelPage/DashboardPage/pages/FeatureSwitchesPage/store/useFeatureSwitches.ts
import type { FeatureSwitch } from "../types";
import { seedFeatureSwitches } from "../data/feature-switches";

/**
 * Client-only mocked store.
 * While the API isn’t available, we persist to localStorage so
 * creates/edits/toggles survive page reloads. Remove this layer when
 * wiring the FastAPI routes.
 */
const STORAGE_KEY = "thehub_feature_switches";

function safeLocalStorage(): Storage | null {
  try {
    if (typeof window !== "undefined" && window.localStorage) return window.localStorage;
  } catch {
    /* ignore */
  }
  return null;
}

function loadInitial(): FeatureSwitch[] {
  const ls = safeLocalStorage();
  if (ls) {
    const raw = ls.getItem(STORAGE_KEY);
    if (raw) {
      try {
        return JSON.parse(raw) as FeatureSwitch[];
      } catch {
        /* ignore and fall through */
      }
    }
    ls.setItem(STORAGE_KEY, JSON.stringify(seedFeatureSwitches));
    return seedFeatureSwitches;
  }
  return seedFeatureSwitches;
}

function persist(list: FeatureSwitch[]) {
  const ls = safeLocalStorage();
  if (ls) ls.setItem(STORAGE_KEY, JSON.stringify(list));
}

// In-memory cache to simulate a tiny client-side repo.
let cache: FeatureSwitch[] = loadInitial();

export function getAllFeatureSwitches(): FeatureSwitch[] {
  return [...cache];
}

export function getFeatureSwitchById(id: string): FeatureSwitch | undefined {
  return cache.find((x) => x.id === id);
}

/**
 * Create a new FS.
 * NOTE: Temporary id minting for the prototype only.
 * The real implementation will POST and use the id returned by the API.
 */
export function createFeatureSwitch(data: Omit<FeatureSwitch, "id">): string {
  const next = `fs-${cache.length + 1}`; // simple, predictable temp id
  cache = [{ id: next, ...data }, ...cache];
  persist(cache);
  return next;
}

export function updateFeatureSwitch(id: string, patch: Partial<FeatureSwitch>): void {
  cache = cache.map((x) => (x.id === id ? { ...x, ...patch } : x));
  persist(cache);
}

export function deleteFeatureSwitch(id: string): void {
  cache = cache.filter((x) => x.id !== id);
  persist(cache);
}

export function toggleFeatureSwitch(id: string): void {
  cache = cache.map((x) => (x.id === id ? { ...x, currentState: !x.currentState } : x));
  persist(cache);
}
