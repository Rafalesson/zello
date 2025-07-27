// src/components/forms/MedicoProfileForm.tsx
"use client";
import { Button } from "../ui/Button";
import { Input } from "../ui/Input";

// Este é um componente de placeholder por enquanto.
// A lógica completa de busca de dados e atualização será similar à do PacienteProfileForm.
export function MedicoProfileForm() {
  return (
    <div className="space-y-6 max-w-lg">
      <Input id="nome_completo" label="Nome Completo (Médico)" type="text" defaultValue="Carregando..." />
      <Input id="crm" label="CRM" type="text" defaultValue="Carregando..." />
      <p className="text-sm text-slate-500">A edição de especialidades será implementada em breve.</p>
      <div className="pt-2">
        <Button type="submit">Salvar Alterações</Button>
      </div>
    </div>
  );
}