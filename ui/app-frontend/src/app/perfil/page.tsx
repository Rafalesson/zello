// src/app/perfil/page.tsx
"use client";

import { useAuth } from "@/context/AuthContext";
import { DashboardLayout } from "@/components/layout/DashboardLayout";
// Supondo que você renomeou 'ProfileForm.tsx' para 'PacienteProfileForm.tsx'
import { PacienteProfileForm } from "@/components/forms/PacienteProfileForm"; 
import { MedicoProfileForm } from "@/components/forms/MedicoProfileForm";
import { Card, CardContent } from "@/components/ui/Card";

export default function PerfilPage() {
  const { user } = useAuth();

  const renderProfileContent = () => {
    // Exibe um estado de carregamento enquanto o objeto 'user' do contexto é populado
    if (!user) {
      return <p>Carregando perfil...</p>;
    }

    // Decide qual componente renderizar com base no tipo de usuário
    switch (user.tipo_usuario) {
      case 'PACIENTE':
        // A lógica de busca e atualização de dados deve ser encapsulada dentro deste componente
        return <PacienteProfileForm />; 
      case 'MEDICO':
        return <MedicoProfileForm />;
      case 'ADMIN':
        return (
          <Card>
            <CardContent className="pt-6">
              <h3 className="font-semibold">Perfil de Administrador</h3>
              <p className="text-sm text-slate-600 mt-2">
                E-mail: {user.email}
              </p>
              <p className="text-sm text-slate-600">
                ID: {user.user_id}
              </p>
              <p className="mt-4 text-xs text-slate-500">
                A gestão de administradores é feita via CLI.
              </p>
            </CardContent>
          </Card>
        );
      default:
        return <p className="text-red-600">Tipo de perfil desconhecido.</p>;
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-4">
        <h1 className="text-3xl font-bold text-slate-800">Meu Perfil</h1>
        <p className="text-slate-600">
          Gerencie suas informações pessoais e de contato.
        </p>
      </div>
      <div className="mt-8 border-t border-slate-200 pt-8">
        {renderProfileContent()}
      </div>
    </DashboardLayout>
  );
}