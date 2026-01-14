// services/web/src/website/AdminPanelPage/DashboardPage/pages/FeatureSwitchesPage/FeatureSwitchAddPage.tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Input } from "@/components/ui/input";
import { featureSwitchSchema, type FeatureSwitchForm } from "./schema";
import { createFeatureSwitch } from "./store/useFeatureSwitches";

export default function FeatureSwitchAddPage() {
  const {
    register,
    handleSubmit,
    formState: { errors, isValid, isSubmitting },
  } = useForm<FeatureSwitchForm>({
    resolver: zodResolver(featureSwitchSchema),
    mode: "onChange",
    defaultValues: { name: "" },
  });

  const outlineBtn =
    "px-4 py-2 rounded-md border border-slate-300 bg-white text-slate-900 hover:bg-slate-800 hover:text-white transition-colors";

  const onSubmit = (data: FeatureSwitchForm) => {
    createFeatureSwitch({ name: data.name.trim(), currentState: false });
    window.location.assign("/dashboard/feature-switches");
  };

  return (
    <div className="min-h-screen grid place-items-center p-6">
      <div className="relative w-full max-w-2xl rounded-[28px] border bg-background p-10 shadow-sm">
        <h2 className="text-center text-2xl font-semibold mb-8 text-plate-800">Add new FS</h2>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6" noValidate>
          <div>
            <label className="block text-sm font-medium mb-1 text-plate-800">Name</label>
            <Input
              maxLength={12}
              placeholder="FS name"
              {...register("name")}
            />
            <div className="text-xs mt-1 text-slate-500">Min 2, max 12 characters.</div>
            {errors.name && <div className="text-sm text-red-500 mt-1">{errors.name.message}</div>}
          </div>

          <div className="flex gap-3 justify-center pt-2">
            <a href="/dashboard/feature-switches">
              <button type="button" className={outlineBtn}>Cancel</button>
            </a>
            <button
              type="submit"
              disabled={!isValid || isSubmitting}
              className="px-4 py-2 rounded-md bg-teal-500 text-white hover:bg-teal-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              title="Add feature switch"
            >
              {isSubmitting ? "Adding…" : "Add FS"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
