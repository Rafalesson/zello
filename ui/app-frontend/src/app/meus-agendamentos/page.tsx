// src/app/meus-agendamentos/page.tsx
import { DashboardLayout } from "@/components/layout/DashboardLayout";

export default function MeusAgendamentosPage() {
  return (
    <DashboardLayout>
      <h1 className="text-3xl font-bold text-slate-800">Meus Agendamentos</h1>
      <p className="mt-2 text-slate-600">
        Acompanhe suas consultas futuras e seu histórico de atendimentos.
      </p>
      {/* A lista de agendamentos será renderizada aqui */}
    </DashboardLayout>
  );
}