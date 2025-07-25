// src/app/perfil/page.tsx
"use client";

import { useEffect, useState } from "react";
import axios from "axios";
import { useAuth } from "@/context/AuthContext";
import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { ProfileForm } from "@/components/forms/ProfileForm";
import type { ProfileFormValues } from "@/schemas/profileSchema";

// Define um tipo para os dados do paciente que virão da API
interface PacienteData {
  id: string;
  nome_completo: string;
  telefone?: string | null;
  usuario: {
    id: string;
    email: string;
    foto_perfil_url?: string | null; // Adicionado
  };
}

export default function PerfilPage() {
  const { user } = useAuth();
  const [pacienteData, setPacienteData] = useState<PacienteData | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function fetchProfileData() {
      if (user?.user_id) {
        setIsLoading(true);
        try {
          const token = document.cookie.replace(/(?:(?:^|.*;\s*)zello-token\s*=\s*([^;]*).*$)|^.*$/, "$1");
          const response = await axios.get(
            `http://localhost:8080/api/v1/pacientes/${user.user_id}`,
            { headers: { Authorization: `Bearer ${token}` } }
          );
          setPacienteData(response.data);
        } catch (error) {
          console.error("Falha ao buscar dados do perfil:", error);
          setPacienteData(null);
        } finally {
          setIsLoading(false);
        }
      } else {
        setIsLoading(false);
      }
    }
    fetchProfileData();
  }, [user]);

  // Função para lidar com a submissão do formulário
  const handleUpdateProfile = async (data: ProfileFormValues) => {
    if (!pacienteData) return;

    // Monta o payload para a API, aninhando os dados do usuário
    const payload = {
        nome_completo: data.nome_completo,
        telefone: data.telefone,
        usuario: {
            foto_perfil_url: data.foto_perfil_url
        }
    };

    try {
      const token = document.cookie.replace(/(?:(?:^|.*;\s*)zello-token\s*=\s*([^;]*).*$)|^.*$/, "$1");
      await axios.put(
        `http://localhost:8080/api/v1/pacientes/${pacienteData.usuario.id}`,
        payload,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert("Perfil atualizado com sucesso!");
      // O ideal aqui seria também atualizar o estado local ou o AuthContext
    } catch (error) {
      console.error("Falha ao atualizar o perfil:", error);
      alert("Não foi possível atualizar o perfil.");
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
        {isLoading ? (
          <p>Carregando seu perfil...</p>
        ) : pacienteData ? (
          <ProfileForm 
            currentUserData={{
                nome_completo: pacienteData.nome_completo,
                telefone: pacienteData.telefone,
                foto_perfil_url: pacienteData.usuario.foto_perfil_url, // Passando o campo da foto
            }}
            onSubmit={handleUpdateProfile} 
          />
        ) : (
          <p>Não foi possível carregar os dados do seu perfil.</p>
        )}
      </div>
    </DashboardLayout>
  );
}