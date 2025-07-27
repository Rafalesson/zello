// src/context/AuthContext.tsx
"use client";

import { createContext, useContext, useState, ReactNode, useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { useRouter } from 'next/navigation';
import { jwtDecode } from 'jwt-decode';

interface User {
  email: string;
  user_id: string;
  tipo_usuario: 'PACIENTE' | 'MEDICO' | 'ADMIN';
  sexo: 'MASCULINO' | 'FEMININO' | 'OUTRO' | null;
  foto_perfil_url?: string | null;
}

interface AuthContextType {
  isAuthenticated: boolean;
  user: User | null;
  login: (loginData: any) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const router = useRouter();

  useEffect(() => {
    const token = Cookies.get('zello-token');
    if (token) {
      try {
        const decoded = jwtDecode<User & { sub: string }>(token);
        setUser({ 
          email: decoded.sub, 
          user_id: decoded.user_id, 
          tipo_usuario: decoded.tipo_usuario,
          sexo: decoded.sexo,
          foto_perfil_url: decoded.foto_perfil_url
        });
      } catch (error) {
        console.error("Token inválido, limpando sessão:", error);
        logout();
      }
    }
  }, []);

  const login = async (loginData: any) => {
    try {
      const params = new URLSearchParams();
      params.append('username', loginData.username);
      params.append('password', loginData.password);

      const response = await axios.post('http://localhost:8080/api/v1/auth/login', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });

      const { access_token } = response.data;

      Cookies.set('zello-token', access_token, { expires: 1 });

      const decoded = jwtDecode<User & { sub: string }>(access_token);
      setUser({ 
        email: decoded.sub, 
        user_id: decoded.user_id, 
        tipo_usuario: decoded.tipo_usuario,
        sexo: decoded.sexo,
        foto_perfil_url: decoded.foto_perfil_url
      });

      router.push('/dashboard');
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        throw new Error(error.response.data.detail || 'E-mail ou senha inválidos.');
      }
      throw new Error('Não foi possível conectar ao servidor.');
    }
  };

  const logout = () => {
    Cookies.remove('zello-token');
    setUser(null);
    router.push('/');
  };

  const value = { isAuthenticated: !!user, user, login, logout };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  }
  return context;
}