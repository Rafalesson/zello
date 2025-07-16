// src/context/AuthContext.tsx
"use client";

import { createContext, useContext, useState, ReactNode, useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { useRouter, usePathname } from 'next/navigation';
import { jwtDecode } from 'jwt-decode'; // Usaremos uma biblioteca mais robusta para decodificar

// Define a interface para os dados do usuário que virão do token
interface User {
  email: string;
  user_id: string;
  tipo_usuario: 'PACIENTE' | 'MEDICO' | 'ADMIN';
  foto_perfil_url?: string | null;
}

// Define a interface para o valor do nosso contexto
interface AuthContextType {
  isAuthenticated: boolean;
  user: User | null;
  login: (loginData: any) => Promise<void>;
  logout: () => void;
}

// Cria o contexto com um valor inicial
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Cria o Provedor do Contexto
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const router = useRouter();
  const pathname = usePathname();

  // Efeito para verificar o token nos cookies quando o app carrega
  useEffect(() => {
    const token = Cookies.get('zello-token');
    if (token) {
      try {
        const decoded = jwtDecode<User & { sub: string }>(token);
        // O 'sub' é o email, que já temos. Vamos mapear para o nosso objeto User.
        setUser({ email: decoded.sub, user_id: decoded.user_id, tipo_usuario: decoded.tipo_usuario });
      } catch (error) {
        console.error("Token inválido:", error);
        logout(); // Se o token for inválido, limpa tudo
      }
    }
  }, []);


  const login = async (loginData: any) => {
    console.log("3. Função login do AuthContext foi alcançada.");
    
    try {
      const params = new URLSearchParams();
      params.append('username', loginData.username);
      params.append('password', loginData.password);
      
      const response = await axios.post('http://localhost:8080/api/v1/auth/login', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });
      
      const { access_token } = response.data;

      Cookies.set('zello-token', access_token, { expires: 1, secure: process.env.NODE_ENV === 'production', sameSite: 'strict' });
      
      const decoded = jwtDecode<User & { sub: string }>(access_token);
      setUser({ email: decoded.sub, user_id: decoded.user_id, tipo_usuario: decoded.tipo_usuario });
      
      router.push('/dashboard');
    } catch (error) {
      console.error("Falha no login:", error);
      throw new Error('E-mail ou senha inválidos.');
    }
  };

  const logout = () => {
    Cookies.remove('zello-token');
    setUser(null);
    router.push('/'); // Redireciona para a home page ao sair
  };

  const value = { isAuthenticated: !!user, user, login, logout };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
} // <--- A CHAVE FALTANTE ESTAVA PROVAVELMENTE AQUI

// Hook customizado para facilitar o uso do contexto
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  }
  return context;
}