// src/app/dashboard/page.tsx
import { DashboardLayout } from "@/components/layout/DashboardLayout";

export default function DashboardPage() {
  return (
    <DashboardLayout>
      <h1 className="text-3xl font-bold text-slate-800">Visão Geral</h1>
      <p className="mt-2 text-slate-600">
        Aqui você verá sua próxima consulta e outras informações importantes.
      </p>
      {/* O ProximaConsultaCard virá aqui no futuro */}
    </DashboardLayout>
  );
}