import { seedFeatureSwitches } from "../data/feature-switches"; // ../data is correct

export type FeatureSwitch = {
  id: string;
  name: string;
  currentState: boolean;
  dbKey?: string; // <-- add dbKey (optional for now)
};

const STORAGE_KEY = "thehub_feature_switches";

function safeLocalStorage(): Storage | null {
  try {
    if (typeof window !== "undefined" && window.localStorage) return window.localStorage;
  } catch (_err) { void _err; }
  return null;
}

function loadInitial(): FeatureSwitch[] {
  const ls = safeLocalStorage();
  if (ls) {
    const raw = ls.getItem(STORAGE_KEY);
    if (raw) {
      try { return JSON.parse(raw) as FeatureSwitch[]; } catch (_err) { void _err; }
    }
    // seed (no dbKey in seed, fine)
    ls.setItem(STORAGE_KEY, JSON.stringify(seedFeatureSwitches));
    return seedFeatureSwitches as unknown as FeatureSwitch[];
  }
  return seedFeatureSwitches as unknown as FeatureSwitch[];
}

function persist(list: FeatureSwitch[]) {
  const ls = safeLocalStorage();
  if (ls) ls.setItem(STORAGE_KEY, JSON.stringify(list));
}

function randomId(): string {
  return `fs-${Math.random().toString(36).slice(2, 10)}-${Date.now()}`;
}

let cache: FeatureSwitch[] = loadInitial();

export function getAllFeatureSwitches(): FeatureSwitch[] { return [...cache]; }
export function getFeatureSwitchById(id: string): FeatureSwitch | undefined { return cache.find(x => x.id === id); }

export function createFeatureSwitch(data: Omit<FeatureSwitch, "id">): string {
  const id = randomId();
  cache = [{ id, ...data }, ...cache];
  persist(cache);
  return id;
}

export function updateFeatureSwitch(id: string, patch: Partial<FeatureSwitch>): void {
  cache = cache.map(x => x.id === id ? { ...x, ...patch } : x);
  persist(cache);
}

export function deleteFeatureSwitch(id: string): void {
  cache = cache.filter(x => x.id !== id);
  persist(cache);
}

export function toggleFeatureSwitch(id: string): void {
  cache = cache.map(x => x.id === id ? { ...x, currentState: !x.currentState } : x);
  persist(cache);
}
