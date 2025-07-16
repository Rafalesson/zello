// src/app/dashboard/page.tsx
"use client"; // Esta página usa hooks, portanto é um Componente de Cliente

import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { Button } from "@/components/ui/Button";

export default function DashboardPage() {
  // Usa nosso hook de autenticação para obter os dados e a função de logout
  const { user, logout, isAuthenticated } = useAuth();
  const router = useRouter();

  // Efeito para proteger a rota: se o usuário não estiver autenticado,
  // redireciona para a página de login.
  useEffect(() => {
    // Adicionamos uma verificação extra para o caso do estado inicial ser nulo
    if (isAuthenticated === false) {
      router.push("/login");
    }
  }, [isAuthenticated, router]);

  // Mostra uma mensagem de carregamento enquanto o estado de autenticação é verificado
  if (!user) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p>Carregando...</p>
      </div>
    );
  }

  // Renderiza o conteúdo do dashboard se o usuário estiver logado
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 bg-gray-50">
      <div className="w-full max-w-2xl text-center space-y-4">
        <h1 className="text-4xl font-bold">Bem-vindo(a) ao Zello!</h1>
        <p className="text-xl text-gray-700">
          Você está logado como:{" "}
          <span className="font-semibold text-blue-600">{user.email}</span>
        </p>
        <p className="text-md text-gray-500">
          Seu tipo de perfil é:{" "}
          <span className="font-semibold">{user.tipo_usuario}</span>
        </p>
        <div>
          <Button onClick={logout} variant="secondary" size="sm">
            Sair
          </Button>
        </div>
      </div>
    </main>
  );
}